"""CT13–CT14 do plano de testes — história #10 (evolução entre tentativas, Sprint 4).

- CT13: a evolução lista as tentativas FINALIZADAS em ordem cronológica,
  cada uma com seu simulado, e calcula a variação em pontos percentuais
  entre elas (critério: comparar desempenho entre diferentes simulados,
  com base nos resultados registrados pelo sistema). Tentativa em andamento
  NÃO entra na linha do tempo.
- CT14: isolamento por aluno (outro aluno vê "sem_dados") e admin recebe 403.

Seed: simulado demonstrativo com q1 (Porcentagem) e q2 (Interpretação).
  q1 alternativas: [10(errada), 30(CORRETA), 35]  → índice da correta = 1
  q2 alternativas: [info central(CORRETA), ...]   → índice da correta = 0
"""
from test_sprint3 import _criar_simulado_extra, _fluxo_finalizado, _simulado_id


def _registrar_e_logar(client, nome, email, senha):
    registro = client.post(
        "/auth/register", json={"nome": nome, "email": email, "senha": senha}
    )
    assert registro.status_code in (200, 201)
    login = client.post("/auth/login", json={"email": email, "senha": senha})
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def _questoes_ids(client, headers, simulado_id):
    from test_sprint3 import _iniciar

    tentativa = _iniciar(client, headers, simulado_id)
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=headers).json()
    return jogo[0]["id"], jogo[1]["id"], tentativa["id"]


def test_ct13_evolucao_cronologica_com_variacao(client, aluno_headers):
    simulado_seed = _simulado_id(client, aluno_headers)
    q1_id, q2_id, _ = _questoes_ids(client, aluno_headers, simulado_seed)

    simulado_q1 = _criar_simulado_extra(q1_id, "Reforço — Porcentagem")
    simulado_q2 = _criar_simulado_extra(q2_id, "Reforço — Interpretação")

    # 3 simulados diferentes, em ordem: 0%, 50%, 100%
    _fluxo_finalizado(client, aluno_headers, simulado_q1, [0])          # q1 errada → 0%
    _fluxo_finalizado(client, aluno_headers, simulado_seed, [0, 0])     # 1 acerto de 2 → 50%
    _fluxo_finalizado(client, aluno_headers, simulado_q2, [0])          # q2 certa → 100%

    # uma tentativa em andamento NÃO pode aparecer na evolução
    from test_sprint3 import _iniciar
    _iniciar(client, aluno_headers, simulado_seed)

    resposta = client.get("/dashboard/evolucao", headers=aluno_headers)
    assert resposta.status_code == 200
    evolucao = resposta.json()

    assert evolucao["total_finalizadas"] == 3
    percentuais = [item["percentual"] for item in evolucao["itens"]]
    assert percentuais == [0.0, 50.0, 100.0]  # ordem cronológica
    assert [i["variacao_vs_anterior"] for i in evolucao["itens"]] == [None, 50.0, 50.0]
    assert evolucao["variacao_total"] == 100.0
    assert evolucao["tendencia"] == "melhorando"
    # cada item identifica o simulado (comparação entre simulados diferentes)
    assert [i["simulado_id"] for i in evolucao["itens"]] == [simulado_q1, simulado_seed, simulado_q2]
    assert all(i["simulado_titulo"] for i in evolucao["itens"])


def test_ct14_evolucao_isolada_por_aluno_e_bloqueada_para_admin(client, aluno_headers, admin_headers):
    simulado_seed = _simulado_id(client, aluno_headers)
    _fluxo_finalizado(client, aluno_headers, simulado_seed, [0, 0])  # 50%

    # admin não tem dashboard de aluno
    assert client.get("/dashboard/evolucao", headers=admin_headers).status_code == 403

    # outro aluno não vê os dados do primeiro
    outros = _registrar_e_logar(client, "Bruno Aluno", "bruno.aluno@simulaai.app", "senha12345")
    resposta = client.get("/dashboard/evolucao", headers=outros)
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total_finalizadas"] == 0
    assert corpo["itens"] == []
    assert corpo["tendencia"] == "sem_dados"
    assert corpo["variacao_total"] is None
