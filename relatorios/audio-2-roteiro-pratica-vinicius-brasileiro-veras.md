# Roteiro do Áudio 2 — O que aprendi na PRÁTICA (tecnologias) — Vinicius Brasileiro Veras (RA 2840482421021)

**Tema:** stack e ferramentas que usei de verdade no SimulaAI
**Duração alvo:** ~3 a 4 minutos · **Tom:** natural, contando como foi usar cada uma

---

**[0:00–0:30] Abertura**

"Oi, sou o Vinicius de novo, RA 2840482421021. Nesse segundo áudio eu conto o que aprendi na prática: as tecnologias e ferramentas que usei no SimulaAI, o que cada uma me ensinou e onde eu errei."

**[0:30–1:30] Backend: Python + FastAPI + SQLAlchemy**

"O backend é Python 3.12 com FastAPI. Aprendi na prática o que é injeção de dependência: as rotas recebem o banco e o usuário autenticado por `Depends`, e os erros 401 e 403 ficam centralizados — isso deixou o código limpo. Com SQLAlchemy 2.x eu aprendi ORM de verdade, e o ponto alto foi o dashboard: um JOIN de quatro tabelas com GROUP BY agregando no banco em vez de no Python. O Pydantic v2 valida os dados na entrada — e me ensinou que e-mail de verdade precisa ser de domínio válido, porque `.local` falha na validação."

**[1:30–2:10] Segurança, banco e testes**

"Segurança: hash de senha com PBKDF2 e autenticação por JWT Bearer usando PyJWT — token expira, e sem token a API devolve 401. O mesmo código roda com SQLite local e com PostgreSQL no Supabase em produção: só muda a variável `DATABASE_URL`. Nos testes usei pytest com o TestClient do httpx e banco SQLite em memória, com fixtures de aluno e admin — hoje a suíte tem 49 testes passando, rodando também no GitHub Actions a cada PR, sem chave de IA, provando que a correção funciona sem serviço externo."

**[2:10–2:50] Git/GitHub e IA**

"No GitHub aprendi o fluxo completo: branch `feature/`, commit no padrão Conventional Commits, push, pull request, review e merge — e aprendi a resolver conflito de merge de verdade na PR 4, escolhendo o que manter quando duas implementações colidiram. Na parte de IA, o serviço usa um provedor injetável: em produção aponta pro NVIDIA NIM com o SDK da OpenAI, e em teste entra um provedor falso. Isso me salvou, porque a API real da NVIDIA deu timeout — o contrato de '503 quando a IA está fora' ficou testado sem depender da internet."

**[2:50–3:30] Frontend, deploy e encerramento**

"O frontend é React com TypeScript e Vite, consumindo a API pelo arquivo `api.ts` — vi de perto como o contrato do backend sustenta a tela. Para o deploy, aprendi que segredos nunca vão pro git: tudo fica em variáveis de ambiente. Deixei o backend pronto com `Procfile`, `runtime.txt` e o endpoint `/health`, e documentei o passo a passo no Render, Supabase e Vercel. E o CORS me pregou uma peça: a URL tem que bater exata."

"Resumindo a prática: FastAPI, SQLAlchemy, Pydantic, JWT, pytest com CI, Git com PR e review, provedor de IA injetável e deploy com variáveis de ambiente. O maior aprendizado técnico: testar cedo, automatizar cedo e tratar serviço externo como opcional. Valeu!"
