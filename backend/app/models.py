"""Modelos ORM — espelham as tabelas do E3/schema.sql.

Cada classe abaixo corresponde a uma tabela do banco modelado na E3:
usuario, materia, assunto, questao, alternativa, simulado, simulado_questao,
tentativa e resposta. Os nomes de tabelas e colunas são os mesmos do DDL,
para manter a rastreabilidade modelo -> código exigida na rubrica.
"""
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


def agora_utc() -> datetime:
    """Timestamp UTC com fuso (datetime.utcnow está obsoleto no Python 3.12)."""
    return datetime.now(timezone.utc)

# Tabela associativa do relacionamento N:N Simulado <-> Questão (E3)
simulado_questao = Table(
    "simulado_questao",
    Base.metadata,
    Column("simulado_id", Integer, ForeignKey("simulado.id", ondelete="CASCADE"), primary_key=True),
    Column("questao_id", Integer, ForeignKey("questao.id", ondelete="CASCADE"), primary_key=True),
    Column("ordem", Integer, nullable=False),
)


class Usuario(Base):
    """História #1 — perfis ALUNO e ADMINISTRADOR."""

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(50), nullable=False)  # 'ALUNO' | 'ADMINISTRADOR'
    criado_em = Column(DateTime, default=agora_utc)

    tentativas = relationship("Tentativa", back_populates="usuario", cascade="all, delete-orphan")


class Materia(Base):
    """História #2 — cadastro de matérias."""

    __tablename__ = "materia"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)

    assuntos = relationship("Assunto", back_populates="materia", cascade="all, delete-orphan")


class Assunto(Base):
    """História #2 — assuntos vinculados a uma matéria."""

    __tablename__ = "assunto"

    id = Column(Integer, primary_key=True)
    materia_id = Column(Integer, ForeignKey("materia.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)

    materia = relationship("Materia", back_populates="assuntos")
    questoes = relationship("Questao", back_populates="assunto", cascade="all, delete-orphan")


class Questao(Base):
    """História #3 — questões objetivas de múltipla escolha."""

    __tablename__ = "questao"

    id = Column(Integer, primary_key=True)
    assunto_id = Column(Integer, ForeignKey("assunto.id", ondelete="CASCADE"), nullable=False)
    enunciado = Column(Text, nullable=False)
    nivel_dificuldade = Column(String(30), nullable=True)

    assunto = relationship("Assunto", back_populates="questoes")
    alternativas = relationship(
        "Alternativa", back_populates="questao", cascade="all, delete-orphan"
    )
    simulados = relationship(
        "Simulado", secondary=simulado_questao, back_populates="questoes"
    )


class Alternativa(Base):
    """História #3 — alternativas; a regra 'exatamente uma correta'
    é validada no endpoint (CT04) porque o banco só garante NOT NULL/DEFAULT."""

    __tablename__ = "alternativa"

    id = Column(Integer, primary_key=True)
    questao_id = Column(Integer, ForeignKey("questao.id", ondelete="CASCADE"), nullable=False)
    texto = Column(Text, nullable=False)
    correta = Column(Boolean, nullable=False, default=False)

    questao = relationship("Questao", back_populates="alternativas")


class Simulado(Base):
    """História #4 (Sprint 2) — estrutura de um simulado."""

    __tablename__ = "simulado"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=agora_utc)

    questoes = relationship("Questao", secondary=simulado_questao, back_populates="simulados")
    tentativas = relationship("Tentativa", back_populates="simulado", cascade="all, delete-orphan")


class Tentativa(Base):
    """Histórias #4–#6 e #8–#10 — registro de um simulado feito pelo aluno."""

    __tablename__ = "tentativa"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    simulado_id = Column(Integer, ForeignKey("simulado.id", ondelete="CASCADE"), nullable=False)
    data_inicio = Column(DateTime, default=agora_utc)
    data_fim = Column(DateTime, nullable=True)
    acertos = Column(Integer, nullable=False, default=0)
    erros = Column(Integer, nullable=False, default=0)
    percentual_aproveitamento = Column(Numeric(5, 2), nullable=False, default=0)
    status = Column(String(30), nullable=False, default="EM_ANDAMENTO")

    usuario = relationship("Usuario", back_populates="tentativas")
    simulado = relationship("Simulado", back_populates="tentativas")
    respostas = relationship("Resposta", back_populates="tentativa", cascade="all, delete-orphan")


class Resposta(Base):
    """Histórias #5–#7 — resposta escolhida e explicação da IA (Sprint 3)."""

    __tablename__ = "resposta"

    id = Column(Integer, primary_key=True)
    tentativa_id = Column(Integer, ForeignKey("tentativa.id", ondelete="CASCADE"), nullable=False)
    questao_id = Column(Integer, ForeignKey("questao.id", ondelete="CASCADE"), nullable=False)
    alternativa_id = Column(Integer, ForeignKey("alternativa.id", ondelete="CASCADE"), nullable=False)
    correta = Column(Boolean, nullable=False)
    explicacao_ia = Column(Text, nullable=True)

    tentativa = relationship("Tentativa", back_populates="respostas")
