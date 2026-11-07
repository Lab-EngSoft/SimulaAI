# Relatório Individual de Contribuição — Sprint 4 — Vinicius Brasileiro Veras (RA 2840482421021)

**Papel nesta sprint:** Backend

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Endpoint `GET /dashboard/evolucao` (história #10): linha do tempo das tentativas finalizadas em ordem cronológica, com simulado, acertos, erros, percentual, variação ponto a ponto, `variacao_total` e `tendencia` — calculada só a partir do histórico persistido | PR #5 (branch `feature/backend-sprint-4`) | Concluído |
| Schemas `EvolucaoItemOut`/`EvolucaoOut` com validação pydantic | PR #5 | Concluído |
| Testes automatizados CT13 (evolução cronológica com 3 simulados diferentes + variação) e CT14 (isolamento por aluno, 403 para admin) — suíte total: 49 testes, 100% aprovados | PR #5 | Concluído |
| Backend pronto para deploy (história #11): `backend/Procfile`, `backend/runtime.txt`, endpoint `/health` | PR #5 | Concluído |
| Guia de deploy `docs/deploy.md` (Supabase → Render → Vercel → CORS → registro das URLs) e seção de deploy no README | PR #5 | Concluído |
| Documentos da entrega E8: relatório, evidências de teste, retrospectiva e este relatório individual | PR #5 | Concluído |

## 2. Rituais que participei

- [ ] Dailies/weeklies — não houve rituais formais na Sprint 4; a comunicação da equipe foi realizada por WhatsApp.
- [ ] Sprint Review — [confirmar com o grupo]
- [ ] Retrospectiva — registrada no repositório (`relatorios/sprint-4-retrospectiva.md`).

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| PR #4 (merge da Sprint 3) | Equipa | Resolvi os conflitos mantendo o contrato de IA do grupo e somando o dashboard — revisei o diff antes do merge |

## 4. Dificuldades e o que aprendi

Nesta sprint o trabalho foi mais maduro: em vez de implementar algo paralelo, li o que já existia na main (a integração do frontend e o serviço de IA do Gabriel) e construí em cima — a evolução (#10) encaixou direto no router do dashboard que eu mesmo tinha entregue na Sprint 3. O aprendizado técnico foi deixar o deploy como "artefatos versionados + guia", em vez de tentar publicar sozinho: Procfile, runtime.txt e /health no código; o passo a passo das contas na plataforma ficou documentado em docs/deploy.md para a equipe executar junta. Aprendi também a escrever o relatório marcando honestamente o que está pronto e o que ainda depende de ação externa (as URLs de produção) — o professor valoriza rastreabilidade mais do que um texto que parece 100% pronto.
