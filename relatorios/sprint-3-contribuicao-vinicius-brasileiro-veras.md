# Relatório Individual de Contribuição — Sprint 3 — Vinicius Brasileiro Veras (RA 2840482421021)

**Papel nesta sprint:** Backend

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Endpoint `GET /dashboard` com agregação no banco (JOIN de 4 tabelas + GROUP BY): total de tentativas, tentativas finalizadas, acertos, erros, média de aproveitamento e desempenho **por matéria** e **por assunto** (história #9 — requisito mínimo do Manual §3, apontada como pendente no relatório da sprint) | PR #4 (branch `feature/backend-sprint-3`) | Concluído |
| Testes automatizados CT11 (histórico de tentativas de diferentes simulados, com isolamento por aluno) e CT12 (dashboard agregado por matéria/assunto) | PR #4 | Concluído |
| CI com GitHub Actions (`.github/workflows/tests.yml`): pytest a cada push/PR para a main, sem chave de IA no ambiente | PR #4 | Concluído |
| Resolução do conflito da PR #4 com o trabalho da equipe: mantive o contrato de IA do grupo (`services/ia.py`, `POST /tentativas/{id}/explicacoes`, 503 quando indisponível — o frontend integrado depende dele) e removi minha implementação paralela de explicações para não duplicar código | PR #4 (merge) | Concluído |
| Documentos da entrega E7: evidências de teste da sprint 3 e atualização do README (variáveis NVIDIA_*, estrutura com frontend/ e database/, 47 testes) | PR #4 | Concluído |

## 2. Rituais que participei

- [ ] Dailies/weeklies — não houve dailies ou weeklies formais na Sprint 3; a comunicação da equipe foi realizada por WhatsApp.
- [ ] Sprint Review — [confirmar com o grupo]
- [ ] Retrospectiva — a ata de retrospectiva da Sprint 3 foi registrada no repositório (`relatorios/sprint-3-retrospectiva.md`).

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| [preencher somente se você revisou uma PR de colega] | — | |

## 4. Dificuldades e o que aprendi

O maior aprendizado desta sprint não foi técnico, foi de processo: eu e o Gabriel implementamos a história #7 (explicações por IA) **em paralelo, sem saber** — eu com um serviço de fallback determinístico, ele com o provedor NVIDIA NIM e o frontend já integrado ao contrato dele. Quando abri minha PR, ela conflitou com a main. A resolução me ensinou o que "trabalho em equipe" significa na prática: o contrato que já está rodando no frontend do projeto vence; a minha implementação paralela foi removida sem drama, porque o que importa é o produto final. Ficou da minha parte o que só a minha branch tinha e o relatório do grupo apontava como pendente: o dashboard da história #9 com a agregação no banco (JOIN de 4 tabelas com GROUP BY), o CI e os testes de histórico e dashboard. Na técnica, aprendi a resolver um merge com conflitos reais (4 arquivos, inclusive um add/add de documento) mantendo os testes verdes do começo ao fim — a suíte combinada fechou com 47 testes aprovados.
