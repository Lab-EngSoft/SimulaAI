# Relatório de Entrega — Sprint 2 — SimulaAI

**Período:** 19/09/2026 a 02/10/2026 (entrega documentada em 02/10/2026, com prazo estendido pelo professor)
**Sprint Review:** 02/10/2026 — [confirmar com o grupo]

## 1. Planejado vs. entregue

| História (backlog) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #4 Como aluno, quero iniciar um simulado | Sim | Sim | `POST /tentativas` registra a tentativa (status EM_ANDAMENTO); `GET /tentativas/{id}/questoes` devolve as questões na ordem cadastrada, sem revelar a alternativa correta |
| #5 Como aluno, quero responder às questões | Sim | Sim | `POST /tentativas/{id}/respostas` persiste a resposta (uma por questão, substituível); valida que a questão pertence ao simulado e a alternativa à questão |
| #6 Como aluno, quero finalizar e receber a correção | Sim | Sim | `POST /tentativas/{id}/finalizar` calcula acertos, erros e percentual de aproveitamento; a correção objetiva independe de serviço externo (IA) |
| #1–#3 (Sprint 1) | — | Mantidas | Autenticação e CRUDs continuam cobertos pela suíte de testes (regressão) |

## 2. Incremento funcional demonstrável

Fluxo completo do simulado na API: **iniciar → responder → finalizar com correção automática**.

- `GET /simulados` lista os simulados com o total de questões de cada um.
- A tentativa fica registrada e vinculada ao aluno autenticado (história #4); dados de um aluno não vazam para outro.
- Respostas persistidas com uma única escolha por questão; a resposta correta só é revelada após a finalização.
- Correção calculada pelo próprio sistema (acertos, erros, percentual), sem depender da API de IA — critério de aceite da história #6.

**Como reproduzir:** ver `README.md`. Roteiro rápido: login como `ana.aluno@simulaai.app` → `GET /simulados` → `POST /tentativas` → `POST /tentativas/{id}/respostas` para cada questão → `POST /tentativas/{id}/finalizar`. Documentação interativa em `http://localhost:8000/docs`.

## 3. Backlog atualizado

- #4, #5, #6 — **concluídas** nesta sprint.
- #7 (explicação por IA), #8 (histórico), #9 (dashboard) — Sprints 3.
- #10 (evolução entre tentativas), #11 (deploy público) — Sprint 4.

## 4. Evidências de teste

CT05–CT08 do plano de testes (`docs/plano-de-testes.md`) implementados como testes automatizados pytest — **12 testes novos; suíte total: 31 testes, 100% aprovados** na execução local de 02/10/2026; detalhe em `docs/sprints/sprint-2-evidencias-teste.md`.

## 5. Retrospectiva e contribuição individual

- Ata de retrospectiva: `docs/sprints/sprint-2-retrospectiva.md`
- Relatórios individuais: `docs/sprints/sprint-2-contribuicao-{gabriel,davi,vinicius,cesar}.md`

## 6. Riscos/impedimentos para a próxima sprint

- **Integração frontend↔backend:** as telas React usam dados em memória; o contrato das rotas está documentado em `/docs` (Swagger). Responsável: Cesar, com apoio do backend.
- **Explicação por IA (história #7):** definir o provedor e a chave (`AI_API_KEY`) e implementar com fallback — a correção objetiva nunca pode parar se a IA falhar.
- **PostgreSQL/Supabase:** conectar via `DATABASE_URL` e validar o schema no banco real (o backend já troca de banco por variável de ambiente).
- **CI (GitHub Actions):** executar pytest a cada PR.
