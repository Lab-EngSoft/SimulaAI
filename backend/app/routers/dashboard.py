"""História #9 (Sprint 3) — dashboard de desempenho do aluno.

Atende ao requisito mínimo do Manual §3 "Consulta agregada
(relatório/dashboard)": uma consulta com JOIN de 4 tabelas (resposta →
tentativa → questão → assunto → matéria) e GROUP BY, agregando no banco.

Critérios de aceite da história:
- total de simulados realizados (tentativas finalizadas);
- quantidade de acertos e erros;
- percentual/média de aproveitamento;
- desempenho por matéria e por assunto.

Só considera tentativas FINALIZADAS — uma tentativa em andamento não tem
resultado ainda. O acesso é do próprio aluno (require_aluno): cada aluno vê
exclusivamente os próprios dados.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_aluno
from app.models import Assunto, Materia, Questao, Resposta, Tentativa
from app.schemas import DashboardOut, DesempenhoRotuloOut

router = APIRouter(prefix="/dashboard", tags=["Dashboard do aluno"])


def _agregar_por_rotulo(
    db: Session, usuario_id: int, rotulo_coluna
) -> list[DesempenhoRotuloOut]:
    """GROUP BY com JOIN de 4 tabelas: a agregação acontece no BANCO.

    respondidas = nº de respostas em tentativas finalizadas;
    acertos     = soma de resposta.correta (case 1/0);
    percentual  = acertos ÷ respondidas × 100.
    """
    linhas = (
        db.query(
            rotulo_coluna.label("rotulo"),
            func.count(Resposta.id).label("respondidas"),
            func.sum(case((Resposta.correta == True, 1), else_=0)).label("acertos"),  # noqa: E712
        )
        .join(Tentativa, Resposta.tentativa_id == Tentativa.id)
        .join(Questao, Resposta.questao_id == Questao.id)
        .join(Assunto, Questao.assunto_id == Assunto.id)
        .join(Materia, Assunto.materia_id == Materia.id)
        .filter(Tentativa.usuario_id == usuario_id, Tentativa.status == "FINALIZADO")
        .group_by(rotulo_coluna)
        .order_by(rotulo_coluna)
        .all()
    )
    agregado = []
    for linha in linhas:
        respondidas = int(linha.respondidas or 0)
        acertos = int(linha.acertos or 0)
        percentual = (acertos / respondidas * 100) if respondidas else 0.0
        agregado.append(
            DesempenhoRotuloOut(
                rotulo=linha.rotulo,
                respondidas=respondidas,
                acertos=acertos,
                erros=respondidas - acertos,
                percentual=round(percentual, 2),
            )
        )
    return agregado


@router.get("", response_model=DashboardOut)
def meu_dashboard(db: Session = Depends(get_db), aluno=Depends(require_aluno)):
    """História #9: consolida o desempenho do aluno autenticado."""
    minhas = (
        db.query(Tentativa)
        .filter(Tentativa.usuario_id == aluno.id)
        .all()
    )
    finalizadas = [t for t in minhas if t.status == "FINALIZADO"]
    total_acertos = sum(t.acertos or 0 for t in finalizadas)
    total_erros = sum(t.erros or 0 for t in finalizadas)
    media = (
        sum(float(t.percentual_aproveitamento or 0) for t in finalizadas)
        / len(finalizadas)
        if finalizadas
        else 0.0
    )

    return DashboardOut(
        total_tentativas=len(minhas),
        tentativas_finalizadas=len(finalizadas),
        total_acertos=total_acertos,
        total_erros=total_erros,
        media_aproveitamento=round(media, 2),
        por_materia=_agregar_por_rotulo(db, aluno.id, Materia.nome),
        por_assunto=_agregar_por_rotulo(db, aluno.id, Assunto.nome),
    )
