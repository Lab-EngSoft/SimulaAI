# Ata de Retrospectiva — Sprint 4 — SimulaAI

**Data:** 17/10/2026 (registrada junto à entrega; revisar na Sprint Review com o grupo)
**Presentes:** [confirmar com o grupo — Gabriel Reis de Souza, Cesar Augusto Saraiva Fifolato, Davi Sousa Cirilo, Vinicius Brasileiro Veras]

## 1. Ações da retrospectiva da Sprint 3 — aplicadas?

| Ação decidida | Aplicada? | Evidência |
|---|---|---|
| Concluir o dashboard (história #9) | Sim | PR #4 mergeada — `GET /dashboard` + CT12 |
| CI com pytest a cada PR | Sim | `.github/workflows/tests.yml` ativo na main |
| Definir combinado semanal síncrono | Parcialmente | [confirmar com o grupo] |
| Enviar relatórios individuais atrasados | Sim (maioria) | relatórios de todos na pasta `relatorios/` — faltam konferir os da sprint 3 do Cesar |
| Integrar frontend à API | Sim | `frontend/src/api.ts` na main, consumindo os endpoints reais |

## 2. O que funcionou bem

- A resolução de conflito da PR #4 mostrou que o fluxo branch → PR → review → merge está funcionando: o contrato de IA do grupo foi preservado e a contribuição complementar (dashboard) entrou limpa, com 47 testes verdes no merge.
- O CI deu visibilidade imediata — cada push na main roda a suíte inteira.
- Preparar o deploy como artefatos versionados (Procfile, runtime.txt, /health, guia) deixou a publicação como tarefa operacional simples.

## 3. O que não funcionou

- **Timeouts de inferência da API NVIDIA** na geração real de explicações — a história #7 segue parcial; precisa de investigação (modelo alternativo, timeout maior ou outro provedor).
- Comunicação seguemajoritariamente assíncrona (WhatsApp); o deploy em 3 plataformas diferentes é exatamente o tipo de tarefa que precisa de um combinado síncrono.
- O deploy ainda não foi executado — sem URL pública, o requisito do Manual §3 e o E10 ficam bloqueados.

## 4. Ações para a próxima entrega (E9/E10)

| Ação | Responsável |
|---|---|
| Executar o deploy seguindo `docs/deploy.md` (Supabase → Render → Vercel → CORS) e registrar as URLs no README | Vinicius (backend) + Cesar (frontend) |
| Consumir `/dashboard` e `/dashboard/evolucao` nas telas do aluno | Cesar |
| Investigar timeouts da NVIDIA (trocar modelo/provedor ou tratar como indisponível) | Gabriel + Vinicius |
| Rodar o plano de testes completo no sistema publicado e montar as evidências do E9 | Todos |
| Manual do usuário com prints reais do sistema em produção (E10) | Todos |
