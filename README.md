# SimulaAI

O SimulaAI é uma plataforma web de simulados para estudantes que se preparam para vestibulares, concursos, provas acadêmicas ou certificações. O sistema organiza questões por matéria e assunto, corrige tentativas, mostra o desempenho e gera explicações por IA para respostas incorretas.

**Deploy:** ainda não publicado — previsto para a Sprint 4 (história #11)
**Repositório:** https://github.com/Lab-EngSoft/SimulaAI
**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraifa Fifolato (2840482421022) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

> **Estado atual (entrega E7):** o backend FastAPI das Sprints 1–3 está implementado e testado (36 testes pytest, 100% aprovados): autenticação com perfis Aluno/Administrador, CRUD de matérias, assuntos e questões, fluxo completo do simulado (iniciar → responder → finalizar com correção automática), **explicação dos erros com IA e fallback** (história #7), **histórico de tentativas** (#8) e **dashboard de desempenho agregado** (#9). CI com GitHub Actions roda a suíte a cada push/PR. O frontend React está pronto na branch `feature/frontend-sprint-1` (dados em memória) e aguarda integração com a API na Sprint 4.

## Stack

- Frontend: React + TypeScript
- Backend: Python 3.12+ + FastAPI + SQLAlchemy (implementado)
- Banco de dados: PostgreSQL 15+ (Supabase) em produção; SQLite para desenvolvimento e testes
- Deploy planejado: Vercel (frontend) + Render (backend)

## Como rodar o backend localmente

### Pré-requisitos

- Python 3.12 ou superior
- Git 2.40 ou superior

### Passo a passo

1. Clone o repositório:

   ```powershell
   git clone https://github.com/Lab-EngSoft/SimulaAI.git
   Set-Location SimulaAI
   ```

2. Crie um ambiente virtual e instale as dependências do backend:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r backend\requirements.txt
   ```

   *(Se `python -m venv` falhar ao instalar o pip, crie com `python -m venv --without-pip .venv` e instale com `python -m pip install --user -r backend\requirements.txt`.)*

3. Configure as variáveis de ambiente. Copie `.env.example` para `.env` e preencha os valores locais. Nunca versione o arquivo `.env`:

   | Variável | Obrigatória | Descrição |
   |---|---:|---|
   | `DATABASE_URL` | Sim | URL de conexão; padrão local: `sqlite:///./simulaai.db` |
   | `SECRET_KEY` | Sim | Chave usada para assinar os tokens JWT; gere uma chave forte (mínimo 32 caracteres) |
   | `CORS_ORIGINS` | Sim | Origens permitidas, por exemplo `http://localhost:5173` |
   | `TOKEN_EXPIRA_MINUTOS` | Não | Validade do token em minutos (padrão: 480 = 8h) |
   | `AI_API_KEY` | Não | Chave da API de IA para as explicações (história #7). Sem ela, o sistema usa o fallback determinístico e segue 100% funcional |
   | `AI_BASE_URL` | Não | Base de um provedor compatível com a API da OpenAI (padrão: `https://api.openai.com/v1`) |
   | `AI_MODEL` | Não | Modelo usado nas explicações (padrão: `gpt-4o-mini`) |
   | `VITE_API_URL` | Sprint 4 | URL da API para o frontend, por exemplo `http://localhost:8000` |

4. Suba o servidor:

   ```powershell
   Set-Location backend
   .\..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
   ```

5. Acesse:
   - API: `http://localhost:8000`
   - Documentação interativa (Swagger): `http://localhost:8000/docs`

6. O seed cria automaticamente, na primeira execução, os usuários de demonstração e o conteúdo do `E3/schema.sql`:

   | Perfil | E-mail | Senha |
   |---|---|---|
   | ADMINISTRADOR | `carlos.admin@simulaai.app` | `admin123` |
   | ALUNO | `ana.aluno@simulaai.app` | `aluno123` |

7. Para usar o PostgreSQL/Supabase em produção, aponte `DATABASE_URL` para a URL do Supabase e execute o conteúdo de `E3/schema.sql` no SQL Editor do projeto.

## Como rodar o frontend localmente

A pasta `frontend/` completa (com `package.json`, `index.html`, `main.tsx` e configurações do Vite) está na branch `feature/frontend-sprint-1`. A partir da integração (Sprint 4):

```powershell
Set-Location frontend
npm install
npm run dev
```

Acesse `http://localhost:5173` e configure `VITE_API_URL=http://localhost:8000`.

## Estrutura do repositório

```text
/backend/                         — aplicação FastAPI (Sprints 1–3)
  /app/                           — main, database, models, schemas, security, deps, seed
    /routers/                     — auth, materias, assuntos, questoes, simulados, tentativas, dashboard
    /services/                    — explicacao_ia (IA com fallback)
  /tests/                         — suíte pytest (CT01–CT12 e regressões)
/.github/workflows/tests.yml      — CI: pytest a cada push/PR para a main
/E3/                              — DER, UML e schema SQL
/docs/plano-de-testes.md          — estratégia e casos de teste planejados
/docs/prototipo.md                — índice das telas do protótipo navegável
/relatorios/                    — relatórios, evidências e retrospectivas por sprint
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
- [Sprint 1 — relatório](relatorios/sprint-1-relatorio.md) · [evidências](relatorios/sprint-1-evidencias-teste.md) · [retrospectiva](relatorios/sprint-1-retrospectiva.md)
- [Sprint 2 — relatório](relatorios/sprint-2-relatorio.md) · [evidências](relatorios/sprint-2-evidencias-teste.md) · [retrospectiva](relatorios/sprint-2-retrospectiva.md)
- [Sprint 3 — relatório](relatorios/sprint-3-relatorio.md) · [evidências](relatorios/sprint-3-evidencias-teste.md) · [retrospectiva](relatorios/sprint-3-retrospectiva.md)

## Convenções da equipe

- Branches: `main` para a versão integrada; `feature/<descricao>` para funcionalidades; `fix/<descricao>` para correções; `docs/<descricao>` para documentação.
- Commits: Conventional Commits, por exemplo `feat: adicionar cadastro de questões` ou `docs: atualizar plano de testes`.
- Toda PR exige revisão de pelo menos um integrante antes do merge na `main`.
- A branch `main` deve permanecer integrável; alterações devem ser feitas em branches de trabalho.

## Testes

A suíte pytest cobre os casos CT01–CT12 do plano de testes (`docs/plano-de-testes.md`) e regressões:

```powershell
Set-Location backend
python -m pip install -r requirements.txt   # na primeira vez
python -m pytest
```

Estado atual: **36 testes, 100% aprovados** (execução local de 03/10/2026). O CI (GitHub Actions, `.github/workflows/tests.yml`) executa a suíte automaticamente a cada push/PR para a main — sempre sem `AI_API_KEY`, provando que correção e explicações funcionam sem a IA. O comando oficial deve ser executado antes de abrir uma PR.

## Licença / Uso acadêmico

Projeto desenvolvido para a disciplina de Laboratório de Engenharia de Software — ADS, Fatec Ribeirão Preto, 2026.
