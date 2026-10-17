"""Protege bancos de questões e tentativas contra exclusões em cascata."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Assunto, Questao, Tentativa, simulado_questao


def questao_usada_em_simulado(db: Session, questao_id: int) -> bool:
    return db.scalar(
        select(simulado_questao.c.simulado_id)
        .where(simulado_questao.c.questao_id == questao_id).limit(1)
    ) is not None


def questao_com_tentativas(db: Session, questao_id: int) -> bool:
    return db.scalar(
        select(Tentativa.id)
        .join(simulado_questao, Tentativa.simulado_id == simulado_questao.c.simulado_id)
        .where(simulado_questao.c.questao_id == questao_id).limit(1)
    ) is not None


def assunto_usado_em_simulado(db: Session, assunto_id: int) -> bool:
    return db.scalar(
        select(Questao.id)
        .join(simulado_questao, Questao.id == simulado_questao.c.questao_id)
        .where(Questao.assunto_id == assunto_id).limit(1)
    ) is not None


def materia_usada_em_simulado(db: Session, materia_id: int) -> bool:
    return db.scalar(
        select(Questao.id)
        .join(Assunto, Questao.assunto_id == Assunto.id)
        .join(simulado_questao, Questao.id == simulado_questao.c.questao_id)
        .where(Assunto.materia_id == materia_id).limit(1)
    ) is not None
