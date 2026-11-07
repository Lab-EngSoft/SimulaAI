# Relatório de Entrega — Sprint 4 — SimulaAI

**Período:** 17/10/2026 a 30/10/2026
**Sprint Review:** [confirmar com o grupo]

## 1. Planejado vs. entregue

| História (backlog) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #10 Como aluno, quero acompanhar minha evolução entre tentativas | Sim | Sim (backend) | `GET /dashboard/evolucao`: linha do tempo das tentativas finalizadas em ordem cronológica, cada uma com simulado, acertos, erros, percentual e variação em pontos percentuais; resumo com `variacao_total` e `tendencia` (melhorando/estável/piorando). Dados 100% do histórico persistido. A tela no frontend fica com o Cesar |
| #11 Acesso público por URL (deploy) | Sim | Preparado — execução pendente | Backend pronto para produção: `backend/Procfile`, `backend/runtime.txt`, endpoint `/health`, guia passo a passo em `docs/deploy.md` (Render + Supabase + Vercel). A criação das contas e a publicação ficam com a equipe — URLs reais devem ser registradas no README após o deploy |
| #7 Explicações por IA | Pendente da Sprint 3 | Em aberto | Estrutura pronta (`services/ia.py`, provedor injetável, contrato testado). Problema conhecido: timeouts de inferência da API NVIDIA — investigar provedor/modelo alternativo na próxima sprint |
| #9 Dashboard | Concluída na Sprint 3 (PR #4) | Mantida | Suíte de regressão segue verde |

## 2. Incremento funcional demonstrável

- **Evolução (história #10):** `GET /dashboard/evolucao` devolve a série temporal do aluno logado — comparar desempenho entre simulados ficou trivial (variação ponto a ponto).
- **Pronto para deploy (história #11):** `Procfile` + `runtime.txt` + `/health` deixam o backend publicável no Render com um clique; `docs/deploy.md` tem o roteiro completo (Supabase → Render → Vercel → CORS).

**Como reproduzir:** ver `README.md` e `docs/integracao-local.md` (execução local integrada). Roteiro da evolução: login como aluno → finalizar 2+ simulados → `GET /dashboard/evolucao`.

## 3. Backlog atualizado

- #10 — **concluída (backend)** nesta sprint.
- #11 — **pronta para deploy**; falta executar nas plataformas e registrar a URL.
- #7 — parcial; pendência: timeouts da NVIDIA.

## 4. Evidências de teste

CT13–CT14 implementados como testes automatizados — **2 testes novos; suíte total: 49 testes, 100% aprovados** (execução local de 17/10/2026) + CI no GitHub Actions. Detalhe em `relatorios/sprint-4-evidencias-teste.md`.

## 5. Retrospectiva e contribuição individual

- Ata de retrospectiva: `relatorios/sprint-4-retrospectiva.md`
- Relatórios individuais: `relatorios/sprint-4-contribuicao-<nome>.md` *(cada integrante preenche o seu)*

## 6. Riscos/impedimentos para a próxima entrega (E9/E10)

- **Deploy precisa acontecer de fato** (contas Render/Supabase/Vercel da equipe) — sem URL pública, o requisito do Manual não é atendido e o E10 (manual com prints do sistema em produção) fica bloqueado.
- Timeouts da API NVIDIA na geração real de explicações.
- Frontend precisa consumir `/dashboard` e `/dashboard/evolucao` (telas de desempenho/evolução).
- Relatórios individuais pendentes de alguns integrantes nas sprints anteriores.
