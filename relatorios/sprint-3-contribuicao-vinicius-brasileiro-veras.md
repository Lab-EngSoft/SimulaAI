# Relatório Individual de Contribuição — Sprint 3 — Vinicius Brasileiro Veras (RA 2840482421021)

**Papel nesta sprint:** Backend

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Serviço de explicação da IA em duas camadas com fallback determinístico — a correção e a explicação nunca dependem de serviço externo (história #7) | PR #[___] (branch `feature/backend-sprint-3`) | Concluído |
| Geração de explicações na finalização (100% dos erros) + endpoint `GET /tentativas/{id}/explicacoes` com bloqueio antes de finalizar (história #7) | PR #[___] | Concluído |
| Endpoint `GET /dashboard` com agregação no banco (JOIN de 4 tabelas + GROUP BY): total de tentativas, acertos, erros, média de aproveitamento e desempenho por matéria e por assunto (história #9) | PR #[___] | Concluído |
| Consolidação do histórico de tentativas de diferentes simulados com resultados e isolamento por aluno (história #8) | PR #[___] | Concluído |
| Testes automatizados CT09–CT12 (5 novos; suíte total: 36 testes, 100% aprovados) e atualização do CT08 à realidade da Sprint 3 | PR #[___] | Concluído |
| CI com GitHub Actions (`.github/workflows/tests.yml`): pytest a cada push/PR para a main, sem chave de IA no ambiente | PR #[___] | Concluído |

## 2. Rituais que participei

- [ ] Dailies/weeklies — não houve dailies ou weeklies formais na Sprint 3; a comunicação da equipe foi realizada por WhatsApp.
- [ ] Sprint Review — [confirmar com o grupo]
- [ ] Retrospectiva — a ata de retrospectiva da Sprint 3 foi elaborada a partir do balanço da equipe e registrada no repositório (`relatorios/sprint-3-retrospectiva.md`).

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| [preencher somente se você revisou uma PR de colega] | — | |

## 4. Dificuldades e o que aprendi

O desafio central desta sprint foi a história #7 sem repetir o erro clássico de depender de serviço externo: desenhei o serviço de explicação em duas camadas — IA quando existe chave configurada, fallback determinístico construído com os dados do banco quando não existe (ou quando a chamada falha). O aprendizado foi perceber que essa decisão já tinha sido ensaiada na Sprint 2, na correção objetiva sem IA: a suíte de testes antiga continuou passando durante toda a implementação, o que confirmou que o padrão estava certo. No dashboard, aprendi a empurrar a agregação para o banco (JOIN de 4 tabelas com GROUP BY) em vez de montar os números na aplicação — a consulta fica mais simples e o teste do CT12 valida os números agrupados de ponta a ponta.
