
"""Teste real da Meta API — realiza uma chamada faturável."""

from dotenv import load_dotenv

load_dotenv()

from app.services.ia import (
    ContextoExplicacao,
    IAIndisponivel,
    obter_provedor,
)


def main() -> None:
    exemplo = ContextoExplicacao(
        materia="Matemática",
        assunto="Porcentagem",
        enunciado=(
            "Uma turma tem 40 alunos. "
            "Se 25% faltaram, quantos compareceram?"
        ),
        alternativas=(
            "10 alunos",
            "30 alunos",
            "35 alunos",
        ),
        resposta_aluno="35 alunos",
        resposta_correta="30 alunos",
    )

    try:
        print("Enviando questão demonstrativa para a Meta API...")
        print(obter_provedor().explicar(exemplo))

    except IAIndisponivel as erro:
        print(f"Não foi possível gerar a explicação: {erro}")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
