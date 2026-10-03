"""Fluxo do simulado — histórias #4, #5 e #6 (Sprint 2).

- POST /tentativas                  → aluno inicia uma tentativa (CT05)
- GET  /tentativas                  → histórico de tentativas do usuário logado
- GET  /tentativas/{id}             → dados de uma tentativa (só o dono ou admin)
- GET  /tentativas/{id}/questoes    → questões para responder, SEM revelar a correta
- POST /tentativas/{id}/respostas   → salva/substitui a resposta de uma questão (CT06)
- POST /tentativas/{id}/finalizar   → corrige: acertos, erros e percentual (CT07, CT08)

Regras de negócio:
- A correção objetiva NÃO depende de serviço externo: mesmo sem a integração
  de IA (Sprint 3), a correção é calculada normalmente (história #6, CT08).
- A alternativa correta só é revelada DEPOIS da finalização (não vaza na
  interface durante a resposta).
- A explicacao_ia permanece NULL até a Sprint 3 (história #7).
- Percentual de aproveitamento = acertos ÷ total de questões do simulado × 100;
  questões não respondidas não contam como erro, mas reduzem o percentual.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_aluno
from app.models import (
    Alternativa,
    Questao,
    Resposta,
    Simulado,
    Tentativa,
    agora_utc,
    simulado_questao,
)
from app.schemas import (
    AlternativaJogoOut,
    FinalizarOut,
    QuestaoJogoOut,
    RespostaCorrigidaOut,
    RespostaIn,
    TentativaIn,
    TentativaOut,
)

router = APIRouter(prefix="/tentativas", tags=["Simulados do aluno"])


def _obter_tentativa_ou_404(db: Session, tentativa_id: int) -> Tentativa:
    tentativa = db.get(Tentativa, tentativa_id)
    if tentativa is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tentativa não encontrada.")
    return tentativa


def _verificar_dono(tentativa: Tentativa, usuario) -> None:
    """Só o dono da tentativa (ou um admin) pode vê-la; só o dono a responde."""
    if tentativa.usuario_id != usuario.id and usuario.perfil != "ADMINISTRADOR":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Esta tentativa pertence a outro aluno.")


def _questao_pertence_ao_simulado(db: Session, simulado_id: int, questao_id: int) -> bool:
    linha = (
        db.execute(
            simulado_questao.select().where(
                simulado_questao.c.simulado_id == simulado_id,
                simulado_questao.c.questao_id == questao_id,
            )
        )
        .mappings()
        .first()
    )
    return linha is not None


@router.post("", response_model=TentativaOut, status_code=status.HTTP_201_CREATED)
def iniciar_tentativa(
    dados: TentativaIn,
    db: Session = Depends(get_db),
    aluno=Depends(require_aluno),
):
    """CT05: a tentativa fica registrada com status EM_ANDAMENTO (história #4)."""
    simulado = db.get(Simulado, dados.simulado_id)
    if simulado is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Simulado não encontrado.")
    if not simulado.questoes:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Este simulado não possui questões cadastradas.",
        )
    tentativa = Tentativa(usuario_id=aluno.id, simulado_id=simulado.id)
    db.add(tentativa)
    db.commit()
    db.refresh(tentativa)
    return tentativa


@router.get("", response_model=list[TentativaOut])
def minhas_tentativas(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    """Base do histórico de tentativas (história #8 — completa na Sprint 3)."""
    return (
        db.query(Tentativa)
        .filter(Tentativa.usuario_id == usuario.id)
        .order_by(Tentativa.id)
        .all()
    )


@router.get("/{tentativa_id}", response_model=TentativaOut)
def obter_tentativa(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    tentativa = _obter_tentativa_ou_404(db, tentativa_id)
    _verificar_dono(tentativa, usuario)
    return tentativa


@router.get("/{tentativa_id}/questoes", response_model=list[QuestaoJogoOut])
def questoes_da_tentativa(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    """CT05: questões do simulado na ordem cadastrada — SEM a marcação de correta."""
    tentativa = _obter_tentativa_ou_404(db, tentativa_id)
    _verificar_dono(tentativa, usuario)

    linhas = (
        db.execute(
            simulado_questao.select()
            .where(simulado_questao.c.simulado_id == tentativa.simulado_id)
            .order_by(simulado_questao.c.ordem)
        )
        .mappings()
        .all()
    )
    questao_ids = [linha["questao_id"] for linha in linhas]
    questoes = db.query(Questao).filter(Questao.id.in_(questao_ids)).all()
    mapa = {q.id: q for q in questoes}
    respondidas = {r.questao_id: r.alternativa_id for r in tentativa.respostas}

    jogo = []
    for questao_id in questao_ids:
        questao = mapa[questao_id]
        jogo.append(
            QuestaoJogoOut(
                id=questao.id,
                enunciado=questao.enunciado,
                nivel_dificuldade=questao.nivel_dificuldade,
                alternativas=[
                    AlternativaJogoOut(id=a.id, texto=a.texto) for a in questao.alternativas
                ],
                respondida_alternativa_id=respondidas.get(questao_id),
            )
        )
    return jogo


@router.post("/{tentativa_id}/respostas", response_model=TentativaOut)
def responder(
    tentativa_id: int,
    dados: RespostaIn,
    db: Session = Depends(get_db),
    aluno=Depends(require_aluno),
):
    """CT06: a resposta escolhida é armazenada na tentativa correta.

    Responder de novo a mesma questão SUBSTITUI a resposta (uma por questão).
    A alternativa precisa pertencer à questão, e a questão ao simulado.
    """
    tentativa = _obter_tentativa_ou_404(db, tentativa_id)
    if tentativa.usuario_id != aluno.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Esta tentativa pertence a outro aluno.")
    if tentativa.status != "EM_ANDAMENTO":
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Esta tentativa já foi finalizada; não aceita novas respostas."
        )

    questao = db.get(Questao, dados.questao_id)
    if questao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Questão não encontrada.")
    if not _questao_pertence_ao_simulado(db, tentativa.simulado_id, questao.id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Esta questão não pertence ao simulado desta tentativa.",
        )
    alternativa = db.get(Alternativa, dados.alternativa_id)
    if alternativa is None or alternativa.questao_id != questao.id:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "A alternativa informada não pertence a esta questão.",
        )

    resposta = (
        db.query(Resposta)
        .filter(Resposta.tentativa_id == tentativa.id, Resposta.questao_id == questao.id)
        .first()
    )
    if resposta is None:
        resposta = Resposta(tentativa_id=tentativa.id, questao_id=questao.id)
        db.add(resposta)
    resposta.alternativa_id = alternativa.id
    resposta.correta = alternativa.correta
    db.commit()
    db.refresh(tentativa)
    return tentativa


@router.post("/{tentativa_id}/finalizar", response_model=FinalizarOut)
def finalizar(
    tentativa_id: int,
    db: Session = Depends(get_db),
    aluno=Depends(require_aluno),
):
    """CT07/CT08: calcula acertos, erros e percentual do aproveitamento.

    A correção objetiva usa somente a resposta correta cadastrada no banco —
    não chama nenhum serviço externo — por isso funciona mesmo se a API de IA
    estiver indisponível (história #6, critério de aceite e CT08).
    """
    tentativa = _obter_tentativa_ou_404(db, tentativa_id)
    if tentativa.usuario_id != aluno.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Esta tentativa pertence a outro aluno.")
    if tentativa.status == "FINALIZADO":
        raise HTTPException(status.HTTP_409_CONFLICT, "Esta tentativa já foi finalizada.")

    respostas = tentativa.respostas
    acertos = sum(1 for r in respostas if r.correta)
    erros = len(respostas) - acertos
    total_questoes = len(tentativa.simulado.questoes)
    percentual = (acertos / total_questoes * 100) if total_questoes else 0.0

    tentativa.acertos = acertos
    tentativa.erros = erros
    tentativa.percentual_aproveitamento = round(percentual, 2)
    tentativa.data_fim = agora_utc()
    tentativa.status = "FINALIZADO"
    db.commit()
    db.refresh(tentativa)

    # explicacao_ia permanece NULL até a Sprint 3 (história #7).
    return FinalizarOut(
        tentativa=TentativaOut.model_validate(tentativa),
        respostas=[RespostaCorrigidaOut.model_validate(r) for r in respostas],
    )
