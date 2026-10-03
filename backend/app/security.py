"""Segurança: hash de senha (PBKDF2) e token de sessão (JWT).

Por que PBKDF2 e não MD5/SHA puro: PBKDF2 aplica o SHA-256 centenas de milhares
de vezes com um sal aleatório por usuário, resistindo a ataques de dicionário
(prática recomendada pelo OWASP para senhas). Por que JWT: o frontend envia o
token em toda requisição (cabeçalho Authorization) e o backend identifica o
usuário sem guardar sessão no servidor — simples de usar no Vercel/Render.
"""
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "simulaai-dev-troque-esta-chave-por-uma-forte-em-producao")
ALGORITHM = "HS256"
TOKEN_EXPIRA_MINUTOS = int(os.getenv("TOKEN_EXPIRA_MINUTOS", "480"))  # 8h

ITERACOES = 600_000


def hash_password(senha: str) -> str:
    """Gera 'pbkdf2_sha256$iteracoes$sal$hash' — nunca guarde a senha pura."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), bytes.fromhex(salt), ITERACOES)
    return f"pbkdf2_sha256${ITERACOES}${salt}${digest.hex()}"


def verify_password(senha: str, armazenado: str) -> bool:
    try:
        _, iteracoes, salt, hash_hex = armazenado.split("$")
        digest = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), bytes.fromhex(salt), int(iteracoes)
        )
        return hmac.compare_digest(digest.hex(), hash_hex)
    except ValueError:
        return False


def create_access_token(usuario) -> str:
    payload = {
        "sub": str(usuario.id),  # PyJWT exige 'sub' como string
        "perfil": usuario.perfil,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRA_MINUTOS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Levanta jwt.PyJWTError se o token for inválido ou expirado."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
