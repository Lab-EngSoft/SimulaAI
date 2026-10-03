"""CT03 do plano de testes — campos obrigatórios (história #2)."""


def _criar_materia(client, headers, nome="História", descricao=None):
    return client.post("/materias", json={"nome": nome, "descricao": descricao}, headers=headers)


def _criar_assunto(client, headers, materia_id, nome="Revolução Francesa"):
    return client.post(
        "/assuntos", json={"materia_id": materia_id, "nome": nome}, headers=headers
    )


def test_ct03_materia_sem_nome_e_recusada(client, admin_headers):
    """CT03: nome vazio -> interface da API recusa (422), nunca chega ao banco."""
    resposta = client.post("/materias", json={"nome": ""}, headers=admin_headers)
    assert resposta.status_code == 422


def test_ct03_assunto_sem_nome_e_recusado(client, admin_headers):
    materia = _criar_materia(client, admin_headers, nome="História-CT03")
    assert materia.status_code == 201
    resposta = _criar_assunto(client, admin_headers, materia.json()["id"], nome="")
    assert resposta.status_code == 422


def test_crud_materia_completo(client, admin_headers):
    criada = _criar_materia(client, admin_headers, nome="Geografia", descricao="desc")
    assert criada.status_code == 201
    materia_id = criada.json()["id"]

    lista = client.get("/materias", headers=admin_headers)
    assert any(m["id"] == materia_id for m in lista.json())

    detalhe = client.get(f"/materias/{materia_id}", headers=admin_headers)
    assert detalhe.status_code == 200
    assert detalhe.json()["assuntos"] == []  # recém-criada, sem assuntos

    atualizada = client.put(
        f"/materias/{materia_id}", json={"nome": "Geografia Física"}, headers=admin_headers
    )
    assert atualizada.status_code == 200
    assert atualizada.json()["nome"] == "Geografia Física"

    duplicada = _criar_materia(client, admin_headers, nome="Geografia Física")
    assert duplicada.status_code == 409

    removida = client.delete(f"/materias/{materia_id}", headers=admin_headers)
    assert removida.status_code == 204
    assert client.get(f"/materias/{materia_id}", headers=admin_headers).status_code == 404


def test_assunto_em_materia_inexistente_e_recusado(client, admin_headers):
    resposta = _criar_assunto(client, admin_headers, materia_id=999999)
    assert resposta.status_code == 404


def test_deletar_materia_leva_assuntos_juntos(client, admin_headers):
    """ON DELETE CASCADE (E3): assuntos da matéria somem com ela."""
    materia = _criar_materia(client, admin_headers, nome="Filosofia").json()
    _criar_assunto(client, admin_headers, materia["id"], nome="Lógica")

    client.delete(f"/materias/{materia['id']}", headers=admin_headers)
    assuntos = client.get(f"/assuntos?materia_id={materia['id']}", headers=admin_headers)
    assert assuntos.json() == []
