
"""Assinatura das explicações para reutilização segura."""

import hashlib
import json
import os

from app.models import Alternativa, Questao
from app.services.ia import PROMPT_VERSAO


def modelo_atual() -> str:
    return os.getenv(
        "META_MODEL",
        "muse-spark-1.3-contributor",
    )


def assinatura_explicacao(
    questao: Questao,
    escolhida: Alternativa,
) -> str:
    alternativas = sorted(
        questao.alternativas,
        key=lambda alt: alt.id,
    )

    payload = {
        "versao_prompt": PROMPT_VERSAO,
        "modelo": modelo_atual(),
        "servidor": os.getenv(
            "META_BASE_URL",
            "https://api.meta.ai/v1",
        ).rstrip("/"),
        "questao_id": questao.id,
        "materia": [
            questao.assunto.materia.id,
            questao.assunto.materia.nome,
        ],
        "assunto": [
            questao.assunto.id,
            questao.assunto.nome,
        ],
        "enunciado": questao.enunciado,
        "nivel_dificuldade": questao.nivel_dificuldade,
        "alternativas": [
            {
                "id": alt.id,
                "texto": alt.texto,
                "correta": alt.correta,
            }
            for alt in alternativas
        ],
        "escolhida_id": escolhida.id,
    }

    bruto = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        bruto.encode("utf-8")
    ).hexdigest()
