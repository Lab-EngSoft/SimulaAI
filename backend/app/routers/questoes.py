"""Rotas de questões e alternativas — história #3.

A leitura do banco administrativo exige perfil ADMINISTRADOR, pois revela
o gabarito. Alunos recebem alternativas sem gabarito via /tentativas/{id}/questoes.

Regra de negócio central (CT04): toda questão deve ter de 2 a 5 alternativas
e EXATAMENTE UMA correta. Sem isso o simulado não pode ser corrigido de
forma confiável. A validação acontece aqui no backend, porque depender só
do frontend deixaria a API exposta.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.integridade import questao_usada_em_simulado, questao_com_tentativas
from app.deps import require_admin
from app.models import Alternativa, Assunto, Questao
from app.schemas import QuestaoIn, QuestaoOut, QuestaoUpdate

router = APIRouter(prefix="/questoes", tags=["Questões"])


def _obter_ou_404(db: Session, questao_id: int) -> Questao:
    questao = db.get(Questao, questao_id)
    if questao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Questão não encontrada.")
    return questao


def _validar_alternativas(alternativas) -> None:
    corretas = [a for a in alternativas if a.correta]
    if len(corretas) != 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"A questão deve ter exatamente uma alternativa correta; recebidas: {len(corretas)}.",
        )


@router.post("", response_model=QuestaoOut, status_code=status.HTTP_201_CREATED)
def criar_questao(
    dados: QuestaoIn,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    if db.get(Assunto, dados.assunto_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Assunto não encontrado.")
    _validar_alternativas(dados.alternativas)

    questao = Questao(
        assunto_id=dados.assunto_id,
        enunciado=dados.enunciado,
        nivel_dificuldade=dados.nivel_dificuldade,
    )
    questao.alternativas = [
        Alternativa(texto=a.texto, correta=a.correta) for a in dados.alternativas
    ]
    db.add(questao)
    db.commit()
    db.refresh(questao)
    return questao


@router.get("", response_model=list[QuestaoOut])
def listar_questoes(
    assunto_id: int | None = None,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    query = db.query(Questao)
    if assunto_id is not None:
        query = query.filter(Questao.assunto_id == assunto_id)
    return query.order_by(Questao.id).all()


@router.get("/{questao_id}", response_model=QuestaoOut)
def obter_questao(
    questao_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return _obter_ou_404(db, questao_id)


@router.put("/{questao_id}", response_model=QuestaoOut)
def atualizar_questao(
    questao_id: int,
    dados: QuestaoUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    questao = _obter_ou_404(db, questao_id)
    if questao_com_tentativas(db, questao_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Questão com tentativas registradas não pode ser alterada. Crie uma nova questão.")
    if dados.assunto_id is not None:
        if db.get(Assunto, dados.assunto_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Assunto não encontrado.")
        questao.assunto_id = dados.assunto_id
    if dados.enunciado is not None:
        questao.enunciado = dados.enunciado
    if dados.nivel_dificuldade is not None:
        questao.nivel_dificuldade = dados.nivel_dificuldade
    if dados.alternativas is not None:
        _validar_alternativas(dados.alternativas)
        questao.alternativas.clear()  # delete-orphan remove as antigas
        questao.alternativas = [
            Alternativa(texto=a.texto, correta=a.correta) for a in dados.alternativas
        ]
    db.commit()
    db.refresh(questao)
    return questao


@router.delete("/{questao_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_questao(
    questao_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    questao = _obter_ou_404(db, questao_id)
    if questao_usada_em_simulado(db, questao_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "A questão faz parte de um simulado. Remova-a dos simulados antes de excluí-la.")
    db.delete(questao)
    db.commit()
