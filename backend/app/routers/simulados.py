"""Cadastro administrativo de simulados e listagem para alunos.

A ordem fica registrada na tabela simulado_questao. Simulados já iniciados
não podem ter suas questões trocadas nem ser excluídos, protegendo o histórico.
Não é preciso alterar o esquema do banco para esta implementação.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_admin
from app.models import Questao, Simulado, Tentativa, simulado_questao
from app.schemas import SimuladoDetalheOut, SimuladoIn, SimuladoOut

router = APIRouter(prefix="/simulados", tags=["Simulados"])


def _obter_ou_404(db: Session, simulado_id: int) -> Simulado:
    simulado = db.get(Simulado, simulado_id)
    if simulado is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Simulado não encontrado.")
    return simulado


def _questao_ids(db: Session, simulado_id: int) -> list[int]:
    return list(db.scalars(
        select(simulado_questao.c.questao_id)
        .where(simulado_questao.c.simulado_id == simulado_id)
        .order_by(simulado_questao.c.ordem)
    ))


def _total_tentativas(db: Session, simulado_id: int) -> int:
    return db.query(Tentativa).filter(Tentativa.simulado_id == simulado_id).count()


def _detalhe(db: Session, simulado: Simulado) -> SimuladoDetalheOut:
    ids = _questao_ids(db, simulado.id)
    return SimuladoDetalheOut(
        id=simulado.id, titulo=simulado.titulo, descricao=simulado.descricao,
        total_questoes=len(ids), questao_ids=ids,
        total_tentativas=_total_tentativas(db, simulado.id),
    )


def _validar_questoes(db: Session, ids: list[int]) -> None:
    if len(ids) != len(set(ids)):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Não repita uma questão no mesmo simulado.")
    existentes = set(db.scalars(select(Questao.id).where(Questao.id.in_(ids))))
    ausentes = [questao_id for questao_id in ids if questao_id not in existentes]
    if ausentes:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Questões inexistentes: {', '.join(map(str, ausentes))}.",
        )


def _gravar_questoes(db: Session, simulado_id: int, ids: list[int]) -> None:
    db.execute(delete(simulado_questao).where(simulado_questao.c.simulado_id == simulado_id))
    db.execute(insert(simulado_questao), [
        {"simulado_id": simulado_id, "questao_id": questao_id, "ordem": ordem}
        for ordem, questao_id in enumerate(ids, start=1)
    ])


@router.get("", response_model=list[SimuladoOut])
def listar_simulados(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Alunos veem os simulados disponíveis, sem gabaritos."""
    return [
        SimuladoOut(
            id=simulado.id, titulo=simulado.titulo, descricao=simulado.descricao,
            total_questoes=len(_questao_ids(db, simulado.id)),
        )
        for simulado in db.query(Simulado).order_by(Simulado.id).all()
    ]


@router.get("/{simulado_id}", response_model=SimuladoDetalheOut)
def detalhar_simulado(
    simulado_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin),
):
    return _detalhe(db, _obter_ou_404(db, simulado_id))


@router.post("", response_model=SimuladoDetalheOut, status_code=status.HTTP_201_CREATED)
def criar_simulado(
    dados: SimuladoIn, db: Session = Depends(get_db), _admin=Depends(require_admin),
):
    _validar_questoes(db, dados.questao_ids)
    simulado = Simulado(titulo=dados.titulo.strip(), descricao=dados.descricao)
    db.add(simulado)
    db.flush()
    _gravar_questoes(db, simulado.id, dados.questao_ids)
    db.commit()
    return _detalhe(db, simulado)


@router.put("/{simulado_id}", response_model=SimuladoDetalheOut)
def atualizar_simulado(
    simulado_id: int, dados: SimuladoIn,
    db: Session = Depends(get_db), _admin=Depends(require_admin),
):
    simulado = _obter_ou_404(db, simulado_id)
    _validar_questoes(db, dados.questao_ids)
    if _questao_ids(db, simulado_id) != dados.questao_ids:
        if _total_tentativas(db, simulado_id):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Este simulado já possui tentativas. Não é possível modificar suas questões; crie outro simulado.",
            )
        _gravar_questoes(db, simulado_id, dados.questao_ids)
    simulado.titulo = dados.titulo.strip()
    simulado.descricao = dados.descricao
    db.commit()
    return _detalhe(db, simulado)


@router.delete("/{simulado_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_simulado(
    simulado_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin),
):
    simulado = _obter_ou_404(db, simulado_id)
    if _total_tentativas(db, simulado_id):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Este simulado já possui tentativas e não pode ser excluído.",
        )
    db.execute(delete(simulado_questao).where(simulado_questao.c.simulado_id == simulado_id))
    db.delete(simulado)
    db.commit()
