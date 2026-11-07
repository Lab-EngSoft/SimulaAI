# Deploy em produção — SimulaAI (Sprint 4 / E8, história #11)

## Checklist rápido (~15 min, pode ser feito por qualquer membro do grupo)

- [ ] **Supabase:** criar projeto → copiar a Connection String (URI) → rodar `database/schema.sql` no SQL Editor
- [ ] **Render:** New Web Service no repo `Lab-EngSoft/SimulaAI` → Root Directory `backend` → Build `pip install -r requirements.txt` → Start deixa o `Procfile` → variáveis `APP_ENV=production`, `DATABASE_URL` (Supabase), `SECRET_KEY` (gerar), `CORS_ORIGINS=http://localhost:5173`, `NVIDIA_API_KEY` (opcional) → Create
- [ ] Testar `https://<url-render>/health` → `{"status":"ok"}`
- [ ] **Vercel:** importar o mesmo repo → Root Directory `frontend` → env `VITE_API_URL=https://<url-render>` → Deploy
- [ ] No Render, atualizar `CORS_ORIGINS` com a URL da Vercel → Save (redeploy automático)
- [ ] Colocar as duas URLs no `README.md` (linha de Deploy) e tirar prints do sistema no ar (serve pro E10)

> Validação local já feita: o backend sobe em modo produção com o comando do
> `Procfile` e responde `/health` (smoke test de 17/10/2026).

---

Este guia coloca o SimulaAI **no ar por URL pública**, cumprindo o requisito
mínimo do Manual §3 "Deploy público por URL".

Arquitetura do deploy:

| Parte | Plataforma | Onde está configurado |
|---|---|---|
| Backend FastAPI | **Render** (Web Service) | `backend/Procfile` + `backend/runtime.txt` |
| Banco PostgreSQL | **Supabase** | `database/schema.sql` |
| Frontend React | **Vercel** | pasta `frontend/` (Vite) |

> Regra de ouro: **nenhum segredo vai para o git** (`SECRET_KEY`,
> `DATABASE_URL`, `NVIDIA_API_KEY` ficam como variáveis de ambiente na
> plataforma — o `.gitignore` já bloqueia o `.env`).

## Passo 1 — Banco no Supabase

1. Acesse [supabase.com](https://supabase.com) → **New project** → guarde a senha do banco.
2. **Settings → Database → Connection string (URI)** → copie algo como
   `postgresql://postgres:[SUA-SENHA]@db.xxxxx.supabase.co:5432/postgres`
   (substitua `[SUA-SENHA]` pela senha do projeto).
3. **SQL Editor** → cole o conteúdo inteiro de `database/schema.sql` → **Run**.
   Isso cria as 9 tabelas do projeto.

## Passo 2 — Backend no Render

1. [render.com](https://render.com) → **New → Web Service** → conecte a conta do GitHub e escolha o repositório `Lab-EngSoft/SimulaAI`.
2. **Root Directory:** `backend`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** deixe em branco — o Render usa o `Procfile`
   (`web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
5. **Environment Variables** (aba *Environment*):

   | Variável | Valor |
   |---|---|
   | `APP_ENV` | `production` (desativa o seed de dados demo) |
   | `DATABASE_URL` | a URI do Supabase (passo 1) |
   | `SECRET_KEY` | gere uma chave forte: `python -c "import secrets;print(secrets.token_urlsafe(48))"` |
   | `CORS_ORIGINS` | comece com `http://localhost:5173` e adicione a URL da Vercel no passo 4 |
   | `NVIDIA_API_KEY` | opcional — sem ela o sistema funciona normalmente, só sem explicações por IA |

6. **Create Web Service** → aguarde o build → a URL tipo
   `https://simulaai-api.onrender.com` aparece no topo.
7. Teste: abra `https://<sua-url>/health` → deve responder `{"status": "ok"}`
   e `/docs` deve abrir o Swagger.

## Passo 3 — Frontend na Vercel

1. [vercel.com](https://vercel.com) → **Add New → Project** → importe `Lab-EngSoft/SimulaAI`.
2. **Root Directory:** `frontend`
3. O Vite é detectado automaticamente (build `npm run build`, output `dist`).
4. **Environment Variables:** `VITE_API_URL` = `https://<url-do-backend-no-render>`
5. **Deploy** → a URL tipo `https://simulaai.vercel.app` sai no painel.

## Passo 4 — Liberar o CORS no backend

No Render, edite `CORS_ORIGINS` para:

```
https://simulaai.vercel.app,http://localhost:5173
```

(use a URL exata da Vercel, com `https://`, sem barra no final) → **Save** →
o Render faz redeploy automático.

## Passo 5 — Registrar as URLs no repositório

No `README.md`, substitua a linha de deploy pelas URLs reais de produção
e guarde prints do sistema no ar para o **E10** (manual do usuário exige
prints reais do sistema publicado, não do protótipo).

## Troubleshooting

- `/health` dá 500 → confira `DATABASE_URL` e a aba **Logs** do Render.
- Erro de CORS no navegador → `CORS_ORIGINS` precisa conter a URL exata da Vercel.
- Explicações por IA indisponíveis → normal sem `NVIDIA_API_KEY`; a correção
  objetiva continua funcionando (coberto pelo CT08 e pelo CI).
- Plano gratuito do Render entra em "sleep" após inatividade — a primeira
  requisição pode levar ~30s para acordar. É esperado no tier grátis.
