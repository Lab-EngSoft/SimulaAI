"""Operações administrativas de simulados, permissão e consistência histórica."""


def _questoes(client, headers):
    return [q["id"] for q in client.get('/questoes', headers=headers).json()]


def test_admin_cria_simulado_ordenado_e_aluno_responde(client, admin_headers, aluno_headers):
    ids = _questoes(client, admin_headers)
    payload = {"titulo": "Revisão criada pelo admin", "descricao": "Teste integração", "questao_ids": ids[::-1]}
    criado = client.post('/simulados', json=payload, headers=admin_headers)
    assert criado.status_code == 201, criado.text
    data = criado.json()
    assert data["questao_ids"] == ids[::-1]
    assert data["total_questoes"] == len(ids)
    assert data["total_tentativas"] == 0

    lista = client.get('/simulados', headers=aluno_headers)
    assert lista.status_code == 200
    assert any(s['id'] == data['id'] for s in lista.json())
    assert 'questao_ids' not in next(s for s in lista.json() if s['id'] == data['id'])
    assert client.get(f"/simulados/{data['id']}", headers=aluno_headers).status_code == 403

    tentativa = client.post('/tentativas', json={'simulado_id': data['id']}, headers=aluno_headers)
    assert tentativa.status_code == 201
    jogo = client.get(f"/tentativas/{tentativa.json()['id']}/questoes", headers=aluno_headers).json()
    assert [q['id'] for q in jogo] == ids[::-1]
    assert all('correta' not in alt for q in jogo for alt in q['alternativas'])
    assert client.post(f"/tentativas/{tentativa.json()['id']}/finalizar", headers=aluno_headers).status_code == 200


def test_admin_edita_questoes_e_metadados_antes_de_tentativa(client, admin_headers):
    ids = _questoes(client, admin_headers)
    criado = client.post('/simulados', json={'titulo': 'Meu simulado', 'questao_ids': ids}, headers=admin_headers).json()
    resposta = client.put(f"/simulados/{criado['id']}", json={
        'titulo': 'Simulado atualizado', 'descricao': 'Nova descrição', 'questao_ids': ids[::-1]
    }, headers=admin_headers)
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()['questao_ids'] == ids[::-1]
    assert resposta.json()['titulo'] == 'Simulado atualizado'
    assert client.get(f"/simulados/{criado['id']}", headers=admin_headers).json()['questao_ids'] == ids[::-1]


def test_aluno_nao_pode_criar_editar_excluir(client, aluno_headers, admin_headers):
    ids = _questoes(client, admin_headers)
    dados = {'titulo': 'Título válido', 'questao_ids': ids}
    simulado_id = client.get('/simulados', headers=aluno_headers).json()[0]['id']
    assert client.post('/simulados', json=dados, headers=aluno_headers).status_code == 403
    assert client.put(f'/simulados/{simulado_id}', json=dados, headers=aluno_headers).status_code == 403
    assert client.delete(f'/simulados/{simulado_id}', headers=aluno_headers).status_code == 403
    assert client.post('/simulados', json=dados).status_code == 401


def test_admin_valida_payload_duplicado_inexistente_ou_vazio(client, admin_headers):
    ids = _questoes(client, admin_headers)
    for payload in (
        {'titulo': 'Simulado', 'questao_ids': []},
        {'titulo': 'Simulado', 'questao_ids': [ids[0], ids[0]]},
        {'titulo': 'Simulado', 'questao_ids': [999999]},
        {'titulo': 'ab', 'questao_ids': ids},
    ):
        res = client.post('/simulados', json=payload, headers=admin_headers)
        assert res.status_code == 422, res.text


def test_admin_exclui_simulado_sem_tentativas(client, admin_headers):
    ids = _questoes(client, admin_headers)
    sid = client.post('/simulados', json={'titulo': 'Para excluir', 'questao_ids': ids}, headers=admin_headers).json()['id']
    assert client.delete(f'/simulados/{sid}', headers=admin_headers).status_code == 204
    assert client.get(f'/simulados/{sid}', headers=admin_headers).status_code == 404


def test_tentativas_impedem_troca_questoes_e_exclusao(client, admin_headers, aluno_headers):
    ids = _questoes(client, admin_headers)
    sid = client.post('/simulados', json={'titulo': 'Simulado histórico', 'questao_ids': ids}, headers=admin_headers).json()['id']
    tentativa = client.post('/tentativas', json={'simulado_id': sid}, headers=aluno_headers)
    assert tentativa.status_code == 201
    troca = client.put(f'/simulados/{sid}', json={
        'titulo': 'Título novo', 'questao_ids': ids[::-1]
    }, headers=admin_headers)
    assert troca.status_code == 409
    assert client.get(f'/simulados/{sid}', headers=admin_headers).json()['questao_ids'] == ids
    assert client.delete(f'/simulados/{sid}', headers=admin_headers).status_code == 409
    metadados = client.put(f'/simulados/{sid}', json={
        'titulo': 'Título novo', 'descricao': 'Sem alterar questões', 'questao_ids': ids
    }, headers=admin_headers)
    assert metadados.status_code == 200


def test_questao_utilizada_nao_pode_ser_apagada_ou_editar_historico(client, admin_headers, aluno_headers):
    ids = _questoes(client, admin_headers)
    questao = client.get(f'/questoes/{ids[0]}', headers=admin_headers).json()
    # Questão seed já vinculada ao demonstrativo
    assert client.delete(f'/questoes/{ids[0]}', headers=admin_headers).status_code == 409
    sid = client.get('/simulados', headers=aluno_headers).json()[0]['id']
    client.post('/tentativas', json={'simulado_id': sid}, headers=aluno_headers)
    res = client.put(f'/questoes/{ids[0]}', json={
        'enunciado': 'Alteração indevida', 'assunto_id': questao['assunto_id'],
        'alternativas': [{'texto': alt['texto'], 'correta': alt['correta']} for alt in questao['alternativas']],
    }, headers=admin_headers)
    assert res.status_code == 409


def test_materia_e_assunto_com_questao_vinculada_nao_podem_ser_excluidos(client, admin_headers):
    questao = client.get('/questoes', headers=admin_headers).json()[0]
    assunto_id = questao['assunto_id']
    assunto = next(a for a in client.get('/assuntos', headers=admin_headers).json() if a['id'] == assunto_id)
    assert client.delete(f'/assuntos/{assunto_id}', headers=admin_headers).status_code == 409
    assert client.delete(f"/materias/{assunto['materia_id']}", headers=admin_headers).status_code == 409
