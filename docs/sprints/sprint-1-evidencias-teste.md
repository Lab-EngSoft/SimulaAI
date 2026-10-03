# Evidências de Teste — Sprint 1 — SimulaAI

**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)

## 1. Casos do plano de testes (docs/plano-de-testes.md)

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT01 | Usuário autentica com credenciais válidas | Integração (pytest) | **Passou** | `backend/tests/test_auth.py::test_ct01_login_valido_devolve_token_e_perfil_correto` e `test_ct01_login_com_senha_errada_e_recusado` (401 com senha errada) — suíte: `python -m pytest`, 19/19 aprovados, execução local em 02/10/2026 |
| CT02 | Usuário tenta acessar função de outro perfil | Integração (pytest) | **Passou** | `backend/tests/test_auth.py::test_ct02_aluno_nao_acessa_rota_administrativa` (ALUNO recebe 403 em rota de escrita administrativa), `test_ct02_sem_token_e_recusado` (401 sem token) e `test_ct02_aluno_le_dados_mas_nao_escreve` (ALUNO lê, mas não escreve) |
| CT03 | Cadastro de matéria ou assunto sem campo obrigatório | Integração (pytest) | **Passou** | `backend/tests/test_materias.py::test_ct03_materia_sem_nome_e_recusada` e `test_ct03_assunto_sem_nome_e_recusado` — API responde 422 sem tocar o banco |
| CT04 | Questão sem alternativa correta ou com duas corretas | Integração (pytest) | **Passou** | `backend/tests/test_questoes.py::test_ct04_questao_sem_alternativa_correta_e_recusada`, `test_ct04_questao_com_duas_corretas_e_recusada` (ambos 422) e `test_ct04_questao_com_uma_correta_e_criada` (201) — a mesma regra é revalidada no PUT em `test_atualizar_alternativas_revalida_regra` |
| CT05 | Aluno inicia simulado com questões cadastradas | Integração | Fora do escopo da Sprint 1 | História planejada para a Sprint 2 |
| CT06 | Aluno responde uma questão | Integração | Fora do escopo da Sprint 1 | História planejada para a Sprint 2 |
| CT07 | Aluno finaliza simulado com acertos e erros | Integração | Fora do escopo da Sprint 1 | História planejada para a Sprint 2 |
| CT08 | Serviço de IA indisponível ao finalizar | Integração | Fora do escopo da Sprint 1 | Depende do backend de simulados (Sprint 2) e da integração de IA (Sprint 3) |
| CT09 | Aluno erra uma questão e recebe explicação | Integração | Fora do escopo da Sprint 1 | História planejada para a Sprint 3 |
| CT10 | Aluno consulta tentativas anteriores | Integração | Fora do escopo da Sprint 1 | História planejada para a Sprint 3 |
| CT11 | Aluno consulta o dashboard | Integração | Fora do escopo da Sprint 1 | História planejada para a Sprint 3 |
| CT12 | Aluno compara tentativas | Integração | Fora do escopo da Sprint 1 | História Should planejada para a Sprint 4 |
| CT13 | Usuário acessa a aplicação em viewport menor | Manual / responsividade | Não executado | Depende da integração frontend↔backend (ação da Sprint 2) |
| FE01 | Compilação do frontend para produção | Build | Passou | `npm run build` concluído em 02/10/2026, gerando `frontend/dist/` (branch `feature/frontend-sprint-1`) |
| FE02 | Análise estática do frontend | Lint | Passou | `npm run lint` concluído em 02/10/2026 sem apontamentos (branch `feature/frontend-sprint-1`) |

## 2. Cobertura automatizada nesta sprint

- Suíte pytest do backend: **19 testes, 100% aprovados** na execução local de 02/10/2026 (comando: `python -m pytest`, na pasta `backend/`).
- Escopo coberto pela suíte: autenticação/autorização (CT01, CT02), CRUD de matérias e assuntos com validações (CT03), CRUD de questões com regra de alternativa única correta (CT04), além de regressões de CRUD completo, integridade de e-mail duplicado, cascata de exclusão e seed de demonstração.
- A execução no CI (GitHub Actions) e a medição formal de cobertura de linhas ficaram como ação da Sprint 2 (ver retrospectiva).

## 3. Como reproduzir

```powershell
# na pasta backend/ do repositório, com Python 3.12+
python -m pip install -r requirements.txt
python -m pytest
```
