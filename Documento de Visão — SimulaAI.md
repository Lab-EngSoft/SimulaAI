# Documento de Visão — SimulaAI

**Equipe:** [Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (28040482421006) — vinicius brasileiro veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)] 
**Trilha:** B(Cliente Real)  
**Origem do problema:**  Dificuldade de estudante em passar em provas
**Data:** 21/08/2026

## 1. Problema
Estudantes que estão se preparando para vestibulares, concursos, provas acadêmicas ou certificações precisam resolver uma grande quantidade de questões para identificar seus pontos fortes e suas dificuldades. Atualmente, esse processo costuma ser realizado por meio de listas de exercícios, provas anteriores, apostilas ou plataformas que apenas informam se uma resposta está correta ou incorreta.

Esse modelo dificulta a compreensão do motivo do erro e exige que o estudante procure manualmente explicações em livros, vídeos, sites ou outras fontes. Além disso, acompanhar a evolução ao longo do tempo pode exigir anotações, planilhas ou análise manual dos resultados obtidos em diferentes simulados.

O problema se torna mais relevante quando o estudante resolve dezenas de questões por semana, pois identificar padrões de erro, matérias com maior dificuldade e conteúdos que precisam ser revisados demanda tempo. O sistema proposto busca centralizar a realização dos simulados, o armazenamento das questões, o acompanhamento de desempenho e a explicação dos erros em uma única plataforma.

## 2. Público-alvo e perfis de usuário
| Perfil | Quem é | O que faz no sistema |
|--------|--------|----------------------|
| Aluno  | Estudante que deseja treinar para provas, vestibulares, concursos ou avaliações | Realiza simulados, responde questões, consulta resultados, recebe explicações da IA e acompanha seu desempenho |
| Administrador | Responsável pela manutenção e organização da plataforma | Cadastra, edita e remove questões, matérias, assuntos e alternativas, além de acompanhar informações gerais do sistema |

## 3. Visão da solução
O SimulaAI será uma plataforma web de treinamento por meio de simulados, utilizando um banco de questões organizado por matérias e assuntos. O aluno poderá realizar simulados, responder às questões e receber automaticamente sua pontuação e análise de desempenho. Quando ocorrer um erro, uma Inteligência Artificial será utilizada para explicar a alternativa correta, apontar possíveis motivos do erro e auxiliar o estudante na compreensão do conteúdo. O sistema também armazenará o histórico de tentativas para identificar matérias e assuntos com maior índice de erros e apresentar indicadores sobre a evolução do aluno.

## 4. Objetivos do MVP (o que o semestre entrega)
- Permitir que um aluno realize um simulado completo com questões cadastradas no banco e receba o resultado automaticamente ao final.
- Gerar uma explicação utilizando IA para pelo menos 90% das questões respondidas incorretamente pelo aluno.
- Disponibilizar um dashboard de desempenho que apresente quantidade de acertos, erros, percentual de aproveitamento e desempenho por matéria e assunto.
- Manter um histórico das tentativas realizadas pelo aluno, permitindo comparar seu desempenho entre diferentes simulados.
- Permitir que administradores cadastrem e gerenciem questões, alternativas, matérias e assuntos utilizados na geração dos simulados.

## 5. Fora de escopo (explicitamente)
- Aplicativo mobile nativo para Android ou iOS, pois o MVP será desenvolvido como aplicação web responsiva.
- Criação automática de questões utilizando IA, pois nesta etapa as questões serão previamente cadastradas e revisadas no banco.
- Correção de questões discursivas, pois o MVP trabalhará prioritariamente com questões objetivas de múltipla escolha.
- Sistema de pagamento, assinatura ou venda de planos, pois o objetivo do semestre é validar as funcionalidades acadêmicas principais.
- Ranking competitivo entre alunos e sistema de recompensas ou gamificação avançada, pois essas funcionalidades não são essenciais para validar a proposta principal.
- Treinamento de um modelo próprio de Inteligência Artificial, pois será utilizada uma API ou modelo de IA já existente para gerar as explicações.

## 6. Requisitos mínimos do §3 do Manual — como este projeto cobre cada um
| Requisito mínimo | Como este projeto cobre |
|------------------|-------------------------|
| Autenticação com 2+ perfis | O sistema terá autenticação de usuários e pelo menos dois perfis de acesso: **Aluno** e **Administrador**, com permissões e funcionalidades diferentes. |
| 6+ entidades com relacionamento N:N | O banco terá entidades como **Usuário, Simulado, Questão, Alternativa, Matéria, Assunto, Tentativa e Resposta**. Um Simulado possui várias Questões e uma Questão pode participar de vários Simulados, caracterizando relacionamento N:N. |
| Regra de negócio não trivial | Ao finalizar um simulado, o sistema calculará a pontuação, percentual de aproveitamento e desempenho por matéria/assunto. As questões respondidas incorretamente serão enviadas para análise da IA, que deverá considerar o enunciado, as alternativas, a resposta escolhida e a resposta correta para gerar um feedback personalizado. |
| Consulta agregada (relatório/dashboard) | O aluno terá um dashboard com total de simulados realizados, média de aproveitamento, quantidade de acertos e erros, desempenho por matéria, desempenho por assunto e evolução ao longo das tentativas. |
| Validações em interface e banco | Serão aplicadas validações no frontend e backend, como campos obrigatórios, formato de e-mail, senha mínima, quantidade de alternativas, existência de apenas uma alternativa correta por questão e integridade dos relacionamentos entre entidades. O banco também utilizará restrições como `NOT NULL`, `UNIQUE`, chaves estrangeiras e demais constraints necessárias. |
| Deploy público por URL | A aplicação será publicada em um serviço de hospedagem e poderá ser acessada publicamente por meio de uma URL. |
| Repositório Git com README | O código-fonte será versionado utilizando Git e armazenado em um repositório contendo este README, instruções para execução do projeto, tecnologias utilizadas e informações da equipe. |

## 7. Riscos identificados
| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| A IA fornecer uma explicação incorreta ou imprecisa | Alto | Enviar para a IA a resposta correta previamente cadastrada no banco e solicitar que ela apenas explique a resolução, além de informar ao usuário que a explicação é um recurso auxiliar |
| Indisponibilidade ou limite de requisições da API de IA | Alto | Implementar tratamento de erros, limitar chamadas desnecessárias e permitir que a correção objetiva continue funcionando mesmo caso a IA esteja indisponível |
| Custo elevado no uso da API de IA | Médio | Controlar o tamanho dos prompts, limitar requisições, armazenar explicações reutilizáveis quando possível e acompanhar o consumo da API |
| Questões cadastradas com resposta incorreta ou informações inconsistentes | Alto | Criar validações no cadastro e permitir que apenas usuários administradores gerenciem o banco de questões |
| Baixa quantidade de questões para gerar simulados variados | Médio | Preparar previamente uma base mínima de questões distribuídas entre diferentes matérias e assuntos |
| Atraso na integração entre frontend, backend, banco de dados e IA | Alto | Dividir o desenvolvimento em etapas, priorizando primeiro autenticação, banco de questões e simulados, deixando a integração com IA para uma etapa posterior |
| Exposição de dados ou acesso indevido às funcionalidades administrativas | Alto | Utilizar autenticação segura, controle de autorização por perfil, armazenamento seguro de senhas e validação das permissões também no backend |
