"""Seed de dados de demonstração — mesmos registros do E3/schema.sql.

Usuários criados (senhas são fictícias, só para desenvolvimento local):
- ADMINISTRADOR: carlos.admin@simulaai.local  /  admin123
- ALUNO:         ana.aluno@simulaai.local     /  aluno123

O seed é idempotente: se o admin já existe, não faz nada.
"""
from app.database import SessionLocal
from app.models import (
    Alternativa,
    Assunto,
    Materia,
    Questao,
    Simulado,
    Usuario,
    simulado_questao,
)
from app.security import hash_password

ADMIN_EMAIL = "carlos.admin@simulaai.app"
ALUNO_EMAIL = "ana.aluno@simulaai.app"


def seed_inicial() -> None:
    db = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.email == ADMIN_EMAIL).first():
            return  # já semeado

        db.add_all(
            [
                Usuario(
                    nome="Carlos Oliveira",
                    email=ADMIN_EMAIL,
                    senha_hash=hash_password("admin123"),
                    perfil="ADMINISTRADOR",
                ),
                Usuario(
                    nome="Ana Souza",
                    email=ALUNO_EMAIL,
                    senha_hash=hash_password("aluno123"),
                    perfil="ALUNO",
                ),
            ]
        )

        matematica = Materia(nome="Matemática", descricao="Conteúdos de matemática para treinamento.")
        portugues = Materia(
            nome="Língua Portuguesa", descricao="Conteúdos de interpretação e gramática."
        )
        porcentagem = Assunto(materia=matematica, nome="Porcentagem", descricao="Cálculos percentuais.")
        interpretacao = Assunto(
            materia=portugues, nome="Interpretação de texto", descricao="Compreensão de textos."
        )

        questao1 = Questao(
            assunto=porcentagem,
            enunciado="Uma turma tem 40 alunos. Se 25% faltaram, quantos alunos compareceram?",
            nivel_dificuldade="Fácil",
        )
        questao1.alternativas = [
            Alternativa(texto="10 alunos", correta=False),
            Alternativa(texto="30 alunos", correta=True),
            Alternativa(texto="35 alunos", correta=False),
        ]
        questao2 = Questao(
            assunto=interpretacao,
            enunciado="Ao identificar a ideia principal de um texto, o leitor deve observar principalmente:",
            nivel_dificuldade="Médio",
        )
        questao2.alternativas = [
            Alternativa(texto="A informação central desenvolvida pelo texto", correta=True),
            Alternativa(texto="A maior palavra do texto", correta=False),
            Alternativa(texto="A opinião de um leitor externo", correta=False),
        ]

        simulado = Simulado(
            titulo="Simulado demonstrativo",
            descricao="Simulado inicial para validar o fluxo do aluno.",
        )

        db.add_all([matematica, portugues, questao1, questao2, simulado])
        db.commit()  # gera os ids

        # Relacionamento N:N com ordem (tabela associativa do E3) — a coluna
        # ordem é NOT NULL, então ela é preenchida explicitamente.
        db.execute(
            simulado_questao.insert(),
            [
                {"simulado_id": simulado.id, "questao_id": questao1.id, "ordem": 1},
                {"simulado_id": simulado.id, "questao_id": questao2.id, "ordem": 2},
            ],
        )
        db.commit()
    finally:
        db.close()
