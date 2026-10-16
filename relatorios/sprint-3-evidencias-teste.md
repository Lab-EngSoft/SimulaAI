# Evidências de Teste — Sprint 3 — SimulaAI

**Execução:** 03/10/2026, local (`python -m pytest -v` na pasta `backend/`) e via GitHub Actions (workflow `testes`).

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT09 | Erro explicado com fallback — sem `AI_API_KEY`, a resposta errada sai com explicação construída dos dados do banco (cita a alternativa correta); a correta não recebe explicação; endpoint recusa tentativa em andamento (409) | Integração | Passou | `backend/tests/test_sprint3.py::test_ct09_explicacao_fallback_sem_ia` |
| CT09b | Cobertura do critério "explicar ≥ 90% das respostas incorretas" — com todos os erros, 100% saem explicados sem IA | Integração | Passou | `backend/tests/test_sprint3.py::test_ct09_cem_por_cento_dos_erros_explicados` |
| CT10 | Explicação via IA — com `AI_API_KEY` configurada (provedor simulado no teste), o texto retornado pela IA é armazenado em `resposta.explicacao_ia` | Integração (mock) | Passou | `backend/tests/test_sprint3.py::test_ct10_explicacao_via_ia` |
| CT11 | Histórico — tentativas de **simulados diferentes** aparecem com seus resultados (50% e 100%); outro aluno autenticado vê lista vazia e recebe 403 na tentativa alheia | Integração | Passou | `backend/tests/test_sprint3.py::test_ct11_historico_com_diferentes_simulados` |
| CT12 | Dashboard — agregação por matéria e assunto confere com os dados (Matemática 1/2, Português 1/1; média 75%); admin recebe 403; aluno sem tentativas recebe painel zerado | Integração | Passou | `backend/tests/test_sprint3.py::test_ct12_dashboard_agrega_por_materia_e_assunto` |
| CT08 (atualizado) | Correção objetiva sem IA — segue 100% funcional sem provedor externo; agora registra também a explicação de fallback nos erros | Integração | Passou | `backend/tests/test_simulados.py::test_ct08_finalizar_funciona_sem_servico_de_ia` |
| CT01–CT07 | Regressão das sprints 1 e 2 | Integração | Passou | Suíte completa: 36/36 |

## Cobertura automatizada nesta sprint

- **36 testes, 100% aprovados** (31 herdados + 5 novos) na execução local de 03/10/2026.
- CI (GitHub Actions, `.github/workflows/tests.yml`): `pip install -r backend/requirements.txt` + `python -m pytest -v` a cada push/PR para a main, **sem `AI_API_KEY` no ambiente** — o CI prova a cada execução que correção e explicações funcionam sem a IA.
- Cenários cobertos nesta sprint: fallback sem chave, IA simulada, recusa de explicação antes da finalização, isolamento de dados entre alunos, agregação por matéria/assunto e painel zerado.
