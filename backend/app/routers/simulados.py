"""Rotas de simulados — história #4 (o aluno escolhe um simulado para iniciar).

A leitura é aberta a qualquer usuário logado; a criação/edição de simulados
como conteúdo administrativo pode ser adicionada em sprint posterior.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Simulado
from app.schemas import SimuladoOut

router = APIRouter(prefix="/simulados", tags=["Simulados"])


@router.get("", response_model=list[SimuladoOut])
def listar_simulados(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Lista os simulados com a quantidade de questões de cada um."""
    resultado = []
    for simulado in db.query(Simulado).order_by(Simulado.id).all():
        resultado.append(
            SimuladoOut(
                id=simulado.id,
                titulo=simulado.titulo,
                descricao=simulado.descricao,
                total_questoes=len(simulado.questoes),
            )
        )
    return resultado
