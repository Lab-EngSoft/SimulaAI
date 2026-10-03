# Relatório de Entrega — Sprint 2 — SimulaAI

**Período:** [data de início] a 02/10/2026  
**Sprint Review:** 02/10/2026, com a equipe

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| Autenticação com perfis Aluno e Administrador | Sim | Sim | Login, registro e autorização implementados no backend |
| Gerenciamento de matérias e assuntos | Sim | Sim | CRUD implementado e testado |
| Gerenciamento de questões e alternativas | Sim | Sim | CRUD e validação de alternativa correta implementados |
| Realização de simulados | Sim | Sim | Tentativas podem ser iniciadas e questões são exibidas |
| Registro de respostas | Sim | Sim | Respostas são persistidas e podem ser alteradas |
| Correção e resultado | Sim | Sim | Acertos, erros e percentual são calculados |
| Explicação por IA | Sim | Parcial | Indisponibilidade da IA não impede a correção objetiva |

## 2. Incremento funcional demonstrável

Ao final da Sprint 2, o backend FastAPI suportava:

- login e registro;
- autorização por perfil;
- CRUD de matérias e assuntos;
- CRUD de questões e alternativas;
- início de tentativa de simulado;
- registro e alteração de respostas;
- finalização de tentativa;
- cálculo de acertos, erros e percentual.

Também foi realizada a reorganização do repositório, separando melhor:

```text
frontend/
backend/
database/
docs/
relatorios/
```

Para executar os testes:

```bash
cd backend
source .venv/bin/activate
python -m pytest
```

Resultado:

```text
31 passed, 1 warning
```

## 3. Backlog atualizado

Ao fim da sprint:

- autenticação e autorização foram concluídas no backend;
- CRUD de matérias e assuntos foi concluído;
- CRUD de questões e alternativas foi concluído;
- fluxo básico de simulados foi concluído;
- registro e correção das respostas foram concluídos;
- integração completa do frontend com a API permaneceu pendente;
- histórico e dashboard de desempenho permaneceram para sprints futuras.

**Board:** [adicionar link ou print]

## 4. Evidências de teste

Foram executados 31 testes automatizados no backend, todos aprovados.

Os testes cobriram:

- CT01 — autenticação;
- CT02 — autorização;
- CT03 — matérias e assuntos;
- CT04 — questões e alternativas;
- CT05 — início de simulado;
- CT06 — registro de resposta;
- CT07 — cálculo do resultado;
- CT08 — funcionamento sem serviço de IA.

Detalhamento:

`relatorios/sprint-2-evidencias-teste.md`

## 5. Retrospectiva e contribuição individual

- Retrospectiva: `relatorios/sprint-2-retrospectiva.md`
- Gabriel Reis de Souza: `relatorios/sprint-2-contribuicao-gabriel-reis-de-souza.md`
- Vinicius Brasileiro Veras: `relatorios/sprint-2-contribuicao-vinicius-brasileiro-veras.md`

Cesar Augusto Saraiva Fifolato não teve contribuição registrada nesta sprint.

## 6. Riscos/impedimentos para a próxima sprint

- integrar o frontend ao backend real;
- substituir dados locais restantes;
- implementar histórico de tentativas;
- implementar dashboard de desempenho do aluno;
- concluir integração com IA;
- configurar CI para execução automática dos testes.