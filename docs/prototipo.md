# Roteiro do Protótipo Navegável — SimulaAI

**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)

**Link do protótipo:** https://www.figma.com/make/XhzihrbXGnBbOWYhQaRjGb/SimulaAI-Web-App-Prototype?p=f

| Tela | Perfil | História relacionada (E2) | O que a tela mostra/permite |
|---|---|---:|---|
| Login | Aluno / Administrador | #1 | Entrada com e-mail e senha e encaminhamento conforme o perfil |
| Dashboard do aluno | Aluno | #9 | Acertos, erros, aproveitamento e desempenho por matéria e assunto |
| Catálogo de simulados | Aluno | #4 | Seleção de matéria, assunto e tipo de simulado para iniciar uma tentativa |
| Simulado em andamento | Aluno | #5 | Enunciado, alternativas, navegação entre questões e registro das respostas |
| Resultado do simulado | Aluno | #6, #7 | Acertos, erros, percentual de aproveitamento, respostas e explicações da IA |
| Histórico de tentativas | Aluno | #8 | Tentativas anteriores e seus respectivos resultados |
| Evolução do desempenho | Aluno | #10 | Comparação do desempenho entre diferentes tentativas realizadas |
| Dashboard administrativo | Administrador | #1, #2, #3 | Acesso às funcionalidades de gerenciamento disponíveis ao Administrador |
| Gestão de matérias e assuntos | Administrador | #2 | Cadastro, edição e remoção de matérias e assuntos |
| Gestão de questões e alternativas | Administrador | #3 | Cadastro, edição e remoção de questões, alternativas e definição da resposta correta |

## Fluxo demonstrável

1. O usuário acessa a tela de Login.
2. Um Aluno acessa o Dashboard e inicia um novo simulado.
3. O Aluno seleciona a matéria, o assunto e o tipo de simulado.
4. O Aluno responde às questões e finaliza a tentativa.
5. O sistema mostra o Resultado, incluindo acertos, erros, aproveitamento e explicações da IA para respostas incorretas.
6. O Aluno consulta o Histórico de tentativas e sua Evolução de desempenho.
7. Um Administrador acessa o Dashboard administrativo.
8. O Administrador acessa as telas de gestão para manter matérias, assuntos, questões e alternativas.

Prompt usado:
Crie um protótipo navegável de uma aplicação web chamada **SimulaAI**, uma plataforma de simulados para estudantes.

O sistema possui dois perfis: **Aluno** e **Administrador**.

Crie um visual moderno, simples, organizado e responsivo, com foco em educação e tecnologia.

O protótipo deve conter as seguintes telas e navegação:

1. **Login**

   * Campo de e-mail
   * Campo de senha
   * Botão "Entrar"
   * Diferenciar acesso de Aluno e Administrador

2. **Dashboard do Aluno**

   * Saudação ao aluno
   * Resumo de desempenho
   * Total de simulados realizados
   * Percentual médio de aproveitamento
   * Desempenho por matéria
   * Desempenho por assunto
   * Área mostrando evolução recente
   * Botão para iniciar novo simulado
   * Acesso ao histórico

3. **Escolha de Simulado**

   * Lista de matérias
   * Lista de assuntos
   * Simulados disponíveis
   * Botão "Iniciar Simulado"

4. **Tela do Simulado**

   * Mostrar uma questão por vez
   * Enunciado da questão
   * Alternativas de múltipla escolha
   * Indicador de progresso, como "Questão 3 de 10"
   * Botões "Anterior" e "Próxima"
   * Botão "Finalizar Simulado"

5. **Resultado do Simulado**

   * Quantidade de acertos
   * Quantidade de erros
   * Percentual de aproveitamento
   * Lista das questões respondidas
   * Destacar questões corretas e incorretas
   * Nas questões incorretas, mostrar uma área de "Explicação da IA"

6. **Histórico**

   * Lista dos simulados realizados
   * Data
   * Matéria
   * Assunto
   * Quantidade de acertos
   * Percentual de aproveitamento
   * Botão para visualizar detalhes

7. **Tela de Evolução**

   * Gráfico simples mostrando a evolução do desempenho entre diferentes tentativas
   * Filtro por matéria e assunto

8. **Dashboard do Administrador**

   * Menu para gerenciar matérias
   * Gerenciar assuntos
   * Gerenciar questões
   * Gerenciar alternativas

9. **Cadastro/Edição de Questões**

   * Campo para enunciado
   * Seleção de matéria
   * Seleção de assunto
   * Campos para alternativas
   * Opção para definir apenas uma alternativa correta
   * Botões para salvar, editar e excluir

Crie conexões navegáveis entre as telas.

Fluxo principal do aluno:

**Login → Dashboard → Escolher Simulado → Realizar Simulado → Resultado → Explicação da IA → Histórico/Dashboard**

Fluxo principal do administrador:

**Login → Dashboard Administrativo → Matérias/Assuntos → Questões → Cadastro/Edição**

Use componentes consistentes, menu lateral ou superior, cards, tabelas, gráficos simples e botões claros.

O objetivo é criar um protótipo acadêmico funcional e fácil de demonstrar, não sendo necessário implementar código ou backend.
