"""CT05–CT08 do plano de testes — fluxo do simulado (histórias #4, #5 e #6).

O seed cria o "Simulado demonstrativo" com 2 questões (3 alternativas cada,
exatamente uma correta) — os testes usam esse simulado.
"""


def _simulado_id(client, headers) -> int:
    lista = client.get("/simulados", headers=headers).json()
    assert lista, "seed deveria ter criado o simulado demonstrativo"
    return lista[0]["id"]


def _correta_e_errada(client, admin_headers, questao_id):
    """Descobre qual alternativa é a correta via API de admin (que enxerga a marcação)."""
    questao = client.get(f"/questoes/{questao_id}", headers=admin_headers).json()
    correta = next(a["id"] for a in questao["alternativas"] if a["correta"])
    errada = next(a["id"] for a in questao["alternativas"] if not a["correta"])
    return correta, errada


def test_ct05_aluno_inicia_simulado_e_questoes_sao_exibidas(client, aluno_headers):
    """CT05: tentativa criada; questões exibidas SEM revelar a correta."""
    simulado_id = _simulado_id(client, aluno_headers)
    resposta = client.post("/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers)
    assert resposta.status_code == 201
    tentativa = resposta.json()
    assert tentativa["status"] == "EM_ANDAMENTO"
    assert tentativa["simulado_id"] == simulado_id

    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    assert len(jogo) == 2
    for questao in jogo:
        assert len(questao["alternativas"]) == 3
        for alternativa in questao["alternativas"]:
            assert "correta" not in alternativa  # a resposta certa não vaza na interface


def test_ct06_resposta_e_persistida_na_tentativa(client, aluno_headers):
    """CT06: a resposta escolhida fica registrada na tentativa correta."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    questao_id = jogo[0]["id"]
    alternativa_id = jogo[0]["alternativas"][1]["id"]

    resposta = client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": questao_id, "alternativa_id": alternativa_id},
        headers=aluno_headers,
    )
    assert resposta.status_code == 200

    jogo_depois = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    respondida = next(q for q in jogo_depois if q["id"] == questao_id)
    assert respondida["respondida_alternativa_id"] == alternativa_id


def test_ct06_responder_de_novo_substitui_a_resposta(client, aluno_headers):
    """Uma única resposta por questão: responder de novo troca a escolha."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    questao_id = jogo[0]["id"]
    primeira = jogo[0]["alternativas"][0]["id"]
    segunda = jogo[0]["alternativas"][2]["id"]

    client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": questao_id, "alternativa_id": primeira},
        headers=aluno_headers,
    )
    client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": questao_id, "alternativa_id": segunda},
        headers=aluno_headers,
    )

    jogo_depois = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    assert next(q for q in jogo_depois if q["id"] == questao_id)["respondida_alternativa_id"] == segunda


def test_ct06_questao_de_fora_do_simulado_e_recusada(client, aluno_headers, admin_headers):
    """Questão que não pertence ao simulado da tentativa -> 422."""
    materia = client.post("/materias", json={"nome": "Física-S2"}, headers=admin_headers).json()
    assunto = client.post(
        "/assuntos", json={"materia_id": materia["id"], "nome": "Cinemática"}, headers=admin_headers
    ).json()
    questao = client.post(
        "/questoes",
        json={
            "assunto_id": assunto["id"],
            "enunciado": "Questão fora do simulado demonstrativo?",
            "alternativas": [{"texto": "2", "correta": True}, {"texto": "3", "correta": False}],
        },
        headers=admin_headers,
    ).json()

    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    resposta = client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": questao["id"], "alternativa_id": questao["alternativas"][0]["id"]},
        headers=aluno_headers,
    )
    assert resposta.status_code == 422


def test_ct06_alternativa_de_outra_questao_e_recusada(client, aluno_headers):
    """A alternativa precisa pertencer à questão respondida -> 422."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    resposta = client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": jogo[0]["id"], "alternativa_id": jogo[1]["alternativas"][0]["id"]},
        headers=aluno_headers,
    )
    assert resposta.status_code == 422


def test_ct07_finalizar_calcula_acertos_erros_e_percentual(client, aluno_headers, admin_headers):
    """CT07: 1 acerto + 1 erro = percentual 50.0 (simulado com 2 questões)."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()

    correta_1, errada_1 = _correta_e_errada(client, admin_headers, jogo[0]["id"])
    correta_2, _ = _correta_e_errada(client, admin_headers, jogo[1]["id"])
    # questao 1: errada; questao 2: correta
    client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": jogo[0]["id"], "alternativa_id": errada_1},
        headers=aluno_headers,
    )
    client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": jogo[1]["id"], "alternativa_id": correta_2},
        headers=aluno_headers,
    )

    final = client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=aluno_headers)
    assert final.status_code == 200
    corpo = final.json()
    assert corpo["tentativa"]["acertos"] == 1
    assert corpo["tentativa"]["erros"] == 1
    assert corpo["tentativa"]["percentual_aproveitamento"] == 50.0
    assert corpo["tentativa"]["status"] == "FINALIZADO"
    assert corpo["tentativa"]["data_fim"]
    # a correção agora REVELA qual alternativa era a correta
    assert len(corpo["respostas"]) == 2
    assert any(r["correta"] for r in corpo["respostas"]) and any(
        not r["correta"] for r in corpo["respostas"]
    )


def test_ct08_finalizar_funciona_sem_servico_de_ia(client, aluno_headers, monkeypatch):
    """CT08: sem nenhuma API de IA configurada, a correção objetiva é concluída
    e o resultado é entregue normalmente (critério de aceite da história #6)."""
    monkeypatch.delenv("AI_API_KEY", raising=False)  # garante: nenhuma IA configurada
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": jogo[0]["id"], "alternativa_id": jogo[0]["alternativas"][0]["id"]},
        headers=aluno_headers,
    )

    final = client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=aluno_headers)
    assert final.status_code == 200
    corpo = final.json()
    assert corpo["tentativa"]["status"] == "FINALIZADO"
    assert corpo["tentativa"]["acertos"] + corpo["tentativa"]["erros"] == 1
    assert all(r["explicacao_ia"] is None for r in corpo["respostas"])


def test_finalizar_sem_respostas_zera_o_resultado(client, aluno_headers):
    """Abandonar o simulado: 0 acertos, 0 erros, percentual 0 — não é erro."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    final = client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=aluno_headers)
    assert final.status_code == 200
    resultado = final.json()["tentativa"]
    assert resultado["acertos"] == 0
    assert resultado["erros"] == 0
    assert resultado["percentual_aproveitamento"] == 0.0


def test_finalizar_duas_vezes_e_recusado(client, aluno_headers):
    """Tentativa já finalizada não pode ser finalizada de novo -> 409."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    assert client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=aluno_headers).status_code == 200
    assert client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=aluno_headers).status_code == 409


def test_responder_apos_finalizar_e_recusado(client, aluno_headers):
    """Não aceita resposta em tentativa finalizada -> 409."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()
    jogo = client.get(f"/tentativas/{tentativa['id']}/questoes", headers=aluno_headers).json()
    client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=aluno_headers)
    resposta = client.post(
        f"/tentativas/{tentativa['id']}/respostas",
        json={"questao_id": jogo[0]["id"], "alternativa_id": jogo[0]["alternativas"][0]["id"]},
        headers=aluno_headers,
    )
    assert resposta.status_code == 409


def test_tentativa_de_outro_aluno_e_bloqueada(client, aluno_headers):
    """Dados de um aluno não vazam para outro (base da história #8) -> 403."""
    simulado_id = _simulado_id(client, aluno_headers)
    tentativa = client.post(
        "/tentativas", json={"simulado_id": simulado_id}, headers=aluno_headers
    ).json()

    novo = {"nome": "Outro Aluno", "email": "outro.s2@exemplo.com", "senha": "senha12345"}
    client.post("/auth/register", json=novo)
    token = client.post(
        "/auth/login", json={"email": novo["email"], "senha": novo["senha"]}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get(f"/tentativas/{tentativa['id']}", headers=headers).status_code == 403
    assert client.get(f"/tentativas/{tentativa['id']}/questoes", headers=headers).status_code == 403
    assert client.post(f"/tentativas/{tentativa['id']}/finalizar", headers=headers).status_code == 403


def test_admin_nao_inicia_tentativa(client, admin_headers):
    """O fluxo do simulado é do perfil ALUNO; admin recebe 403."""
    resposta = client.post("/tentativas", json={"simulado_id": 1}, headers=admin_headers)
    assert resposta.status_code == 403
