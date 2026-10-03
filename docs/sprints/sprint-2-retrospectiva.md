# Ata de Retrospectiva — Sprint 2 — SimulaAI

**Data:** 02/10/2026
**Presentes:** [confirmar com o grupo — equipe: Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraifa Fifolato (2840482421022)]

## 1. Ações da retrospectiva anterior (Sprint 1) — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Criar commits pequenos e uma PR revisável para cada frente de trabalho | Em aplicação | Backend organizado em branch `feature/backend-sprints-1-2` com PR revisável; PR do frontend aguardando o Cesar |
| Definir contrato das rotas de simulados, tentativas, respostas e correção | **Aplicada** | Rotas implementadas na Sprint 2 (`/simulados`, `/tentativas`) e documentadas no Swagger (`/docs`) |
| Substituir os dados locais do fluxo do aluno por serviços de API | Pendente | Responsável: Cesar (Front-End), com apoio do backend — contrato pronto em `/docs` |
| Criar testes de interface para validações e registrar execução no CI | Pendente | Ação mantida para a Sprint 3 |
| Registrar presença, Sprint Review, retrospectiva e revisões de PR no encerramento | Em aplicação | Esta ata e os relatórios individuais desta entrega estão no repositório |

## 2. O que funcionou bem

- O fluxo do simulado ficou completo de ponta a ponta: iniciar → responder → finalizar com correção.
- A regra "a resposta correta só é revelada na correção" protege a integridade do simulado (não vaza na interface).
- A correção objetiva não depende de serviço externo — o CT08 cobre o critério de aceite da história #6.
- A suíte de testes cresceu de 19 para 31 testes sem quebrar os anteriores (regressão garantida).

## 3. O que não funcionou

- A sprint passou por atraso de agenda (prazo estendido pelo professor); a integração frontend↔backend não começou.
- O frontend (branch do Cesar) ainda não foi commitado com PR nem integrado à API.
- Ainda não há CI (GitHub Actions) nem conexão com o Supabase.

## 4. Ações para a próxima sprint (Sprint 3)

| Ação | Responsável |
|---|---|
| Integrar o frontend à API: substituir os dados em memória por chamadas a `/auth`, `/simulados` e `/tentativas` | Cesar (Front-End), com apoio de Vinicius (Backend) |
| Implementar a explicação por IA (história #7) com fallback — a correção objetiva nunca para | Gabriel (PO/Backend) e Vinicius (Backend) |
| Histórico de tentativas e dashboard de desempenho (histórias #8 e #9) | Vinicius (Backend) e Davi (Banco de dados) |
| Configurar CI (GitHub Actions) executando pytest a cada PR | Davi (Scrum Master) |
| Conectar o Supabase (`DATABASE_URL`) e validar o schema no banco real | Davi (Banco de dados) |
| Registrar presenças e revisões de PR no encerramento da Sprint 3 | Toda a equipe |
