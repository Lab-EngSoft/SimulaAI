"""Rotas de matérias — história #2 (cadastro e gerenciamento, admin).

- Escrita (POST/PUT/DELETE): só ADMINISTRADOR (CT02 cobre o 403).
- Leitura (GET): qualquer usuário logado — o aluno vai precisar listar
  matérias no simulado/dashboard a partir da Sprint 2.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_admin
from app.models import Materia
from app.schemas import MateriaDetalheOut, MateriaIn, MateriaOut

router = APIRouter(prefix="/materias", tags=["Matérias"])


def _obter_ou_404(db: Session, materia_id: int) -> Materia:
    materia = db.get(Materia, materia_id)
    if materia is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Matéria não encontrada.")
    return materia


@router.post("", response_model=MateriaOut, status_code=status.HTTP_201_CREATED)
def criar_materia(
    dados: MateriaIn,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    nome = dados.nome.strip()
    if db.query(Materia).filter(Materia.nome == nome).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma matéria com este nome.")
    materia = Materia(nome=nome, descricao=dados.descricao)
    db.add(materia)
    db.commit()
    db.refresh(materia)
    return materia


@router.get("", response_model=list[MateriaOut])
def listar_materias(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(Materia).order_by(Materia.nome).all()


@router.get("/{materia_id}", response_model=MateriaDetalheOut)
def obter_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return _obter_ou_404(db, materia_id)


@router.put("/{materia_id}", response_model=MateriaOut)
def atualizar_materia(
    materia_id: int,
    dados: MateriaIn,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    materia = _obter_ou_404(db, materia_id)
    nome = dados.nome.strip()
    duplicada = (
        db.query(Materia).filter(Materia.nome == nome, Materia.id != materia_id).first()
    )
    if duplicada:
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma matéria com este nome.")
    materia.nome = nome
    materia.descricao = dados.descricao
    db.commit()
    db.refresh(materia)
    return materia


@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    materia = _obter_ou_404(db, materia_id)
    db.delete(materia)  # assuntos pendentes caem junto (ON DELETE CASCADE, E3)
    db.commit()
