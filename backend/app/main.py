"""Aplicação FastAPI do SimulaAI.

Sobe com: uvicorn app.main:app --reload --port 8000 (na pasta backend/)
Documentação automática: http://localhost:8000/docs
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import assuntos, auth, materias, questoes, simulados, tentativas
from app.seed import seed_inicial


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Cria as tabelas (se não existirem) e semeia dados de demonstração.
    Base.metadata.create_all(bind=engine)
    seed_inicial()
    yield


app = FastAPI(
    title="SimulaAI API",
    version="0.1.0",
    description="Backend do SimulaAI — Laboratório de Engenharia de Software (Sprint 1).",
    lifespan=lifespan,
)

_origens = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origens,  # frontend React (Vercel/local) autorizado a chamar a API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(materias.router)
app.include_router(assuntos.router)
app.include_router(questoes.router)
app.include_router(simulados.router)
app.include_router(tentativas.router)


@app.get("/", tags=["Raiz"])
def raiz():
    return {"sistema": "SimulaAI", "documentacao": "/docs", "versao": "0.1.0"}
