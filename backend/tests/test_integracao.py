"""Regressões de integração da interface (CRUD + autorização)."""

def test_aluno_nao_recebe_gabarito_administrativo(client, aluno_headers, admin_headers):
    assert client.get("/questoes", headers=aluno_headers).status_code == 403
    primeira = client.get("/questoes", headers=admin_headers).json()[0]
    assert client.get(f"/questoes/{primeira['id']}", headers=aluno_headers).status_code == 403


def test_edicao_de_questao_troca_assunto(client, admin_headers):
    assuntos = client.get("/assuntos", headers=admin_headers).json()
    assert len(assuntos) >= 2
    questao = client.get("/questoes", headers=admin_headers).json()[0]
    destino = next(a["id"] for a in assuntos if a["id"] != questao["assunto_id"])
    resposta = client.put(f"/questoes/{questao['id']}", json={"assunto_id": destino}, headers=admin_headers)
    assert resposta.status_code == 200
    assert resposta.json()["assunto_id"] == destino
    assert client.put(f"/questoes/{questao['id']}", json={"assunto_id": 999999}, headers=admin_headers).status_code == 404
    assert client.get(f"/questoes/{questao['id']}", headers=admin_headers).json()["assunto_id"] == destino


def test_fluxo_real_admin_aluno_e_persistencia_http(client, admin_headers, aluno_headers):
    """Contrato consumido pelo frontend: CRUD admin + aluno e correção no banco."""
    assert client.post('/auth/login', json={'email': 'ana.aluno@simulaai.app', 'senha': 'senha-errada'}).status_code == 401
    materia = client.post('/materias', headers=admin_headers, json={'nome': 'Ciências Integradas', 'descricao': 'Para teste'}).json()
    assert materia['id']
    assunto = client.post('/assuntos', headers=admin_headers, json={'materia_id': materia['id'], 'nome': 'Energia', 'descricao': None}).json()
    questao = client.post('/questoes', headers=admin_headers, json={
        'assunto_id': assunto['id'], 'enunciado': 'Qual é a unidade de energia no SI?',
        'nivel_dificuldade': 'Fácil',
        'alternativas': [{'texto': 'Joule', 'correta': True}, {'texto': 'Metro', 'correta': False}],
    })
    assert questao.status_code == 201
    id_questao = questao.json()['id']
    atualizado = client.put(f'/questoes/{id_questao}', headers=admin_headers, json={'enunciado': 'Unidade de energia?'}).json()
    assert atualizado['enunciado'] == 'Unidade de energia?'
    assert client.get('/materias', headers=admin_headers).json()
    assert client.get('/assuntos', headers=admin_headers).json()
    assert any(q['id'] == id_questao for q in client.get('/questoes', headers=admin_headers).json())
    assert client.post('/materias', headers=aluno_headers, json={'nome': 'Ataque'}).status_code == 403

    simulado = client.get('/simulados', headers=aluno_headers).json()[0]
    tentativa = client.post('/tentativas', headers=aluno_headers, json={'simulado_id': simulado['id']})
    assert tentativa.status_code == 201
    id_tentativa = tentativa.json()['id']
    jogo = client.get(f'/tentativas/{id_tentativa}/questoes', headers=aluno_headers).json()
    assert jogo
    assert not any('correta' in alternativa for q in jogo for alternativa in q['alternativas'])
    assert client.post(f'/tentativas/{id_tentativa}/respostas', headers=aluno_headers,
                       json={'questao_id': jogo[0]['id'], 'alternativa_id': jogo[0]['alternativas'][0]['id']}).status_code == 200
    continuacao = client.get(f'/tentativas/{id_tentativa}/questoes', headers=aluno_headers).json()
    assert continuacao[0]['respondida_alternativa_id'] == jogo[0]['alternativas'][0]['id']
    resultado = client.post(f'/tentativas/{id_tentativa}/finalizar', headers=aluno_headers)
    assert resultado.status_code == 200
    assert resultado.json()['tentativa']['status'] == 'FINALIZADO'
    historico = client.get('/tentativas', headers=aluno_headers).json()
    assert any(t['id'] == id_tentativa and t['status'] == 'FINALIZADO' for t in historico)
