# Relatório Individual de Contribuição — Sprint 4 — Gabriel Reis de Souza

**Aluno:** Gabriel Reis de Souza  
**RA:** 2840482421005  
**Projeto:** SimulaAI  
**Período da Sprint 4 registrado no repositório:** 17/10/2026 a 30/10/2026  
**Complementação técnica documentada:** até 07/11/2026  
**Papel exercido nas atividades descritas:** integração frontend/backend, IA e apoio à publicação

## 1. Atividades que realizei

| Atividade | Descrição | Situação |
|---|---|---|
| Substituição da integração com IA | Ajustei o serviço de explicações, antes configurado para NVIDIA NIM, para usar Meta Model API/Muse Spark Contributor. | Implementada; teste real da chave relatado como bem-sucedido |
| Correção pedagógica | Integrei ao fluxo de resultados a apresentação do gabarito, da alternativa selecionada e das explicações por questão. | Implementada no código |
| Cache global de explicações | Trabalhei na integração do armazenamento/reutilização no PostgreSQL, com busca antes de acionar o provedor externo. | Implementação presente; teste funcional informado como concluído |
| Integração com Supabase | Validei a conexão do backend ao PostgreSQL, ajustando a URI de conexão e as dependências Psycopg. | Conexão validada |
| Dashboard do aluno | Integrei a apresentação React dos indicadores e da evolução de desempenho usando dados do backend e histórico de tentativas. | Implementado e build aprovado |
| Correções de frontend | Corrigi erros de TypeScript e estrutura JSX ocorridos durante alterações em `StudentArea`/`App.tsx`. | Build do frontend aprovado |
| Validação de regressão | Executei a suíte do backend, corrigindo um teste que pressupunha a ausência da chave da Meta. | 52 testes aprovados na última execução apresentada |
| Preparação do deploy | Sincronizei a cópia do projeto ao repositório e preparei build React para `/simulaai/`, além de configurar o backend no Render. | Frontend enviado à Hostinger; validação pública integral sem evidência anexada |

## 2. Como o meu trabalho contribuiu para o MVP

Minha principal contribuição foi integrar funcionalidades que estavam separadas ou incompletas: explicações pedagógicas por IA, persistência PostgreSQL, dashboard do aluno e apresentação da correção. Mantive a correção objetiva independente da IA e utilizei cache para reduzir chamadas repetidas. Também participei da preparação da publicação web, preservando a arquitetura FastAPI + React e adotando Hostinger para o frontend e Render para o backend.

## 3. Dificuldades enfrentadas e soluções

Enfrentei problemas na configuração do PostgreSQL (`localhost` em vez de Supabase e ausência do driver `psycopg`), na identificação do arquivo de variáveis de ambiente, em alterações de JSX no `App.tsx`, na aplicação de patches sobre versões diferentes e na sincronização de um projeto originalmente extraído de ZIP com o histórico Git da equipe. No deploy, o primeiro build do Render não encontrou `requirements.txt` porque precisava executar a partir de `backend/`. As correções envolveram inspeção dos logs, ajustes de dependências, revisão do JSX, compilação com TypeScript e conferência dos caminhos de execução.

## 4. Testes e evidências

- Suíte executada: `python -m pytest -q` — 52 testes aprovados, 1 aviso de depreciação.
- Build executado: `npm run build -- --base=/simulaai/` — concluído pelo Vite.
- Teste de conexão PostgreSQL/Supabase e acesso ao SQL Editor realizado.
- Chave da Meta testada em chamada real, conforme registro da atividade.
- O fluxo de cache foi informado como validado manualmente; cobertura automatizada específica ainda precisa ser anexada.
- Evidências finais do backend no Render e de login no ambiente público devem ser anexadas antes de declarar o deploy integralmente concluído.

## 5. Participação em rituais e revisão de PRs

**Sprint Review:** [preencher somente se participei; indicar data]  
**Retrospectiva:** [preencher somente se participei; indicar data]  
**Pull Requests revisados:** [indicar PRs de colegas efetivamente revisados; caso nenhum, registrar "nenhum"]  
**Commit/PR das alterações:** [inserir link exato após conferir o histórico na main]

## 6. Aprendizados e melhorias propostas

Aprendi a importância de validar integrações externas separadamente, usar os testes automatizados como proteção contra regressões, sincronizar versões antes de editar arquivos compartilhados e registrar evidências reais de publicação. Para continuar o projeto, priorizarei testes específicos do cache, atualização da documentação de deploy, revisão das senhas de demonstração e medição da taxa de explicações geradas para verificar o critério de 90%.

**Repositório:** https://github.com/Lab-EngSoft/SimulaAI
Link da aplicação: https://projectreis.com/simulaai/
usuarios disponiveis para teste: 
Perfil	        E-mail	                    Senha
Administrador	carlos.admin@simulaai.app	admin123
Aluno	        ana.aluno@simulaai.app	    aluno123