# Relatório Individual de Contribuição — Sprint 3 — Davi Sousa Cirilo (RA 2840482421006)

**Papel nesta sprint:** Back-End / Infraestrutura de Banco de Dados (Supabase)

## 1. O que fiz

| Item | PR/commit | Status | 
| ----- | ----- | ----- | 
| Criação e configuração inicial do projeto PostgreSQL na plataforma Supabase | Setup em nuvem (Sem commit) | Concluído | 
| Execução do script SQL de migração estrutural para criação das 9 tabelas do sistema | Setup em nuvem (Sem commit) | Concluído | 
| Geração e configuração da string de conexão (Session Pooler/IPv4) para integração futura | Setup em nuvem (Sem commit) | Concluído | 
| Manipulação de dados via SQL Editor (Elevação de usuário para Administrador) | Setup em nuvem (Sem commit) | Concluído | 

## 2. Rituais que participei

* [ ] Não houveram reuniões em grupo diariamente.

* [x] Sprint Review — Aconteceram de quinta e sexta.

* [x] Retrospectiva — Projeto dissecado e setorizado.

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido | 
| ----- | ----- | ----- | 
| - | - | Nenhum PR de código revisado nesta etapa, foco exclusivo na preparação do ambiente de banco de dados. | 

## 4. Dificuldades e o que aprendi

* **Dificuldades:** Entender a interface do Supabase e garantir que o script SQL rodasse perfeitamente no SQL Editor da plataforma, estabelecendo a infraestrutura correta sem depender de um banco local.

* **O que aprendi:** Aprendi a provisionar um banco de dados PostgreSQL na nuvem (BaaS), rodar scripts de criação de tabelas diretamente no console web e extrair as credenciais corretas (Session Pooler) para preparar o terreno para a futura conexão da API FastAPI.