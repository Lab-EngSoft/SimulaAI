"""Conexão com o banco de dados.

O endereço do banco vem da variável de ambiente DATABASE_URL (ver .env.example):
- Desenvolvimento local (padrão): sqlite:///./simulaai.db — não precisa instalar servidor.
- Produção: postgresql://... (Supabase), conforme o Termo de Aceite (E2b).
- Testes: "sqlite://" = banco em memória, descartado ao fim de cada teste.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./simulaai.db")

_MEMORIA = DATABASE_URL in ("sqlite://", "sqlite:///:memory:", "sqlite")

if _MEMORIA:
    # Banco em memória: uma única conexão compartilhada (senão cada sessão
    # criaria um banco vazio diferente).
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
elif DATABASE_URL.startswith("sqlite"):
    # SQLite em arquivo (desenvolvimento local).
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL/Supabase (produção).
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependência do FastAPI: abre uma sessão por requisição e fecha ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
