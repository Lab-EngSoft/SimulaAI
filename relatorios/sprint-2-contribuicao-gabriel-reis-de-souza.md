# Relatório Individual de Contribuição — Sprint 2 — Gabriel Reis de Souza (RA 2840482421005)

**Papel nesta sprint:** Organização técnica / Qualidade

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Análise e planejamento da reorganização da estrutura do projeto | [adicionar commit/PR] | Concluído |
| Organização do frontend em pasta dedicada | [adicionar commit/PR] | Concluído |
| Revisão da estrutura existente do backend após reorganização | [adicionar commit/PR ou evidência] | Concluído |
| Execução da suíte automatizada do backend | Evidência local: `python -m pytest` | 31/31 testes passaram |
| Validação das funcionalidades já cobertas pelos testes automatizados | Evidência local / log de testes | Concluído |

## 2. Rituais que participei

- [ ] Dailies/weeklies
- [x] Sprint Review
- [x] Retrospectiva


## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| [adicionar PR, se houver] | [autor] | [comentário] |

Caso não tenha revisado nenhum PR:

Nenhum PR de colega foi revisado formalmente nesta sprint.

## 4. Dificuldades e o que aprendi

Durante a preparação dos testes, o comando direto `pytest` apresentou problema para localizar o módulo `app`.

A execução com:

`python -m pytest`

permitiu utilizar corretamente o ambiente Python do projeto e executar toda a suíte de testes.

Também foi necessário tomar cuidado durante a reorganização das pastas para não quebrar imports, caminhos de arquivos ou configurações do frontend e backend.

Aprendi a importância de validar alterações estruturais com testes automatizados antes de integrá-las à branch principal.

## Evidência complementar de testes

A suíte localizada em `backend/tests/` foi executada com sucesso.

Resultado:

`31 passed, 1 warning`

Os testes cobriram funcionalidades de autenticação, autorização, matérias, assuntos, questões e fluxo de simulados.

O único aviso encontrado foi relacionado à depreciação na integração entre Starlette e httpx, sem impacto no resultado da suíte.