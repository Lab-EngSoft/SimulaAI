# Ata de Retrospectiva — Sprint 3 — SimulaAI

**Data:** 03/10/2026 (retrospectiva registrada junto à entrega; revisar na Sprint Review com o grupo)
**Presentes:** [confirmar com o grupo — Gabriel Reis de Souza, Cesar Augusto Saraiva Fifolato, Davi Sousa Cirilo, Vinicius Brasileiro Veras]

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Implementar a explicação por IA com fallback (história #7), mantendo a correção objetiva independente de serviço externo | Sim | `backend/app/services/explicacao_ia.py` — fallback determinístico coberto pelo CT09; correção segue sem IA (CT08) |
| Documentar o contrato da API para a integração do frontend | Sim | Swagger em `/docs` + endpoints novos documentados; contrato do dashboard e das explicações pronto para o Cesar consumir |
| Executar pytest automaticamente a cada PR (CI) | Sim | `.github/workflows/tests.yml` — 36 testes por push/PR, sem chave de IA no ambiente |
| Cada integrante enviar o próprio relatório individual de contribuição | Parcialmente | Relatórios de Gabriel e Davi continuam pendentes; com a pasta `relatorios/` organizada, o envio ficou simples — prioridade para a Sprint 4 |

## 2. O que funcionou bem

- O desenho da Sprint 2 "correção sem IA" pagou de novo: o fallback da história #7 reusou a mesma filosofia e o CT08 continuou passando durante toda a implementação.
- Agregação do dashboard feita no banco (JOIN + GROUP BY) ficou simples e testável — sem carregar tudo em memória.
- A entrega conjunta autorizada das Sprints 1 e 2 liberou a Sprint 3 para começar adiantada; parte do trabalho já foi feita no dia seguinte à entrega.

## 3. O que não funcionou

- A comunicação do grupo segue acontecendo só por WhatsApp, sem dailies/weeklies — funcionou até aqui, mas a integração frontend↔backend da Sprint 4 exige pelo menos um combinado síncrono por semana.
- Os relatórios individuais de Gabriel e Davi (Sprints 1 e 2) ainda não foram enviados; o fator de contribuição de cada um precisa dessa evidência.
- O frontend continua sem consumir a API real — é o maior risco do MVP (história #11).

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Definir 1 combinado semanal síncrono (mesmo curto) até o fim da Sprint 4 | Gabriel (facilitador) |
| Enviar os relatórios individuais atrasados (Sprints 1–3) de cada integrante | Gabriel e Davi |
| Integrar as telas React à API (login, CRUDs, fluxo do simulado, dashboard) e preparar o deploy público (história #11) | Cesar, com apoio do backend |
| Implementar a evolução entre tentativas (história #10) sobre o histórico existente | Vinicius |
| Cadastrar `AI_API_KEY` como segredo do provedor de deploy e conectar o PostgreSQL/Supabase via `DATABASE_URL` | Vinicius |
