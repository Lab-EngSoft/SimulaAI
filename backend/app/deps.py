"""Dependências de autenticação/autorização do FastAPI.

- get_current_user: lê o token do cabeçalho Authorization, valida e devolve
  o usuário logado (401 se faltar token, for inválido ou expirado).
- require_admin: além de logado, o perfil precisa ser ADMINISTRADOR (403).

É aqui que a permissão é "validada também no backend" — critério de aceite
da história #1 e do caso de teste CT02: mesmo que alguém mexa no frontend,
a API recusa.
"""
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    if credentials is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Autenticação obrigatória: envie o token no cabeçalho Authorization.",
        )
    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido ou expirado.")

    usuario = db.get(Usuario, int(payload["sub"]))
    if usuario is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário do token não existe mais.")
    return usuario


def require_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.perfil != "ADMINISTRADOR":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Acesso restrito ao perfil ADMINISTRADOR.",
        )
    return usuario


def require_aluno(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    """O fluxo do simulado (iniciar/responder/finalizar) é do perfil ALUNO."""
    if usuario.perfil != "ALUNO":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Acesso restrito ao perfil ALUNO.",
        )
    return usuario
