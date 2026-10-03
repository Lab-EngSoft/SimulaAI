"""Rotas de autenticação — história #1 (perfis ALUNO e ADMINISTRADOR).

- POST /auth/login    → devolve token JWT + dados do usuário (CT01)
- POST /auth/register → qualquer pessoa pode criar conta ALUNO;
  administradores não são criados por aqui (evita alguém se autopromover)
- GET  /auth/me       → dados do usuário logado
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Usuario
from app.schemas import LoginIn, RegisterIn, TokenOut, UsuarioOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenOut)
def login(dados: LoginIn, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email.lower()).first()
    if usuario is None or not verify_password(dados.senha, usuario.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou senha incorretos.")
    return TokenOut(
        access_token=create_access_token(usuario),
        usuario=UsuarioOut.model_validate(usuario),
    )


@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def register(dados: RegisterIn, db: Session = Depends(get_db)):
    email = dados.email.lower()
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe usuário com este e-mail.")
    usuario = Usuario(
        nome=dados.nome,
        email=email,
        senha_hash=hash_password(dados.senha),
        perfil="ALUNO",
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(get_current_user)):
    return usuario
