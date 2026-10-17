"""Preparação de IA desacoplada da nota, sem dependência de serviço externo."""


def _tentativa_errada(client, aluno_headers, admin_headers):
    sid = client.get('/simulados', headers=aluno_headers).json()[0]['id']
    attempt = client.post('/tentativas', headers=aluno_headers, json={'simulado_id': sid}).json()
    jogo = client.get(f"/tentativas/{attempt['id']}/questoes", headers=aluno_headers).json()
    questao = client.get(f"/questoes/{jogo[0]['id']}", headers=admin_headers).json()
    errada = next(a['id'] for a in questao['alternativas'] if not a['correta'])
    client.post(f"/tentativas/{attempt['id']}/respostas", headers=aluno_headers, json={
        'questao_id': jogo[0]['id'], 'alternativa_id': errada,
    })
    return attempt['id']


def test_status_indisponivel_e_endpoint_nao_modifica_nota(client, aluno_headers, admin_headers):
    r = client.get('/tentativas/ia/status', headers=aluno_headers)
    assert r.status_code == 200, r.text
    assert r.json()['disponivel'] is False
    tid = _tentativa_errada(client, aluno_headers, admin_headers)
    assert client.post(f'/tentativas/{tid}/explicacoes', headers=aluno_headers).status_code == 409
    final = client.post(f'/tentativas/{tid}/finalizar', headers=aluno_headers)
    assert final.status_code == 200
    nota = final.json()['tentativa']['percentual_aproveitamento']
    assert client.post(f'/tentativas/{tid}/explicacoes', headers=aluno_headers).status_code == 503
    mesmo = client.get(f'/tentativas/{tid}/resultado', headers=aluno_headers)
    assert mesmo.status_code == 200
    assert mesmo.json()['tentativa']['percentual_aproveitamento'] == nota
    assert all(r['explicacao_ia'] is None for r in mesmo.json()['respostas'])


def test_injecao_de_provedor_persiste_explicacao(client, aluno_headers, admin_headers, monkeypatch):
    from app.routers import tentativas
    tid = _tentativa_errada(client, aluno_headers, admin_headers)
    client.post(f'/tentativas/{tid}/finalizar', headers=aluno_headers)
    contexts = []

    class ProvedorFalso:
        def explicar(self, contexto):
            contexts.append(contexto)
            return 'A solução usa o conteúdo do enunciado.'

    monkeypatch.setattr(tentativas, 'obter_provedor', lambda: ProvedorFalso())
    saida = client.post(f'/tentativas/{tid}/explicacoes', headers=aluno_headers)
    assert saida.status_code == 200, saida.text
    assert len(contexts) == 1
    assert contexts[0].resposta_aluno != contexts[0].resposta_correta
    assert any(r['explicacao_ia'] for r in saida.json()['respostas'])
    # Idempotência — o que já foi explicado não gera outra requisição externa.
    assert client.post(f'/tentativas/{tid}/explicacoes', headers=aluno_headers).status_code == 200
    assert len(contexts) == 1


def test_resultado_protegido_antes_e_depois(client, aluno_headers, admin_headers):
    tid = _tentativa_errada(client, aluno_headers, admin_headers)
    assert client.get(f'/tentativas/{tid}/resultado', headers=aluno_headers).status_code == 409
    assert client.get(f'/tentativas/{tid}/resultado').status_code == 401
    client.post(f'/tentativas/{tid}/finalizar', headers=aluno_headers)
    assert client.get(f'/tentativas/{tid}/resultado', headers=aluno_headers).status_code == 200
