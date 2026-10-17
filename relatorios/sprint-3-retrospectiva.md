# Ata de Retrospectiva — Sprint 3 — SimulaAI

**Data:** [Confirmar data da reunião]  
**Presentes:** [Preencher somente com os participantes da retrospectiva]

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Integrar frontend e backend | Sim | Interfaces React integradas aos endpoints FastAPI. |
| Implementar explicações por IA | Parcialmente | Estrutura implementada, mas geração comprometida por timeouts da NVIDIA. |
| Implementar histórico e dashboard | Parcialmente | Histórico funcional; dashboard completo pendente. |
| Configurar CI com GitHub Actions | A confirmar | Não há evidência de execução automática registrada. |
| Integrar banco ao Supabase | A confirmar | Aguardando validação da integração realizada por Davi. |
| Registrar presenças e revisões de PR | A confirmar | Verificar registros dos rituais e revisões da equipe. |

## 2. O que funcionou bem

- Integração frontend/backend e implementação do gerenciamento administrativo de simulados.
- Funcionamento da correção automática e do histórico de tentativas.
- Estrutura modular da IA, permitindo a futura substituição do provedor sem alterações extensas no sistema.
- Aprovação dos 45 testes automatizados na validação anterior às últimas configurações da NVIDIA.

## 3. O que não funcionou

- A API de prototipagem NVIDIA apresentou timeouts recorrentes, impedindo a geração de explicações.
- O dashboard de desempenho não foi concluído integralmente.
- [Adicionar eventuais dificuldades da integração Supabase após confirmação.]

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Investigar os timeouts e avaliar uma API privada como alternativa à NVIDIA | Gabriel |
| Concluir e validar o dashboard de desempenho | [A definir responsável] |
| Validar a integração e persistência no Supabase | Davi |
| Preparar e testar o deploy Vercel + Render | [A definir responsáveis] |
| Executar os testes de regressão e registrar evidências finais | Equipe |

