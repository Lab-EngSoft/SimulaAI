"""Schemas Pydantic — validação de entrada e formato de saída da API.

Regra da casa: nada chega no banco sem passar por um schema aqui. É a
"validação em interface e banco" do requisito mínimo do Manual (§3):
- Campos obrigatórios e tamanhos são validados ANTES de tocar o banco (422).
- Regras de negócio (ex.: exatamente uma alternativa correta) ficam nos
  routers, com mensagem de erro clara (CT04).
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ---------- Autenticação (história #1) ----------

class LoginIn(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=8, max_length=100)


class RegisterIn(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=100)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


# ---------- Matérias (história #2) ----------

class MateriaIn(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str | None = None


class AssuntoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    materia_id: int
    nome: str
    descricao: str | None


class MateriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str | None


class MateriaDetalheOut(MateriaOut):
    assuntos: list[AssuntoOut] = []


# ---------- Assuntos (história #2) ----------

class AssuntoIn(BaseModel):
    materia_id: int
    nome: str = Field(min_length=1, max_length=100)
    descricao: str | None = None


# ---------- Questões e alternativas (história #3) ----------

class AlternativaIn(BaseModel):
    texto: str = Field(min_length=1)
    correta: bool = False


class AlternativaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    texto: str
    correta: bool


class QuestaoIn(BaseModel):
    assunto_id: int
    enunciado: str = Field(min_length=1)
    nivel_dificuldade: str | None = Field(default=None, max_length=30)
    alternativas: list[AlternativaIn] = Field(min_length=2, max_length=5)


class QuestaoUpdate(BaseModel):
    """PUT parcial: só os campos enviados são alterados."""
    assunto_id: int | None = None
    enunciado: str | None = Field(default=None, min_length=1)
    nivel_dificuldade: str | None = Field(default=None, max_length=30)
    alternativas: list[AlternativaIn] | None = Field(default=None, min_length=2, max_length=5)


class QuestaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assunto_id: int
    enunciado: str
    nivel_dificuldade: str | None
    alternativas: list[AlternativaOut]


# ---------- Simulados e tentativas (histórias #4–#6, Sprint 2) ----------

class SimuladoOut(BaseModel):
    id: int
    titulo: str
    descricao: str | None
    total_questoes: int


class SimuladoIn(BaseModel):
    """Questões são identificadas e ordenadas por questao_ids (sem gabarito no payload)."""
    titulo: str = Field(min_length=3, max_length=150)
    descricao: str | None = None
    questao_ids: list[int] = Field(min_length=1, max_length=200)

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, value: str) -> str:
        titulo = value.strip()
        if len(titulo) < 3:
            raise ValueError("O título deve ter pelo menos 3 caracteres não vazios.")
        return titulo


class SimuladoDetalheOut(SimuladoOut):
    questao_ids: list[int]
    total_tentativas: int


class TentativaIn(BaseModel):
    simulado_id: int


class TentativaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    simulado_id: int
    status: str
    data_inicio: datetime
    data_fim: datetime | None
    acertos: int
    erros: int
    percentual_aproveitamento: float


class AlternativaJogoOut(BaseModel):
    """Alternativa vista pelo aluno RESPONDENDO — sem a marcação de correta:
    a resposta certa só é revelada na correção, depois de finalizar."""

    id: int
    texto: str


class QuestaoJogoOut(BaseModel):
    id: int
    enunciado: str
    nivel_dificuldade: str | None
    alternativas: list[AlternativaJogoOut]
    respondida_alternativa_id: int | None = None


class RespostaIn(BaseModel):
    questao_id: int
    alternativa_id: int


class RespostaCorrigidaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    questao_id: int
    alternativa_id: int
    correta: bool
    explicacao_ia: str | None


class FinalizarOut(BaseModel):
    tentativa: TentativaOut
    respostas: list[RespostaCorrigidaOut]


# ---------- IA (contrato preparado para uma próxima sprint) ----------

class IAStatusOut(BaseModel):
    disponivel: bool
    descricao: str
