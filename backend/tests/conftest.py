"""Fixture compartilhada dos testes.

Banco em memória ("sqlite://"): rápido e dispensa servidor — cada teste
começa com tabelas limpas e o mesmo seed da demonstração.
"""
import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ.setdefault("SECRET_KEY", "chave-de-teste-simulaai-usada-apenas-no-pytest")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

ADMIN = {"email": "carlos.admin@simulaai.app", "senha": "admin123"}
ALUNO = {"email": "ana.aluno@simulaai.app", "senha": "aluno123"}


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:  # o startup semeia os dados de demonstração
        yield c


def _login(client, credenciais):
    resposta = client.post("/auth/login", json=credenciais)
    assert resposta.status_code == 200, f"login falhou: {resposta.text}"
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}


@pytest.fixture()
def admin_headers(client):
    return _login(client, ADMIN)


@pytest.fixture()
def aluno_headers(client):
    return _login(client, ALUNO)
