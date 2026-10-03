# Relatório Individual de Contribuição — Sprint 2 — Vinicius Brasileiro Veras (RA 2840482421021)

**Papel nesta sprint:** Backend

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Rotas do fluxo de simulado: iniciar tentativa, responder questões e finalizar com correção (histórias #4, #5 e #6) | PR #2 (branch `feature/backend-sprints-1-2`) | Concluído |
| Regra de negócio: correção calcula acertos, erros e percentual de aproveitamento; a resposta correta só é revelada na correção | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Regra de negócio: correção objetiva independente da disponibilidade da IA — critério de aceite da história #6 (CT08) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Autorização por perfil no fluxo do aluno: `require_aluno` (403 para admin) e bloqueio de acesso a tentativa de outro aluno | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Testes automatizados CT05–CT08 e regressões (12 testes novos; suíte total: 31 testes, 100% aprovados) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |
| Base do histórico de tentativas (`GET /tentativas`) para a história #8 (Sprint 3) | PR #2 (commits `5a8d13e` e `8a1af53`) | Concluído |

## 2. Rituais que participei

- [ ] Dailies/weeklies — não houve dailies ou weeklies formais na Sprint 2; a comunicação da equipe foi realizada por WhatsApp.
- [ ] Sprint Review — não houve Sprint Review formal; a entrega conjunta das Sprints 1 e 2 foi autorizada pelo professor.
- [ ] Retrospectiva — a ata de retrospectiva da Sprint 2 foi elaborada a partir do balanço da equipe e registrada no repositório (`docs/sprints/sprint-2-retrospectiva.md`).

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| [preencher somente se você revisou uma PR de colega] | — | |

## 4. Dificuldades e o que aprendi

Com o backend pronto e testado, o foco desta sprint foi o fluxo do simulado. Aprendi a desenhar a correção de forma que ela nunca dependa de um serviço externo: o endpoint calcula acertos, erros e percentual usando somente a resposta correta cadastrada no banco, o que cumpre o critério de aceite da história #6 (funcionar mesmo se a IA estiver indisponível). Testar esse caso (CT08) antes de sequer existir a integração de IA mudou o meu jeito de pensar regras de negócio. A integração frontend↔backend ficou para a Sprint 3, conforme registrado na retrospectiva.
