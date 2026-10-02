# Plano de Testes — SimulaAI

**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)

## 1. Estratégia

| Tipo de teste | O que cobre | Ferramenta | Quando roda |
|---|---|---|---|
| Unitário | Regras de negócio isoladas: autenticação, correção, cálculo de aproveitamento e explicação por IA | Pytest no backend e Vitest/Jest no frontend | A cada PR e no CI |
| Integração | Rotas da API, autorização por perfil e persistência no PostgreSQL de teste | Pytest + HTTPX/TestClient | A cada PR, a partir da Sprint 1 |
| Manual/aceitação | Fluxos de aluno e administrador, responsividade e critérios de aceite do backlog | Roteiro manual e evidências por sprint | Ao final de cada sprint e na bateria final |

As camadas são verificadas em conjunto: regra de negócio nos testes unitários, validações de entrada e autorização nos testes de integração, persistência e constraints no banco, e fluxo completo nos testes manuais.

## 2. Critério de bloqueio de merge

Nenhum PR deve ser aceito na `main` se:

- algum teste automatizado existente falhar;
- uma regra nova for adicionada sem teste correspondente;
- houver falha de autorização entre Aluno e Administrador;
- uma migration ou alteração no schema quebrar a criação do banco;
- um critério de aceite de prioridade Must não for atendido ou estiver sem evidência.

## 3. Casos de teste planejados

| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|---|---:|---|---|---|---|
| CT01 | #1 | Usuário autentica com credenciais válidas | E-mail e senha cadastrados | Acesso concedido com o perfil correto | Alta |
| CT02 | #1 | Usuário tenta acessar função de outro perfil | Aluno acessando rota administrativa | Backend recusa com erro de autorização | Alta |
| CT03 | #2 | Cadastro de matéria ou assunto sem campo obrigatório | Nome vazio | Interface e API recusam o cadastro | Alta |
| CT04 | #3 | Questão sem alternativa correta ou com duas corretas | Alternativas com `correta=false` em todas ou em duas | Cadastro recusado por validação | Alta |
| CT05 | #4 | Aluno inicia simulado com questões cadastradas | Simulado publicado com questões objetivas | Tentativa é criada e questões são exibidas | Alta |
| CT06 | #5 | Aluno responde uma questão | Alternativa válida associada à questão | Resposta é persistida na tentativa correta | Alta |
| CT07 | #6 | Aluno finaliza simulado com acertos e erros | Respostas corretas e incorretas | Sistema calcula acertos, erros e percentual corretamente | Alta |
| CT08 | #6 | Serviço de IA está indisponível ao finalizar | Timeout ou erro da API de IA | Correção objetiva é concluída e erro da IA é tratado | Alta |
| CT09 | #7 | Aluno erra uma questão | Questão, resposta escolhida e correta cadastradas | Explicação é gerada para pelo menos 90% das respostas elegíveis | Alta |
| CT10 | #8 | Aluno consulta tentativas anteriores | Usuário com duas tentativas finalizadas | Apenas o histórico do aluno é exibido com resultados | Média |
| CT11 | #9 | Aluno consulta o dashboard | Tentativas em matérias e assuntos diferentes | Totais, acertos, erros e agrupamentos são calculados corretamente | Alta |
| CT12 | #10 | Aluno compara tentativas | Duas tentativas com percentuais diferentes | Evolução é apresentada usando dados persistidos | Média |
| CT13 | #11 | Usuário acessa a aplicação em viewport menor | Navegador desktop e celular | Fluxos principais permanecem utilizáveis e responsivos | Média |

*(A partir da E5, cada caso executado deve receber resultado e evidência em `docs/sprints/sprint-N-evidencias-teste.md`.)*