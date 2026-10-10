# Relatório de Entrega — Sprint 3 — SimulaAI

**Período:** 02/10/2026 a 09/10/2026 
**Responsável pelas atividades descritas:** Gabriel Reis de Souza e Davi Cirilo
**Projeto:** SimulaAI 

## 1. Planejado vs. entregue

Durante esta sprint, nossas atividades foram concentradas na integração entre frontend e backend, implementação do gerenciamento administrativo de simulados, disponibilização das funcionalidades aos alunos e desenvolvimento da estrutura de integração com inteligência artificial. E a conexão do BD ao supabase

As entregas foram relacionadas às histórias previstas no backlog do projeto, considerando também funcionalidades técnicas complementares e pendências da sprint anterior.

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #4 — Realização de simulados | Não, prevista na Sprint 2 | Sim, com melhorias | Integração frontend/backend e implementação do gerenciamento administrativo de simulados. |
| #5 — Registro de respostas | Não, prevista na Sprint 2 | Sim, integração concluída | Registro das alternativas selecionadas pelo aluno por meio da API. |
| #6 — Correção automática | Não, prevista na Sprint 2 | Sim, integração concluída | Correção e apresentação dos resultados na interface, independentemente da IA. |
| #7 — Explicações por IA | Sim | Parcialmente | Estrutura modular e comunicação implementadas, porém geração efetiva comprometida por timeouts da API externa. |
| #8 — Histórico de tentativas | Sim | Sim | Consulta de tentativas anteriores, resultados e continuidade de simulados em andamento. |
| #9 — Dashboard de desempenho | Sim | Não concluído nesta contribuição | Resultados individuais estão disponíveis, mas ainda não foi implementado um dashboard completo com desempenho por matéria e assunto. |

Além das histórias previstas, foram realizadas atividades técnicas complementares:

- Integração das funcionalidades React com os endpoints FastAPI.
- Implementação do CRUD administrativo de simulados, com seleção, filtragem e ordenação de questões.
- Validação das permissões de acesso entre os perfis Aluno e Administrador.
- Implementação de restrições para preservar simulados com tentativas já registradas.
- Preparação da arquitetura para integração com diferentes provedores de IA.

**[PREENCHIMENTO POSTERIOR — INTEGRAÇÃO SUPABASE]**



## 2. Incremento funcional demonstrável

O incremento desenvolvido nesta sprint ampliou as funcionalidades disponíveis no SimulaAI, permitindo a utilização integrada do frontend React com o backend FastAPI.

### Integração frontend e backend

Foi realizada a integração das interfaces de autenticação, administração e utilização dos simulados com os endpoints disponibilizados pelo backend.

A aplicação passou a utilizar os dados e as regras de negócio fornecidos pela API, substituindo os comportamentos demonstrativos anteriores nas funcionalidades integradas.

Essa implementação permite validar as permissões dos usuários no backend e utilizar os registros persistidos no banco configurado para a aplicação.

### Gerenciamento administrativo de simulados

Foi implementada a funcionalidade de criação e gerenciamento de simulados pelo administrador.

O administrador pode:

- Criar simulados utilizando questões previamente cadastradas.
- Selecionar questões e filtrá-las por matéria e assunto.
- Definir e alterar a ordem de apresentação das questões.
- Editar informações e excluir simulados, respeitando as restrições de integridade.

Foram implementadas proteções para impedir alterações destrutivas em simulados que já possuem tentativas registradas, preservando a consistência dos resultados dos alunos.

### Funcionalidades do aluno

A área do aluno foi integrada ao fluxo de realização de simulados.

O aluno pode iniciar um simulado, responder às questões, continuar tentativas em andamento, finalizar a avaliação e consultar os resultados calculados pelo backend.

Também foi disponibilizada a consulta ao histórico de tentativas, permitindo visualizar resultados anteriores e respectivos percentuais de aproveitamento.

### Estrutura e integração com inteligência artificial

Foi implementado o serviço `backend/app/services/ia.py`, responsável por estabelecer a comunicação com provedores externos de inteligência artificial.

A estrutura utiliza uma interface de provedor desacoplada das regras de negócio da aplicação, permitindo configurar o serviço e o modelo por meio de variáveis de ambiente.

Inicialmente, foi selecionada a API de prototipagem NVIDIA NIM, utilizando comunicação compatível com o SDK da OpenAI.

A implementação contempla:

- Estrutura de contexto contendo matéria, assunto, enunciado, alternativas, resposta do aluno e gabarito.
- Prompt pedagógico orientado à explicação dos erros.
- Comunicação com modelos externos de linguagem.
- Tratamento de erros e indisponibilidade do provedor.
- Integração com a rota `POST /tentativas/{id}/explicacoes`.
- Estrutura para armazenar as explicações geradas no campo `resposta.explicacao_ia`.
- Independência entre a correção objetiva e o funcionamento do serviço de IA.

A estrutura foi implementada e validada por testes de contrato e de comunicação interna. A aplicação reconheceu corretamente as configurações de autenticação da NVIDIA e conseguiu encaminhar requisições à funcionalidade de explicações.

Entretanto, durante os testes de geração real, foram identificados problemas técnicos de diagnóstico complexo, caracterizados por falhas de tempo limite nas requisições de inferência.

Os erros identificados foram `ReadTimeout` e `APITimeoutError`, que resultaram em respostas HTTP `503 Service Unavailable` na aplicação.

Foram realizados testes com diferentes modelos, incluindo DeepSeek V4.1 Flash e Gemma 4 31B IT. Embora a API tenha respondido às requisições de listagem de modelos, a geração de texto permaneceu indisponível nos testes realizados.

Os problemas também ocorreram em requisições HTTP diretas, sem utilização do SDK Python.

Dessa forma, não foi possível determinar definitivamente se a causa está relacionada à infraestrutura externa, ao ambiente de rede ou a condições específicas do serviço de inferência.

**A estrutura de integração foi concluída, mas a geração efetiva das explicações ainda não atende aos critérios de aceite da história #7**, que exige explicações para pelo menos 90% das respostas incorretas.

A investigação e a busca de uma solução foram previstas para a próxima sprint.

### Execução e demonstração

O sistema pode ser executado localmente utilizando dois servidores:

**Backend FastAPI:**

`python -m uvicorn app.main:app --reload --port 8000`

**Frontend React:**

`npm run dev`

Endereços de desenvolvimento:

- Frontend: `http://localhost:5173`
- Documentação da API: `http://localhost:8000/docs`

**Repositório:** https://github.com/Lab-EngSoft/SimulaAI

**Deploy:** Ainda não realizado. Publicação prevista para a Sprint 4, utilizando Vercel para o frontend e Render para o backend, conforme a história #11.

**[PREENCHIMENTO POSTERIOR — INTEGRAÇÃO SUPABASE]**

Adicionar a demonstração da persistência no PostgreSQL/Supabase quando a integração for concluída e validada.

## 3. Backlog atualizado

Ao final das atividades desenvolvidas nesta sprint, os seguintes estados foram identificados:

| Atividade | Situação |
|---|---|
| Integração frontend/backend | Concluída |
| Autenticação e controle de acesso pela API | Integrados |
| CRUD administrativo de simulados | Concluído |
| Associação e ordenação de questões | Concluída |
| Realização e finalização de simulados | Integradas |
| Correção automática | Integrada |
| Histórico de tentativas | Concluído |
| Dashboard completo de desempenho | Pendente |
| Estrutura modular de IA | Concluída |
| Configuração do provedor NVIDIA | Concluída |
| Geração efetiva de explicações por IA | Bloqueada por falhas de inferência |
| Investigação definitiva dos timeouts | Pendente |
| Avaliação de provedor alternativo de IA | Planejada para a próxima sprint |

A história #7 permanece parcialmente atendida, enquanto a história #9 ainda necessita de implementação complementar para satisfazer todos os seus critérios de aceite.



**[PREENCHIMENTO POSTERIOR — INTEGRAÇÃO SUPABASE]**

Acrescentar as tarefas relacionadas ao banco externo, com os respectivos estados após a conclusão do trabalho.

## 4. Evidências de teste

### Registros técnicos das falhas de integração com IA

Durante os testes de integração com a API NVIDIA NIM, foram registrados erros relacionados ao tempo limite das requisições de inferência.

Ao solicitar a geração de explicações pela interface do SimulaAI, o backend registrou:

POST /tentativas/4/explicacoes HTTP/1.1
503 Service Unavailable
```

Nos testes realizados diretamente pelo terminal, utilizando o SDK Python, foram identificadas as seguintes exceções:


httpcore.ReadTimeout:
The read operation timed out

httpx.ReadTimeout:
The read operation timed out

openai.APITimeoutError:
Request timed out.
```

Para investigar a causa, foram realizadas chamadas independentes ao endpoint da NVIDIA, incluindo a consulta à listagem de modelos disponíveis:

API acessível. Modelos: 80
```

Esse resultado demonstrou que a comunicação com o endpoint de listagem estava funcionando. Entretanto, as requisições de geração de texto continuaram apresentando timeout, inclusive com modelos diferentes e chamadas HTTP diretas.

Os registros não permitem identificar definitivamente a origem do problema, mas demonstram que a falha não está limitada ao fluxo da interface do SimulaAI.

**Situação:** investigação técnica pendente para a próxima sprint.

Foram realizados testes automatizados do backend e procedimentos específicos para validação das funcionalidades implementadas e diagnóstico da integração com IA.

### Testes automatizados

A suíte do backend registrou **45 testes aprovados** na validação realizada após a implementação do gerenciamento administrativo de simulados e da estrutura inicial de IA.

Os testes abrangeram:

- Autenticação e autorização.
- Gerenciamento de matérias e assuntos.
- Cadastro e validação de questões e alternativas.
- Criação, edição e exclusão de simulados.
- Registro e correção automática das respostas.
- Restrições de integridade para simulados com tentativas.
- Contratos do serviço de IA e persistência utilizando provedor simulado.
- Preservação da correção objetiva na ausência da IA.

Esse resultado corresponde à validação automatizada anterior às últimas alterações de configuração do provedor NVIDIA. Portanto, não substitui a necessidade de executar novamente a suíte na versão final.

### Testes de integração com IA

| Teste realizado | Resultado |
|---|---|
| Reconhecimento da variável `NVIDIA_API_KEY` | Aprovado |
| Verificação de disponibilidade pela função `status_ia()` | Aprovado |
| Acionamento da rota de explicações pelo frontend | Requisição recebida pelo backend |
| Listagem de modelos pela API NVIDIA | Aprovado — 80 modelos retornados |
| Geração pelo modelo DeepSeek V4.1 Flash | Falha por timeout |
| Geração pelo modelo Gemma 4 31B IT | Falha por timeout |
| Requisição HTTP direta ao endpoint de inferência | Falha por timeout |
| Geração de explicações pedagógicas no SimulaAI | Não validada com sucesso |

Os resultados indicam que a aplicação reconhece as configurações e executa o fluxo interno de requisições. Entretanto, a geração real de explicações permanece pendente.

A indisponibilidade da IA não impediu a realização dos simulados nem a correção objetiva das respostas.



## 5. Retrospectiva e contribuição individual

### Contribuição individual — Gabriel Reis de Souza

Gabriel Reis: Minha participação nesta sprint concentrou-se na integração das camadas da aplicação, implementação do gerenciamento administrativo de simulados e preparação da infraestrutura de inteligência artificial.
As atividades envolveram alterações nas interfaces React, nos endpoints FastAPI e na estrutura do serviço responsável pela comunicação com provedores de IA.
A implementação do gerenciamento administrativo de simulados representou uma evolução funcional do projeto, permitindo que as avaliações fossem criadas e organizadas diretamente pelo sistema.
Na parte de IA, a principal contribuição foi o desenvolvimento de uma estrutura modular, permitindo que a lógica de geração de explicações permaneça separada da correção automática e das demais regras de negócio.
Durante os testes com a NVIDIA, foram identificadas falhas técnicas de difícil diagnóstico. Para investigá-las, foram realizados testes isolados dos serviços, verificações de configuração, consultas à API, utilização de diferentes modelos e análise das exceções retornadas.
Apesar de não ter sido possível concluir a geração efetiva das explicações, a investigação permitiu verificar que as falhas também ocorriam fora do fluxo normal da aplicação, reduzindo a probabilidade de estarem associadas exclusivamente ao código interno do SimulaAI.

O principal aprendizado foi a necessidade de distinguir a validação da arquitetura interna da disponibilidade operacional de provedores externos.

Também ficou evidente a importância de manter integrações desacopladas, permitindo a eventual substituição de serviços externos sem exigir alterações extensas no restante do sistema.

**Evidências individuais:**

- Commits relacionados às minhas alterações: [Inserir links]
- Pull Requests relacionados às minhas atividades: [Inserir links]
- Relatório individual: `relatorios/sprint-3-contribuicao-gabriel-reis-de-souza.md`

### Referências da retrospectiva

- **Ata de retrospectiva:** `relatorios/sprint-3-retrospectiva.md` — [Inserir link quando disponível]
- **Relatório individual de contribuição:** [Inserir link]

As contribuições dos demais integrantes serão registradas em seus próprios relatórios, conforme as atividades e evidências correspondentes.

## 6. Riscos/impedimentos para a próxima sprint

### 6.1. Instabilidade da API de inteligência artificial

O principal impedimento identificado foi a falha recorrente nas requisições de geração de texto por meio da API de prototipagem da NVIDIA.

Embora a autenticação e a consulta à listagem de modelos tenham funcionado, as operações de inferência apresentaram timeouts, impedindo que a funcionalidade de explicações pedagógicas fosse validada integralmente.

**Ação prevista:** aprofundar a investigação técnica, analisando as condições de conexão, disponibilidade dos endpoints, configuração das requisições e possíveis limitações do serviço externo.

### 6.2. Possível substituição do provedor de IA

Caso a instabilidade da API NVIDIA permaneça, será avaliada a substituição do serviço de prototipagem por uma API privada ou comercial.

A escolha deverá considerar:

- Disponibilidade e confiabilidade operacional.
- Custos e limites de requisições.
- Latência na geração das explicações.
- Compatibilidade com a estrutura existente.
- Segurança e proteção das credenciais.
- Qualidade pedagógica das respostas.

A estrutura modular implementada deverá facilitar a substituição do provedor, sem exigir a reconstrução das funcionalidades de correção e realização de simulados.

### 6.3. Conclusão da história #7 — Explicações por IA

Após a resolução do problema ou substituição do serviço, será necessário realizar testes completos de geração das explicações, persistência e recuperação das respostas.

A funcionalidade deverá ser validada conforme o critério de aceite estabelecido no E2, que exige explicações para pelo menos 90% das questões respondidas incorretamente.

### 6.4. Conclusão do dashboard de desempenho

A história #9 permanece pendente de implementação integral.

Será necessário disponibilizar indicadores consolidados de desempenho geral, por matéria e por assunto, utilizando os resultados armazenados no histórico de tentativas.

### 6.5. Preparação para o deploy

A publicação está prevista para a Sprint 4, utilizando Vercel para o frontend e Render para o backend.

Será necessário validar a configuração de variáveis de ambiente, CORS, conexão com o banco de dados, autenticação e comunicação com a API de IA em ambiente hospedado.

**[PREENCHIMENTO POSTERIOR — INTEGRAÇÃO SUPABASE]**

Acrescentar os impedimentos e riscos relacionados à integração do banco PostgreSQL, caso existam, incluindo eventuais ajustes necessários antes do deploy.

---

## Conclusão

A Sprint 3 representou uma evolução importante do SimulaAI, especialmente na integração entre frontend e backend, no gerenciamento administrativo de simulados e na preparação da infraestrutura de inteligência artificial.

As funcionalidades de realização de simulados, correção e consulta ao histórico foram integradas, permitindo ampliar o incremento funcional demonstrável da plataforma.

A estrutura modular de IA foi implementada e validada internamente, porém a geração de explicações pedagógicas não pôde ser concluída devido a falhas técnicas recorrentes nas requisições de inferência do serviço externo.

Como próximo passo, será priorizada a investigação dessas falhas e, caso necessário, a avaliação de uma API privada ou comercial como alternativa à API de prototipagem da NVIDIA.

O objetivo será concluir os critérios de aceite da história #7, preservar a independência da correção objetiva e avançar na preparação da plataforma para sua futura publicação.
