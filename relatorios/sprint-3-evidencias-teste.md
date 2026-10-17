# Evidências de Teste — Sprint 3 — SimulaAI

**Execução:** 16/10/2026, local (`python -m pytest -v` na pasta `backend/`) e via GitHub Actions (workflow `testes`).

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT09 (contrato de IA) | Sem `NVIDIA_API_KEY`: status indisponível, explicações devolvem 503 e a correção/nota permanece intacta | Integração | Passou | `backend/tests/test_ia_contract.py::test_status_indisponivel_e_endpoint_nao_modifica_nota` |
| CT09 (provedor injetado) | Com provedor falso injetado, a explicação é persistida em `resposta.explicacao_ia` e não gera nova requisição para o que já foi explicado | Integração (mock) | Passou | `backend/tests/test_ia_contract.py::test_injecao_de_provedor_persiste_explicacao` |
| — | Resultado protegido: 409 antes de finalizar, 401 sem token, 200 após | Integração | Passou | `backend/tests/test_ia_contract.py::test_resultado_protegido_antes_e_depois` |
| CT11 | Histórico — tentativas de **simulados diferentes** aparecem com seus resultados (50% e 100%); outro aluno autenticado vê lista vazia e recebe 403 na tentativa alheia | Integração | Passou | `backend/tests/test_sprint3.py::test_ct11_historico_com_diferentes_simulados` |
| CT12 | Dashboard — agregação por matéria e assunto confere com os dados (Matemática 1 acerto/2 respondidas, Português 1/1; média 75%); admin recebe 403; aluno sem tentativas recebe painel zerado | Integração | Passou | `backend/tests/test_sprint3.py::test_ct12_dashboard_agrega_por_materia_e_assunto` |
| — | Integração frontend/backend: gabarito não vaza para o aluno, edição de questão troca assunto, fluxo real admin→aluno com persistência | Integração | Passou | `backend/tests/test_integracao.py` (3 testes) |
| — | CRUD administrativo de simulados com restrições de integridade | Integração | Passou | `backend/tests/test_admin_simulados.py` |
| CT01–CT08 | Regressão das sprints 1 e 2 (correção objetiva segue funcionando sem IA — CT08) | Integração | Passou | Suíte completa: 47/47 |

## Cobertura automatizada nesta sprint

- **47 testes, 100% aprovados** na execução local de 16/10/2026 (suíte combinada: sprints 1–2 + contribuições da Sprint 3 de todos os integrantes).
- CI (GitHub Actions, `.github/workflows/tests.yml`): `pip install -r backend/requirements.txt` + `python -m pytest -v` a cada push/PR para a main, **sem `NVIDIA_API_KEY` no ambiente** — cada execução prova que a correção objetiva funciona sem a IA.
- Observação registrada no relatório da sprint: a geração **real** de explicações pela API da NVIDIA apresentou timeouts de inferência (ReadTimeout/APITimeoutError) nos testes do grupo; os testes automatizados cobrem o contrato com provedor simulado, e a investigação ficou registrada como pendência para a Sprint 4.
