"""CT11–CT12 do plano de testes — histórias #8 e #9 (Sprint 3).

- CT11: histórico — tentativas de SIMULADOS DIFERENTES aparecem com seus
  resultados, associadas ao aluno autenticado (nada vaza para outro aluno).
- CT12: dashboard — agregação por matéria e assunto com JOIN/GROUP BY.

Os casos de IA da Sprint 3 (história #7) são cobertos pelos testes de
contrato do grupo em `test_ia_contract.py` (provedor injetado, 503 quando
indisponível, correção objetiva preservada).

O seed cria 1 simulado com 2 questões:
  q1 (Porcentagem/Matemática): alternativas [10(errada), 30(CORRETA), 35]
  q2 (Interpretação/L. Portuguesa): [info central(CORRETA), maior palavra, opinião]
"""
from app.database import SessionLocal
from app.models import Simulado, simulado_questao


# ---------- helpers ----------

def _simulado_id(client, headers) -> int:
    return client.get("/simulados", headers=headers).json()[0]["id"]


def _iniciar(client, headers, simulado_id) -> dict:
    resposta = client.post("/tentativas", json={"simulado_id": simulado_id}, headers=headers)
    assert resposta.status_code == 201
    return resposta.json()


def _responder(client, headers, tentativa_id, questao_id, alternativa_id):
    return client.post(
        f"/tentativas/{tentativa_id}/respostas",
        json={"questao_id": questao_id, "alternativa_id": alternativa_id},
        headers=headers,
    )


def _criar_simulado_extra(questao_id: int, titulo: str) -> int:
    """Cria um 2º simulado direto no banco (o CRUD administrativo de
    simulados é coberto pelos testes do grupo em test_admin_simulados.py)."""
    db = SessionLocal()
    try:
        simulado = Simulado(titulo=titulo, descricao="Criado no teste.")
        db.add(simulado)
        db.commit()
        db.execute(
            simulado_questao.insert(),
            [{"simulado_id": simulado.id, "questao_id": questao_id, "ordem": 1}],
        )
        db.commit()
        return simulado.id
    finally:
        db.close()


def _fluxo_finalizado(client, headers, simulado_id, escolhas):
    """Inicia, responde (índice da alternativa em cada questão) e finaliza."""
    tentativa = _iniciar(client, headers, simulado_id)
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=headers).json()
    for questao, indice in zip(jogo, escolhas):
        resposta = _responder(
            client, headers, tentativa["id"], questao["id"], questao["alternativas"][indice]["id"]
        )
        assert resposta.status_code == 200
    finalizado = client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=headers)
    assert finalizado.status_code == 200, finalizado.text
    return tentativa["id"], finalizado.json()


# ---------- CT11: histórico ----------

def test_ct11_historico_com_diferentes_simulados(client, aluno_headers):
    # tentativa 1: simulado do seed, 1 acerto / 1 erro (50%)
    simulado1 = _simulado_id(client, aluno_headers)
    _, correcao1 = _fluxo_finalizado(client, aluno_headers, simulado1, [0, 0])

    # tentativa 2: outro simulado (só a q1), acertando (100%)
    jogo = client.get(f"/tentativas/{correcao1['tentativa']['id']}/questoes", headers=aluno_headers).json()
    q1_id = jogo[0]["id"]
    simulado2 = _criar_simulado_extra(q1_id, "Simulado de reforço — Matemática")
    _, correcao2 = _fluxo_finalizado(client, aluno_headers, simulado2, [1])

    historico = client.get("/tentativas", headers=aluno_headers).json()
    assert len(historico) == 2
    por_simulado = {t["simulado_id"]: t for t in historico}
    assert por_simulado[simulado1]["acertos"] == 1 and por_simulado[simulado1]["percentual_aproveitamento"] == 50.0
    assert por_simulado[simulado2]["acertos"] == 1 and por_simulado[simulado2]["percentual_aproveitamento"] == 100.0
    assert all(t["status"] == "FINALIZADO" for t in historico)

    # dados associados ao aluno autenticado: outro aluno não vê nada
    registro = client.post(
        "/auth/register",
        json={"nome": "Bruno Aluno", "email": "bruno.aluno@simulaai.app", "senha": "senha12345"},
    )
    assert registro.status_code in (200, 201)
    login = client.post(
        "/auth/login", json={"email": "bruno.aluno@simulaai.app", "senha": "senha12345"}
    )
    outros_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    assert client.get("/tentativas", headers=outros_headers).json() == []
    intruso = client.get(f"/tentativas/{correcao1['tentativa']['id']}", headers=outros_headers)
    assert intruso.status_code == 403


# ---------- CT12: dashboard agregado ----------

def test_ct12_dashboard_agrega_por_materia_e_assunto(client, aluno_headers, admin_headers):
    simulado1 = _simulado_id(client, aluno_headers)
    _fluxo_finalizado(client, aluno_headers, simulado1, [0, 0])  # 50%: acertou q2, errou q1

    jogo = client.get("/tentativas/1/questoes", headers=aluno_headers).json()
    q1_id = jogo[0]["id"]
    simulado2 = _criar_simulado_extra(q1_id, "Simulado de reforço — Matemática")
    _fluxo_finalizado(client, aluno_headers, simulado2, [1])  # 100% na q1

    resposta = client.get("/dashboard", headers=aluno_headers)
    assert resposta.status_code == 200
    painel = resposta.json()

    assert painel["total_tentativas"] == 2
    assert painel["tentativas_finalizadas"] == 2
    assert painel["total_acertos"] == 2
    assert painel["total_erros"] == 1
    assert painel["media_aproveitamento"] == 75.0

    por_materia = {linha["rotulo"]: linha for linha in painel["por_materia"]}
    # Matemática: q1 respondida 2× (1ª errada, 2ª correta) → 1 acerto, 1 erro, 50%
    assert por_materia["Matemática"] == {
        "rotulo": "Matemática", "respondidas": 2, "acertos": 1, "erros": 1, "percentual": 50.0,
    }
    # Língua Portuguesa: q2 respondida 1× e correta → 100%
    assert por_materia["Língua Portuguesa"] == {
        "rotulo": "Língua Portuguesa", "respondidas": 1, "acertos": 1, "erros": 0, "percentual": 100.0,
    }

    por_assunto = {linha["rotulo"]: linha for linha in painel["por_assunto"]}
    assert por_assunto["Porcentagem"]["respondidas"] == 2
    assert por_assunto["Porcentagem"]["acertos"] == 1
    assert por_assunto["Interpretação de texto"]["respondidas"] == 1
    assert por_assunto["Interpretação de texto"]["acertos"] == 1

    # admin não tem dashboard de aluno (funcionalidade do perfil ALUNO)
    assert client.get("/dashboard", headers=admin_headers).status_code == 403

    # sem tentativas finalizadas, o painel volta zerado (não quebra)
    registro = client.post(
        "/auth/register",
        json={"nome": "Carla Aluna", "email": "carla.aluno@simulaai.app", "senha": "senha12345"},
    )
    assert registro.status_code in (200, 201)
    login = client.post(
        "/auth/login", json={"email": "carla.aluno@simulaai.app", "senha": "senha12345"}
    )
    headers_zerado = {"Authorization": f"Bearer {login.json()['access_token']}"}
    painel_zerado = client.get("/dashboard", headers=headers_zerado).json()
    assert painel_zerado["total_tentativas"] == 0
    assert painel_zerado["por_materia"] == []
