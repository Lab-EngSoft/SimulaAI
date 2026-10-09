# Guia de integração frontend ↔ backend — SimulaAI

## Arquitetura

- Frontend React/Vite (`frontend/src/App.tsx`): telas e estado de interface; **não contém dados de demonstração cadastrados na memória**.
- Cliente HTTP (`frontend/src/api.ts`): funções tipadas de login, CRUD, simulados e tentativas; tokens na sessão da aba (`sessionStorage`).
- Proxy Vite (`frontend/vite.config.ts`): `/api/*` no navegador → `http://127.0.0.1:8000/*` no FastAPI.
- Backend FastAPI (`backend/app/main.py`, `backend/app/routers/`): valida autenticação/autorização, fornece JSON e persiste no SQLite/PostgreSQL.
- Banco local: `backend/simulaai.db` (inicializado no primeiro start com matéria, assunto, questões, um simulado e usuários de demonstração).

## Preparação rápida

Em terminais separados a partir da raiz do repositório:

**Linux/macOS — terminal 1**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Windows PowerShell — terminal 1**

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2, qualquer sistema**

```bash
cd frontend
npm ci
npm run dev
```

- Interface: http://localhost:5173
- Documentação da API: http://localhost:8000/docs
- Verifique o Node.js: `node -v` (recomendado 22+).
- Localmente, não precisa criar `.env`: o backend usa SQLite e o Vite usa o proxy.

## Roteiro de validação manual

1. Entre com `carlos.admin@simulaai.app` / `admin123` e confira as matérias, assuntos e questões do seed.
2. Cadastre uma matéria e um assunto; cadastre uma questão com uma correta. Atualize a questão, inclusive o assunto. Recarregue o navegador e confirme que os dados persistiram.
3. Saia e entre com `ana.aluno@simulaai.app` / `aluno123`. Confirme que não há acesso ao painel de administração.
4. Inicie **Simulado demonstrativo**, marque respostas, saia da área do simulado e clique **Continuar**: as escolhas devem permanecer.
5. Finalize e confira acertos, erros, percentual e histórico. O aluno não vê o gabarito durante a tentativa.
6. Teste senha incorreta: login deve falhar. Teste acesso à API `/questoes` com token de aluno: deve receber HTTP 403.
7. Pare o backend e tente fazer login: deve aparecer aviso de conexão, sem login fictício.
8. Execute `cd backend && python -m pytest -q` e `cd frontend && npm run build && npm run lint`.

## API mapeada

| Ação frontend | Endpoint FastAPI |
| --- | --- |
| Login / sessão / cadastro | `POST /auth/login`, `GET /auth/me`, `POST /auth/register` |
| Matérias / assuntos | `/materias`, `/assuntos` (GET, POST, PUT, DELETE) |
| Questões e alternativas | `/questoes` (GET, POST, PUT, DELETE; perfil admin) |
| Catálogo de simulados | `GET /simulados` |
| Histórico e início | `GET /tentativas`, `POST /tentativas` |
| Questões sem gabarito | `GET /tentativas/{id}/questoes` |
| Resposta / correção | `POST /tentativas/{id}/respostas`, `POST /tentativas/{id}/finalizar` |

## Limitações conhecidas

- Ainda não há CRUD administrativo de simulados, somente catálogo/seed e execução pelo aluno.
- A explicação gerada por IA (campo `explicacao_ia`) não está implementada no backend.
- O histórico mostra os resultados consolidados; a API atual não devolve a correção detalhada de uma tentativa já finalizada. A visualização detalhada existe apenas no momento de finalizar.
- O frontend permanece **sem testes automatizados de componentes/E2E**; execute o roteiro acima antes do merge. Produção requer `APP_ENV=production` (desabilita o seed demonstrativo em banco novo), gestão segura de `SECRET_KEY`, remoção de contas de demo existentes e CORS.
