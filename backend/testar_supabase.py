
"""Testa a conexão do SimulaAI com o Supabase.

Somente leitura: não cria, altera ou apaga registros.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import inspect, text
from sqlalchemy.engine import make_url

# Carrega o .env da raiz antes de importar o banco.
raiz = Path(__file__).resolve().parent.parent
load_dotenv(raiz / ".env")

from app.database import DATABASE_URL, engine


def main():
    url = make_url(DATABASE_URL)

    if not url.drivername.startswith("postgresql"):
        print("ERRO: o SimulaAI ainda está usando SQLite.")
        print("Configure DATABASE_URL no .env da raiz.")
        sys.exit(1)

    # Mostra o destino sem revelar a senha.
    print(f"Servidor: {url.host}")
    print(f"Porta: {url.port or 5432}")
    print("Conectando ao PostgreSQL...")

    try:
        with engine.connect() as conexao:
            resultado = conexao.execute(
                text("""
                    SELECT
                        current_database() AS banco,
                        current_user AS usuario,
                        current_timestamp AS horario
                """)
            ).mappings().one()

            print("\nCONEXÃO ESTABELECIDA!")
            print(f"Banco: {resultado['banco']}")
            print(f"Usuário: {resultado['usuario']}")
            print(f"Horário do servidor: {resultado['horario']}")

            tabelas = set(
                inspect(conexao).get_table_names(schema="public")
            )

            esperadas = [
                "usuario",
                "materia",
                "assunto",
                "questao",
                "alternativa",
                "simulado",
                "simulado_questao",
                "tentativa",
                "resposta",
            ]

            print("\nVerificando tabelas:")

            for tabela in esperadas:
                if tabela in tabelas:
                    print(f"[OK] {tabela}")
                else:
                    print(f"[PENDENTE] {tabela}")

            if "usuario" in tabelas:
                total = conexao.execute(
                    text("SELECT COUNT(*) FROM public.usuario")
                ).scalar_one()

                print(f"\nUsuários cadastrados: {total}")

            if len(tabelas.intersection(esperadas)) == len(esperadas):
                print("\nEstrutura básica do SimulaAI encontrada.")
            else:
                print("\nConexão OK, mas faltam tabelas.")

    except Exception as erro:
        print(f"\nFALHA NA CONEXÃO: {erro.__class__.__name__}")
        print("Verifique a URI, senha, rede e status do projeto.")
        sys.exit(1)

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
