"""Rotas de assuntos — história #2 (assuntos vinculados a uma matéria).

Validações: matéria precisa existir (404) e nome é obrigatório (422 — CT03).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_admin
from app.models import Assunto, Materia
from app.schemas import AssuntoIn, AssuntoOut

router = APIRouter(prefix="/assuntos", tags=["Assuntos"])


def _obter_ou_404(db: Session, assunto_id: int) -> Assunto:
    assunto = db.get(Assunto, assunto_id)
    if assunto is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Assunto não encontrado.")
    return assunto


@router.post("", response_model=AssuntoOut, status_code=status.HTTP_201_CREATED)
def criar_assunto(
    dados: AssuntoIn,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    if db.get(Materia, dados.materia_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Matéria não encontrada.")
    assunto = Assunto(
        materia_id=dados.materia_id,
        nome=dados.nome.strip(),
        descricao=dados.descricao,
    )
    db.add(assunto)
    db.commit()
    db.refresh(assunto)
    return assunto


@router.get("", response_model=list[AssuntoOut])
def listar_assuntos(
    materia_id: int | None = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(Assunto)
    if materia_id is not None:
        query = query.filter(Assunto.materia_id == materia_id)
    return query.order_by(Assunto.nome).all()


@router.get("/{assunto_id}", response_model=AssuntoOut)
def obter_assunto(
    assunto_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return _obter_ou_404(db, assunto_id)


@router.put("/{assunto_id}", response_model=AssuntoOut)
def atualizar_assunto(
    assunto_id: int,
    dados: AssuntoIn,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    assunto = _obter_ou_404(db, assunto_id)
    if db.get(Materia, dados.materia_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Matéria não encontrada.")
    assunto.materia_id = dados.materia_id
    assunto.nome = dados.nome.strip()
    assunto.descricao = dados.descricao
    db.commit()
    db.refresh(assunto)
    return assunto


@router.delete("/{assunto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_assunto(
    assunto_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    assunto = _obter_ou_404(db, assunto_id)
    db.delete(assunto)
    db.commit()
