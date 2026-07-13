import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_SECRET_KEY
from app.models.usuario import Usuario

HASH_ALGORITHM = "pbkdf2_sha256"
HASH_ITERATIONS = 390000
SALT_BYTES = 16
JWT_ALGORITHM = "HS256"


class CredenciaisInvalidasError(Exception):
    pass


class TokenInvalidoError(Exception):
    pass


def _normalizar_usuario(ds_usuario: str) -> str:
    return ds_usuario.strip().lower()


def gerar_hash_senha(ds_senha: str) -> str:
    salt = secrets.token_bytes(SALT_BYTES)
    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        ds_senha.encode("utf-8"),
        salt,
        HASH_ITERATIONS
    )
    return "$".join(
        [
            HASH_ALGORITHM,
            str(HASH_ITERATIONS),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(hash_senha).decode("ascii"),
        ]
    )


def verificar_senha(ds_senha: str, ds_senha_hash: str) -> bool:
    try:
        algoritmo, iteracoes, salt_b64, hash_b64 = ds_senha_hash.split("$", 3)
        if algoritmo != HASH_ALGORITHM:
            return False

        salt = base64.b64decode(salt_b64)
        hash_salvo = base64.b64decode(hash_b64)
        hash_informado = hashlib.pbkdf2_hmac(
            "sha256",
            ds_senha.encode("utf-8"),
            salt,
            int(iteracoes)
        )
        return hmac.compare_digest(hash_informado, hash_salvo)
    except (ValueError, TypeError):
        return False


def buscar_usuario_por_login(db: Session, ds_usuario: str) -> Usuario | None:
    usuario_normalizado = _normalizar_usuario(ds_usuario)
    return (
        db.query(Usuario)
        .filter(Usuario.ds_usuario == usuario_normalizado)
        .filter(Usuario.st_ativo.is_(True))
        .first()
    )


def autenticar_usuario(
    db: Session,
    ds_usuario: str,
    ds_senha: str
) -> Usuario:
    try:
        usuario = buscar_usuario_por_login(db, ds_usuario)

        if usuario is None:
            raise CredenciaisInvalidasError()

        if not verificar_senha(ds_senha, usuario.ds_senha_hash):
            raise CredenciaisInvalidasError()

        return usuario
    except SQLAlchemyError:
        raise


def _base64url_encode(valor: bytes) -> str:
    return base64.urlsafe_b64encode(valor).rstrip(b"=").decode("ascii")


def _base64url_decode(valor: str) -> bytes:
    padding = "=" * (-len(valor) % 4)
    return base64.urlsafe_b64decode(valor + padding)


def _json_base64url(valor: dict[str, Any]) -> str:
    return _base64url_encode(
        json.dumps(valor, separators=(",", ":")).encode("utf-8")
    )


def criar_token_acesso(usuario: Usuario) -> tuple[str, datetime, int]:
    agora = datetime.now(UTC)
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_at = agora + expires_delta

    header = {
        "alg": JWT_ALGORITHM,
        "typ": "JWT",
    }
    payload = {
        "sub": str(usuario.seq_usuario),
        "ds_usuario": usuario.ds_usuario,
        "iat": int(agora.timestamp()),
        "exp": int(expires_at.timestamp()),
    }

    assinatura_base = f"{_json_base64url(header)}.{_json_base64url(payload)}"
    assinatura = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        assinatura_base.encode("ascii"),
        hashlib.sha256
    ).digest()

    token = f"{assinatura_base}.{_base64url_encode(assinatura)}"
    return token, expires_at, int(expires_delta.total_seconds())


def validar_token_acesso(token: str) -> dict[str, Any]:
    try:
        header_b64, payload_b64, assinatura_b64 = token.split(".")
        assinatura_base = f"{header_b64}.{payload_b64}"
        assinatura_esperada = hmac.new(
            AUTH_SECRET_KEY.encode("utf-8"),
            assinatura_base.encode("ascii"),
            hashlib.sha256
        ).digest()
        assinatura_recebida = _base64url_decode(assinatura_b64)

        if not hmac.compare_digest(assinatura_recebida, assinatura_esperada):
            raise TokenInvalidoError()

        header = json.loads(_base64url_decode(header_b64))
        if header.get("alg") != JWT_ALGORITHM:
            raise TokenInvalidoError()

        payload = json.loads(_base64url_decode(payload_b64))
        exp = int(payload["exp"])

        if datetime.now(UTC).timestamp() >= exp:
            raise TokenInvalidoError()

        return payload
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        raise TokenInvalidoError() from None


def gerar_hash_senha_cli() -> None:
    senha = os.getenv("AUTH_PASSWORD")
    if not senha:
        raise RuntimeError("Informe a senha em AUTH_PASSWORD")

    print(gerar_hash_senha(senha))
