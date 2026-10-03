# Relatório de Entrega — Sprint 1 — SimulaAI

**Período:** 11/09/2026 a 02/10/2026 (Sprint 1 entregue junto com a Sprint 2, conforme autorização do professor)
**Sprint Review:** 02/10/2026 — [confirmar com o grupo]

## 1. Planejado vs. entregue

| História (backlog) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #1 Autenticação com perfis Aluno/Administrador | Sim | Sim | Backend FastAPI com login (JWT), registro de alunos e autorização validada no backend (rotas de escrita exigem perfil ADMINISTRADOR) |
| #2 Cadastro e gerenciamento de matérias e assuntos | Sim | Sim | CRUD completo na API, com validação de campos obrigatórios e nomes únicos de matéria |
| #3 Cadastro e gerenciamento de questões e alternativas | Sim | Sim | CRUD completo na API, com regra "exatamente uma alternativa correta" validada no backend |
| — (apoio) Base de frontend | Não planejada formalmente | Parcial | Interface React + TypeScript com login, painel administrativo e CRUD em memória, na branch `feature/frontend-sprint-1`; aguarda integração com a API na Sprint 2 |

## 2. Incremento funcional demonstrável

API REST do SimulaAI (FastAPI) com as três histórias Must da Sprint 1 funcionando:

- **Autenticação** — `POST /auth/login` devolve token JWT e o perfil do usuário; `POST /auth/register` cria contas de ALUNO; rotas administrativas recusam ALUNO com HTTP 403 e ausência de token com HTTP 401.
- **Matérias e assuntos** — CRUD completo (`/materias`, `/assuntos`), restrito a ADMINISTRADOR para escrita, com validação de campo obrigatório (422) e nome duplicado (409).
- **Questões e alternativas** — CRUD em `/questoes`, com validação de 2 a 5 alternativas e exatamente uma correta (422 caso contrário).

**Como reproduzir:** ver `README.md` (backend: `pip install -r backend/requirements.txt` + `uvicorn app.main:app --reload --port 8000`). A documentação interativa da API fica em `http://localhost:8000/docs`. O seed cria os usuários de demonstração `carlos.admin@simulaai.app` (senha `admin123`) e `ana.aluno@simulaai.app` (senha `aluno123`).

## 3. Backlog atualizado

- #1, #2, #3 — **concluídas** nesta sprint.
- #4 (iniciar simulado), #5 (responder questões), #6 (correção automática) — movidas para a Sprint 2, conforme planejamento original.
- #7–#10 — mantidas nas Sprints 3/4.

## 4. Evidências de teste

Casos CT01–CT04 do plano de testes (`docs/plano-de-testes.md`) implementados como testes automatizados pytest — **19 testes, 100% aprovados** na execução local de 02/10/2026; detalhe em `relatorios/sprint-1-evidencias-teste.md`.

## 5. Retrospectiva e contribuição individual

- Ata de retrospectiva: `relatorios/sprint-1-retrospectiva.md`
- Relatórios individuais: `relatorios/sprint-1-contribuicao-{gabriel,davi,vinicius,cesar}.md`

## 6. Riscos/impedimentos para a próxima sprint

- Integrar o frontend (que usa dados em memória) à API do backend — contrato de rotas definido: os formatos JSON das respostas de `/auth`, `/materias`, `/assuntos` e `/questoes` já estão documentados em `/docs` (Swagger).
- Persistência em PostgreSQL/Supabase ainda não conectada — o backend funciona com SQLite em desenvolvimento e troca de banco via `DATABASE_URL`, mas a validação no Supabase ficou para a Sprint 2.
- Execução dos testes no CI (GitHub Actions) pendente — a suíte pytest existe e roda localmente; automatizar o CI é ação da Sprint 2.
