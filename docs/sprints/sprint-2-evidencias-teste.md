# Evidências de Teste — Sprint 2 — SimulaAI

**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)

## 1. Casos do plano de testes (docs/plano-de-testes.md)

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT05 | Aluno inicia simulado com questões cadastradas | Integração (pytest) | **Passou** | `backend/tests/test_simulados.py::test_ct05_aluno_inicia_simulado_e_questoes_sao_exibidas` — tentativa criada (201, EM_ANDAMENTO); questões devolvidas na ordem cadastrada e SEM a marcação de correta (não vaza na interface) |
| CT06 | Aluno responde uma questão | Integração (pytest) | **Passou** | `test_ct06_resposta_e_persistida_na_tentativa` (resposta persistida), `test_ct06_responder_de_novo_substitui_a_resposta` (uma escolha por questão), `test_ct06_questao_de_fora_do_simulado_e_recusada` e `test_ct06_alternativa_de_outra_questao_e_recusada` (422) |
| CT07 | Aluno finaliza simulado com acertos e erros | Integração (pytest) | **Passou** | `test_ct07_finalizar_calcula_acertos_erros_e_percentual` — 1 acerto + 1 erro = 50.0 de aproveitamento; status FINALIZADO com data de fim; a correção agora revela as alternativas corretas |
| CT08 | Serviço de IA indisponível ao finalizar | Integração (pytest) | **Passou** | `test_ct08_finalizar_funciona_sem_servico_de_ia` — sem `AI_API_KEY` configurada, a correção objetiva é concluída normalmente (a correção usa somente a resposta correta cadastrada no banco, sem serviço externo) |
| CT09 | Aluno erra uma questão e recebe explicação | Integração | Fora do escopo da Sprint 2 | História #7 planejada para a Sprint 3 |
| CT10 | Aluno consulta tentativas anteriores | Integração | Fora do escopo da Sprint 2 | História #8 planejada para a Sprint 3 (a base `GET /tentativas` já existe) |
| CT11 | Aluno consulta o dashboard | Integração | Fora do escopo da Sprint 2 | História #9 planejada para a Sprint 3 |
| CT12 | Aluno compara tentativas | Integração | Fora do escopo da Sprint 2 | História #10 planejada para a Sprint 4 |
| CT13 | Usuário acessa a aplicação em viewport menor | Manual / responsividade | Não executado | Depende da integração frontend↔backend (ação da Sprint 3) |

## 2. Cobertura automatizada nesta sprint

- Suíte pytest: **31 testes (19 da Sprint 1 + 12 novos), 100% aprovados** na execução local de 02/10/2026 (comando: `python -m pytest`, na pasta `backend/`).
- Regressão garantida: as histórias da Sprint 1 (autenticação, autorização, CRUDs) continuam cobertas pela suíte.
- A execução no CI (GitHub Actions) e a medição formal de cobertura ficaram como ação da Sprint 3 (ver retrospectiva).

## 3. Como reproduzir

```powershell
# na pasta backend/ do repositório, com Python 3.12+
python -m pip install -r requirements.txt
python -m pytest
```
