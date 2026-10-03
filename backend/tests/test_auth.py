"""CT01 e CT02 do plano de testes — autenticação e autorização (história #1)."""

ADMIN = {"email": "carlos.admin@simulaai.app", "senha": "admin123"}
ALUNO = {"email": "ana.aluno@simulaai.app", "senha": "aluno123"}


def test_ct01_login_valido_devolve_token_e_perfil_correto(client):
    """CT01: credenciais válidas -> acesso concedido com o perfil certo."""
    admin = client.post("/auth/login", json=ADMIN)
    assert admin.status_code == 200
    corpo = admin.json()
    assert corpo["access_token"]
    assert corpo["token_type"] == "bearer"
    assert corpo["usuario"]["perfil"] == "ADMINISTRADOR"

    aluno = client.post("/auth/login", json=ALUNO)
    assert aluno.status_code == 200
    assert aluno.json()["usuario"]["perfil"] == "ALUNO"


def test_ct01_login_com_senha_errada_e_recusado(client):
    resposta = client.post("/auth/login", json={"email": ALUNO["email"], "senha": "senha-errada"})
    assert resposta.status_code == 401


def test_ct02_aluno_nao_acessa_rota_administrativa(client, aluno_headers):
    """CT02: aluno em rota de admin -> 403, validado no backend."""
    resposta = client.post("/materias", json={"nome": "Biologia"}, headers=aluno_headers)
    assert resposta.status_code == 403
    assert "ADMINISTRADOR" in resposta.json()["detail"]


def test_ct02_sem_token_e_recusado(client):
    resposta = client.post("/materias", json={"nome": "Biologia"})
    assert resposta.status_code == 401


def test_ct02_aluno_le_dados_mas_nao_escreve(client, aluno_headers):
    """Aluno pode LER matérias (vai usar no simulado), mas não criar."""
    leitura = client.get("/materias", headers=aluno_headers)
    assert leitura.status_code == 200
    assert any(m["nome"] == "Matemática" for m in leitura.json())


def test_registro_cria_aluno_que_consegue_logar(client):
    novo = {"nome": "Novo Aluno", "email": "novo.aluno@exemplo.com", "senha": "senha12345"}
    criado = client.post("/auth/register", json=novo)
    assert criado.status_code == 201
    assert criado.json()["perfil"] == "ALUNO"

    login = client.post(
        "/auth/login", json={"email": novo["email"], "senha": novo["senha"]}
    )
    assert login.status_code == 200


def test_registro_com_email_duplicado_e_recusado(client):
    duplicado = {"nome": "Outra Pessoa", "email": ALUNO["email"], "senha": "senha12345"}
    resposta = client.post("/auth/register", json=duplicado)
    assert resposta.status_code == 409


def test_me_devolve_usuario_logado(client, aluno_headers):
    resposta = client.get("/auth/me", headers=aluno_headers)
    assert resposta.status_code == 200
    assert resposta.json()["email"] == ALUNO["email"]
