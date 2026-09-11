# Diagramas UML — SimulaAI

**Equipe:** Gabriel Reis de Souza (2840482421005) — Davi Sousa Cirilo (2840482421006) — Vinicius Brasileiro Veras (2840482421021) — Cesar Augusto Saraiva Fifolato (2840482421022)

## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
  Aluno((Aluno))
  Admin((Administrador))

  Aluno --> UC1[Autenticar-se]
  Admin --> UC1

  Admin --> UC2[Gerenciar matérias e assuntos]
  Admin --> UC3[Gerenciar questões e alternativas]
  Admin --> UC11[Gerenciar simulados]

  Aluno --> UC4[Iniciar simulado]
  Aluno --> UC5[Responder questões]
  Aluno --> UC6[Finalizar simulado e receber correção]
  Aluno --> UC7[Receber explicação da IA]
  Aluno --> UC8[Consultar histórico de tentativas]
  Aluno --> UC9[Visualizar dashboard de desempenho]
  Aluno --> UC10[Acompanhar evolução do desempenho]

  UC7 -.->|<<extend>>| UC6
```

## 2. Diagrama de Classes

```mermaid
classDiagram

  class Usuario {
    +id: int
    +email: string
    +senhaHash: string
    +perfil: enum
    +autenticar()
  }

  class Materia {
    +id: int
    +nome: string
  }

  class Assunto {
    +id: int
    +nome: string
  }

  class Questao {
    +id: int
    +enunciado: string
  }

  class Alternativa {
    +id: int
    +texto: string
    +correta: boolean
  }

  class Simulado {
    +id: int
    +titulo: string
    +criadoEm: datetime
  }

  class Tentativa {
    +id: int
    +iniciadaEm: datetime
    +finalizadaEm: datetime
    +finalizar()
    +calcularAproveitamento()
  }

  class Resposta {
    +id: int
    +respondidaEm: datetime
    +explicacaoIA: string
    +registrar()
  }

  Usuario "1" -- "0..*" Tentativa : realiza

  Materia "1" -- "0..*" Assunto : possui

  Assunto "1" -- "0..*" Questao : classifica

  Questao "1" -- "1..*" Alternativa : possui

  Simulado "0..*" -- "0..*" Questao : contem

  Simulado "1" -- "0..*" Tentativa : origina

  Tentativa "1" -- "0..*" Resposta : registra

  Questao "1" -- "0..*" Resposta : recebe

  Alternativa "1" -- "0..*" Resposta : selecionada
```

## 3. Rastreabilidade — caso de uso → história do backlog

| Caso de uso                           | História(s) relacionada(s) (E2) |
| ------------------------------------- | ------------------------------- |
| Autenticar-se                         | #1                              |
| Gerenciar matérias e assuntos         | #2                              |
| Gerenciar questões e alternativas     | #3                              |
| Iniciar simulado                      | #4                              |
| Responder questões                    | #5                              |
| Finalizar simulado e receber correção | #6                              |
| Receber explicação da IA              | #7                              |
| Consultar histórico de tentativas     | #8                              |
| Visualizar dashboard de desempenho    | #9                              |
| Acompanhar evolução do desempenho     | #10                             |
| Gerenciar simulados                   | #11*                            |
