"""História #7 (Sprint 3) — explicação da resposta errada pelo tutor.

Estratégia em duas camadas (a regra que o CT08 consagrou na Sprint 2):

1. Se a chave ``AI_API_KEY`` estiver configurada, tentamos chamar o provedor
   de IA compatível com a API da OpenAI (``AI_BASE_URL``/``AI_MODEL``).
2. Se a chave não existe, ou a chamada falha por QUALQUER motivo (rede,
   timeout, erro do provedor), geramos uma explicação determinística usando
   somente os dados já cadastrados no banco (enunciado, alternativa correta,
   alternativa escolhida, assunto e matéria).

Assim, ``gerar_explicacao`` SEMPRE devolve um texto — o objetivo de
"explicar ao menos 90% das respostas incorretas" é cumprido com 100%,
inclusive com a IA fora do ar. A explicação não é requisito para corrigir:
ela é gerada DEPOIS da correção objetiva.
"""
import os

import httpx

_TIMEOUT_SEGUNDOS = 15.0


def _texto_via_ia(questao, alternativa_correta, alternativa_escolhida) -> str | None:
    """Chama o provedor de IA; devolve None em qualquer falha (vira fallback)."""
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    modelo = os.getenv("AI_MODEL", "gpt-4o-mini")
    prompt = (
        "Você é um tutor didático. O aluno respondeu uma questão errada. "
        "Explique em até 4 frases, em português, por que a alternativa correta "
        "é a correta e o que o aluno confundiu. Seja encorajador.\n\n"
        f"Enunciado: {questao.enunciado}\n"
        f"Assunto: {questao.assunto.nome} (matéria: {questao.assunto.materia.nome})\n"
        f"Alternativa CORRETA: {alternativa_correta.texto}\n"
        f"Alternativa ESCOLHIDA pelo aluno: {alternativa_escolhida.texto}\n"
        "Responda somente com a explicação."
    )
    try:
        resposta = httpx.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": modelo,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
                "temperature": 0.4,
            },
            timeout=_TIMEOUT_SEGUNDOS,
        )
        resposta.raise_for_status()
        conteudo = resposta.json()["choices"][0]["message"]["content"]
        return conteudo.strip() or None
    except Exception:  # noqa: BLE001 — qualquer falha cai no fallback (regra da história #6)
        return None


def _texto_fallback(questao, alternativa_correta, alternativa_escolhida) -> str:
    """Explicação determinística construída com os dados do banco (sem IA)."""
    assunto = questao.assunto
    return (
        f"Você marcou \"{alternativa_escolhida.texto}\", mas a alternativa correta é "
        f"\"{alternativa_correta.texto}\". Revise o conteúdo de "
        f"\"{assunto.nome}\" (matéria {assunto.materia.nome}) — releia o enunciado "
        f"comparando as duas alternativas para identificar o detalhe que fez a diferença."
    )


def gerar_explicacao(questao, alternativa_correta, alternativa_escolhida) -> str:
    """Nunca falha: IA se disponível, fallback determinístico caso contrário."""
    return (
        _texto_via_ia(questao, alternativa_correta, alternativa_escolhida)
        or _texto_fallback(questao, alternativa_correta, alternativa_escolhida)
    )
