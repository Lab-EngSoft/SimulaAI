"""CT04 do plano de testes — exatamente uma alternativa correta (história #3)."""


def _assunto(client, headers):
    materia = client.post("/materias", json={"nome": "Química-CT04"}, headers=headers)
    assunto = client.post(
        "/assuntos",
        json={"materia_id": materia.json()["id"], "nome": "Tabela periódica"},
        headers=headers,
    )
    return assunto.json()["id"]


def _questao(assunto_id, correta_a=False, correta_b=False, correta_c=False):
    return {
        "assunto_id": assunto_id,
        "enunciado": "Qual elemento tem símbolo Fe?",
        "alternativas": [
            {"texto": "Ferro", "correta": correta_a},
            {"texto": "Flúor", "correta": correta_b},
            {"texto": "Fósforo", "correta": correta_c},
        ],
    }


def test_ct04_questao_sem_alternativa_correta_e_recusada(client, admin_headers):
    assunto_id = _assunto(client, admin_headers)
    resposta = client.post("/questoes", json=_questao(assunto_id), headers=admin_headers)
    assert resposta.status_code == 422
    assert "exatamente uma" in resposta.json()["detail"]


def test_ct04_questao_com_duas_corretas_e_recusada(client, admin_headers):
    assunto_id = _assunto(client, admin_headers)
    dados = _questao(assunto_id, correta_a=True, correta_b=True)
    resposta = client.post("/questoes", json=dados, headers=admin_headers)
    assert resposta.status_code == 422


def test_ct04_questao_com_uma_correta_e_criada(client, admin_headers):
    assunto_id = _assunto(client, admin_headers)
    dados = _questao(assunto_id, correta_a=True)
    resposta = client.post("/questoes", json=dados, headers=admin_headers)
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert len(corpo["alternativas"]) == 3
    assert sum(a["correta"] for a in corpo["alternativas"]) == 1


def test_questao_em_assunto_inexistente_e_recusada(client, admin_headers):
    resposta = client.post("/questoes", json=_questao(999999, correta_a=True), headers=admin_headers)
    assert resposta.status_code == 404


def test_atualizar_alternativas_revalida_regra(client, admin_headers):
    """Tentar deixar duas corretas via PUT também é bloqueado."""
    assunto_id = _assunto(client, admin_headers)
    criada = client.post(
        "/questoes", json=_questao(assunto_id, correta_a=True), headers=admin_headers
    ).json()

    update = {
        "alternativas": [
            {"texto": "Ferro", "correta": True},
            {"texto": "Flúor", "correta": True},
        ]
    }
    resposta = client.put(f"/questoes/{criada['id']}", json=update, headers=admin_headers)
    assert resposta.status_code == 422

    update["alternativas"][1]["correta"] = False
    ok = client.put(f"/questoes/{criada['id']}", json=update, headers=admin_headers)
    assert ok.status_code == 200
    assert len(ok.json()["alternativas"]) == 2


def test_deletar_questao_leva_alternativas_juntas(client, admin_headers):
    assunto_id = _assunto(client, admin_headers)
    criada = client.post(
        "/questoes", json=_questao(assunto_id, correta_a=True), headers=admin_headers
    ).json()

    lista_antes = client.get(f"/questoes?assunto_id={assunto_id}", headers=admin_headers).json()
    assert any(q["id"] == criada["id"] for q in lista_antes)

    client.delete(f"/questoes/{criada['id']}", headers=admin_headers)
    lista_depois = client.get(f"/questoes?assunto_id={assunto_id}", headers=admin_headers).json()
    assert all(q["id"] != criada["id"] for q in lista_depois)
