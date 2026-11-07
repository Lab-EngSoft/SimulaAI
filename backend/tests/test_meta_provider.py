
"""Testes do provedor Meta sem acesso à API externa."""

from types import SimpleNamespace

import pytest

from app.services import ia


def _contexto():
    return ia.ContextoExplicacao(
        materia="Matemática",
        assunto="Porcentagem",
        enunciado="Quanto é 25% de 40?",
        alternativas=("10", "20", "30"),
        resposta_aluno="20",
        resposta_correta="10",
    )


def test_sem_chave_nao_habilita_ia(monkeypatch):
    monkeypatch.delenv("META_API_KEY", raising=False)
    monkeypatch.setenv(
        "NVIDIA_API_KEY",
        "chave-antiga-ignorada",
    )

    assert ia.status_ia() is False

    with pytest.raises(
        ia.IAIndisponivel,
        match="META_API_KEY",
    ):
        ia.obter_provedor()


def test_configuracao_contributor_e_prompt_educacional(monkeypatch):
    chamadas = []

    class ClienteFalso:
        def __init__(self, **kwargs):
            chamadas.append(("config", kwargs))
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=self.create)
            )

        def create(self, **kwargs):
            chamadas.append(("gerar", kwargs))
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        finish_reason="stop",
                        message=SimpleNamespace(
                            content="  Porque 25% de 40 é 10.  "
                        ),
                    )
                ]
            )

    monkeypatch.setattr(ia, "OpenAI", ClienteFalso)
    monkeypatch.setenv("META_API_KEY", "segredo-nao-revelar")
    monkeypatch.delenv("META_MODEL", raising=False)
    monkeypatch.delenv("META_BASE_URL", raising=False)

    assert ia.status_ia() is True

    assert (
        ia.obter_provedor().explicar(_contexto())
        == "Porque 25% de 40 é 10."
    )

    assert chamadas[0][1]["base_url"] == "https://api.meta.ai/v1"
    assert chamadas[0][1]["api_key"] == "segredo-nao-revelar"

    chamada = chamadas[1][1]

    assert chamada["model"] == "muse-spark-1.3-contributor"
    assert chamada["messages"][0]["role"] == "developer"
    assert '"resposta_correta": "10"' in (
        chamada["messages"][1]["content"]
    )
    assert chamada["max_completion_tokens"] == 1600
    assert chamada["stream"] is False


def test_resposta_incompleta_nao_e_salva(monkeypatch):
    class ClienteFalso:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **kw: SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                finish_reason="length",
                                message=SimpleNamespace(content="parcial"),
                            )
                        ]
                    )
                )
            )

    monkeypatch.setattr(ia, "OpenAI", ClienteFalso)

    with pytest.raises(
        ia.IAIndisponivel,
        match="interrompida",
    ):
        ia.ProvedorMeta("chave-teste").explicar(_contexto())


def test_falha_da_api_oculta_detalhes_do_provedor(monkeypatch):
    from openai import APIConnectionError
    import httpx

    class ClienteFalso:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=self.create)
            )

        def create(self, **kwargs):
            request = httpx.Request(
                "POST",
                "https://api.meta.ai/v1/chat/completions",
            )
            raise APIConnectionError(request=request)

    monkeypatch.setattr(ia, "OpenAI", ClienteFalso)

    with pytest.raises(
        ia.IAIndisponivel,
        match="indisponível",
    ):
        ia.ProvedorMeta("chave-teste").explicar(_contexto())
