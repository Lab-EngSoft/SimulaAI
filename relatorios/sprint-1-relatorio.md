# Relatório de Entrega — Sprint 1 — SimulaAI

**Período:** [data de início] a 02/10/2026  
**Sprint Review:** 02/10/2026, com a equipe

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| Autenticação com perfis Aluno e Administrador | Sim | Parcial | Tela de login criada, ainda sem autenticação real integrada ao backend |
| Gerenciamento de matérias e assuntos | Sim | Parcial | Interface criada utilizando dados locais |
| Gerenciamento de questões e alternativas | Sim | Parcial | Interface inicial criada no frontend |
| Realização de simulados | Não | Não | Planejada para a Sprint 2 |
| Registro e correção de respostas | Não | Não | Planejada para a Sprint 2 |

## 2. Incremento funcional demonstrável

Ao final da Sprint 1, o SimulaAI possuía um frontend inicial em React + TypeScript com:

- tela de login;
- dashboard administrativo;
- gerenciamento local de matérias e assuntos;
- gerenciamento local de questões e alternativas;
- estrutura visual baseada no protótipo do Figma.

Nesta sprint, os dados ainda eram mantidos localmente no frontend, sem integração completa com backend e banco de dados.

Para executar localmente:

```bash
npm install
npm run dev
```

Referência do protótipo: `docs/prototipo.md`.

## 3. Backlog atualizado

Ao fim da sprint:

- autenticação permaneceu parcial;
- matérias e assuntos permaneceram parciais;
- questões e alternativas permaneceram parciais;
- integração com backend foi direcionada para a Sprint 2;
- fluxo de simulados foi direcionado para a Sprint 2.

**Board:** [adicionar link ou print]

## 4. Evidências de teste

Nesta sprint, as validações ficaram concentradas principalmente no frontend.

Ainda não havia uma suíte automatizada consolidada para autenticação, CRUDs e simulados.

Detalhamento:

`relatorios/sprint-1-evidencias-teste.md`

## 5. Retrospectiva e contribuição individual

- Retrospectiva: `relatorios/sprint-1-retrospectiva.md`
- Gabriel Reis de Souza: `relatorios/sprint-1-contribuicao-gabriel-reis-de-souza.md`
- Cesar Augusto Saraiva Fifolato: `relatorios/sprint-1-contribuicao-cesar-augusto-saraiva-fifolato.md`
- Vinicius Brasileiro Veras: `relatorios/sprint-1-contribuicao-vinicius-brasileiro-veras.md`

## 6. Riscos/impedimentos para a próxima sprint

- falta de integração entre frontend e backend;
- ausência de persistência real dos dados;
- ausência de testes automatizados;
- necessidade de implementar o fluxo de simulados;
- baixa rastreabilidade de algumas contribuições devido a commits grandes.