# Relatório Individual de Contribuição — Sprint 1 — Vinicius Brasileiro Veras (RA 2840482421021)

**Papel nesta sprint:** Backend

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Estrutura do backend FastAPI: conexão de banco via `DATABASE_URL` e modelos ORM espelhando o `E3/schema.sql` (9 tabelas) | PR #2 (branch `feature/backend-sprints-1-2`) | Concluído |
| Autenticação com perfis ALUNO/ADMINISTRADOR: login JWT, registro de alunos e autorização validada no backend (história #1) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| CRUD de matérias e assuntos com validação de campo obrigatório e nome único (história #2) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| CRUD de questões e alternativas com a regra "exatamente uma alternativa correta" validada no backend (história #3) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Suíte pytest com os casos CT01–CT04 (19 testes, 100% aprovados) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Seed de dados de demonstração alinhado ao `E3/schema.sql` (usuários, matérias, assuntos, questões e simulado) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Correção de documentação: e-mails de demonstração com domínio válido (`.app`) — os testes detectaram que `.local` é domínio reservado e recusado pelo validador | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |

## 2. Rituais que participei

- [ ] Dailies/weeklies — [preencher conforme a sua participação real]
- [ ] Sprint Review — [preencher]
- [ ] Retrospectiva — [preencher]

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| [preencher somente se você revisou uma PR de colega] | — | |

## 4. Dificuldades e o que aprendi

A entrega desta sprint ficou concentrada no backend, papel acordado no termo de aceite, e foi entregue junto com a Sprint 2 conforme autorização do professor. Nunca tinha usado Git/GitHub — vinha de backup manual — e aprendi clone, branch, commit, push e Pull Request durante a entrega. Os testes automatizados detectaram um bug real no dado de exemplo (um domínio de e-mail reservado que o validador recusa), o que me mostrou na prática o valor de uma suíte de testes: ela pega defeitos que passam despercebidos na revisão de olho.
