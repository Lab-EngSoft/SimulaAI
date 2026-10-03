# Ata de Retrospectiva — Sprint 1 — SimulaAI

**Data:** 02/10/2026  
**Presentes:** participação a confirmar antes da entrega — equipe prevista: Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Não se aplica | — | Não foi localizada ata de retrospectiva de sprint anterior no repositório. |

## 2. O que funcionou bem

- O backlog separa com clareza as histórias Must da Sprint 1: autenticação por perfil, matérias/assuntos e questões/alternativas.
- O roteiro do protótipo no Figma serviu como referência para organizar o fluxo e a interface administrativa.
- A base React + TypeScript foi criada com tela de login, dashboard administrativo e operações locais de conteúdo.
- A compilação de produção e a análise estática concluíram sem erros (`npm run build` e `npm run lint`).

## 3. O que não funcionou

- A autenticação e o CRUD ainda usam somente dados em memória; não há API FastAPI, persistência PostgreSQL ou autorização real.
- Ainda não existe suíte automatizada, CI ou evidência de teste manual em navegador para os critérios de aceite.
- As alterações da Sprint 1 ainda precisam ser organizadas em commits e PRs individuais para permitir rastreabilidade da contribuição da equipe.
- Presenças e participação nos rituais não foram registradas no repositório durante a sprint.

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Criar commits pequenos e uma PR revisável para cada frente de trabalho antes de encerrar a sprint. | Toda a equipe; acompanhamento de Davi (Scrum Master) |
| Definir contrato das rotas de simulados, tentativas, respostas e correção para integrar frontend e FastAPI. | Gabriel (PO/Backend) e Vinicius (Backend) |
| Substituir os dados locais do fluxo do aluno por serviços de API, mantendo estados de carregamento e erro na interface. | Cesar (Front-End), com apoio do backend |
| Criar testes de interface para validações e registrar execução no CI. | Cesar (Front-End) e Davi (Qualidade/SM) |
| Registrar presença, Sprint Review, retrospectiva e revisões de PR no encerramento da Sprint 2. | Toda a equipe; acompanhamento de Davi (Scrum Master) |
