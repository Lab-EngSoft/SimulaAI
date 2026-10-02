# SimulaAI

O SimulaAI será uma plataforma web de simulados para estudantes que se preparam para vestibulares, concursos, provas acadêmicas ou certificações. O sistema organiza questões por matéria e assunto, corrige tentativas, mostra o desempenho e gera explicações por IA para respostas incorretas.

**Deploy:** ainda não publicado — previsto para as sprints de implementação
**Repositório:** https://github.com/Lab-EngSoft/SimulaAI
**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

> **Estado da entrega E4:** este repositório contém a documentação e o schema de dados das entregas E1–E3. A aplicação ainda não possui código de frontend/backend executável; os comandos abaixo descrevem a configuração definida para a implementação.

## Stack

- Frontend: React + TypeScript
- Backend: Python 3.12+ + FastAPI
- Banco de dados: PostgreSQL 15+ (Supabase)
- Deploy planejado: Vercel (frontend) + Render (backend)

## Como rodar localmente

### Pré-requisitos

- Git 2.40 ou superior
- Node.js 20 ou superior e npm 10 ou superior
- Python 3.12 ou superior
- PostgreSQL 15 ou superior, ou uma conta/projeto no Supabase
- Acesso à internet para instalar dependências e, quando implementada, consultar a API de IA

### Passo a passo

1. Clone o repositório:

   ```powershell
   git clone https://github.com/Lab-EngSoft/SimulaAI.git
   Set-Location SimulaAI
   ```

2. Instale as dependências quando as pastas de aplicação forem adicionadas:

   ```powershell
   npm install                 # frontend, quando houver package.json
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r backend\requirements.txt
   ```

3. Configure as variáveis de ambiente. Copie `.env.example` para `.env` e preencha os valores locais. Nunca versione o arquivo `.env`:

   | Variável | Obrigatória | Descrição |
   |---|---:|---|
   | `DATABASE_URL` | Sim | URL de conexão do PostgreSQL/Supabase |
   | `SECRET_KEY` | Sim | Chave usada para assinar sessões ou tokens; gere uma chave forte |
   | `AI_API_KEY` | Sim para explicações por IA | Chave da API de IA usada pelo backend |
   | `CORS_ORIGINS` | Sim | Origens permitidas, por exemplo `http://localhost:5173` |
   | `VITE_API_URL` | Sim para o frontend | URL da API, por exemplo `http://localhost:8000` |

   O arquivo `.env.example` deverá conter somente nomes de variáveis e valores fictícios, por exemplo:

   ```dotenv
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/simulaai
   SECRET_KEY=chave-local-apenas-para-desenvolvimento
   AI_API_KEY=preencher-localmente
   CORS_ORIGINS=http://localhost:5173
   VITE_API_URL=http://localhost:8000
   ```

4. Crie o banco `simulaai` e aplique o schema:

   ```powershell
   createdb simulaai
   psql -d simulaai -f E3\schema.sql
   ```

   No Supabase, use o SQL Editor para executar o conteúdo de [E3/schema.sql](E3/schema.sql).

5. O arquivo `E3\schema.sql` já contém o seed de dados demonstrativos e deve ser executado uma única vez em um banco vazio. Migrations específicas do backend ainda serão adicionadas durante a implementação.

6. Suba os serviços durante a implementação:

   ```powershell
   # backend
   uvicorn app.main:app --reload --port 8000

   # frontend, em outro terminal
   npm run dev
   ```

7. Acesse o frontend em `http://localhost:5173`. A documentação da API ficará disponível em `http://localhost:8000/docs` quando o backend for implementado.

## Estrutura do repositório

```text
/E3/                              — DER, UML e schema SQL
/docs/plano-de-testes.md          — estratégia e casos de teste planejados
/docs/prototipo.md                — índice das telas do protótipo navegável
/backlog.md                       — histórias priorizadas e critérios de aceite
/Documento de Visão — SimulaAI.md — problema, público, objetivos e requisitos
/E2-Lucas.md                      — termo de aceite do projeto
/README.md                        — instruções de configuração e uso
```

## Documentação do projeto

- [Documento de Visão](Documento%20de%20Visão%20—%20SimulaAI.md)
- [Backlog priorizado](backlog.md)
- [Termo de Aceite do Projeto](E2-Lucas.md)
- [DER e dicionário de dados](E3/DER.md)
- [Diagramas UML](E3/UML.md)
- [Schema SQL](E3/schema.sql)
- [Plano de testes](docs/plano-de-testes.md)
- [Roteiro do protótipo](docs/prototipo.md)

## Convenções da equipe

- Branches: `main` para a versão integrada; `feature/<descricao>` para funcionalidades; `fix/<descricao>` para correções; `docs/<descricao>` para documentação.
- Commits: Conventional Commits, por exemplo `feat: adicionar cadastro de questões` ou `docs: atualizar plano de testes`.
- Toda PR exige revisão de pelo menos um integrante antes do merge na `main`.
- A branch `main` deve permanecer integrável; alterações devem ser feitas em branches de trabalho.

## Testes

O plano de testes da E4 está em [docs/plano-de-testes.md](docs/plano-de-testes.md). No estado atual ainda não há suíte automatizada nem comando de teste executável, pois a aplicação está em fase de documentação e modelagem.

Quando o código for adicionado, o comando oficial deverá ser documentado aqui e executado antes de abrir uma PR. O mínimo esperado é:

```powershell
npm test
pytest
```

## Licença / Uso acadêmico

Projeto desenvolvido para a disciplina de Laboratório de Engenharia de Software — ADS, Fatec Ribeirão Preto, 2026.