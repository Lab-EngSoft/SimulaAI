# Evidências de Teste — Sprint 4 — SimulaAI

**Execução:** 17/10/2026, local (`python -m pytest -v` na pasta `backend/`) e via GitHub Actions (workflow `testes`).

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT13 | Evolução: 3 simulados diferentes finalizados (0%, 50%, 100%) aparecem em ordem cronológica com variação ponto a ponto (+50, +50), `variacao_total` +100 e `tendencia` = "melhorando"; tentativa em andamento NÃO entra na linha do tempo | Integração | Passou | `backend/tests/test_sprint4.py::test_ct13_evolucao_cronologica_com_variacao` |
| CT14 | Evolução isolada por aluno (outro aluno vê `sem_dados`) e admin recebe 403 | Integração | Passou | `backend/tests/test_sprint4.py::test_ct14_evolucao_isolada_por_aluno_e_bloqueada_para_admin` |
| — | Health check `/health` para monitoramento do deploy | Integração | Passou | endpoint em `backend/app/main.py` |
| CT01–CT12 | Regressão completa das sprints 1–3 | Integração | Passou | Suíte completa: 49/49 |

## Cobertura automatizada nesta sprint

- **49 testes, 100% aprovados** na execução local de 17/10/2026.
- CI (GitHub Actions): a cada push/PR para a main a suíte roda inteira sem `NVIDIA_API_KEY` — prova de que correção funciona sem IA.
- Deploy (história #11): artefatos prontos (`backend/Procfile`, `backend/runtime.txt`, `/health`) e roteiro em `docs/deploy.md`; a publicação em si gera evidência visual (URL + prints) a ser anexada no E9/E10 após a execução pela equipe.
