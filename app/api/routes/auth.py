from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import TokenResponse
from app.services.auth_service import (
    CredenciaisInvalidasError,
    TokenInvalidoError,
    autenticar_usuario,
    criar_token_acesso,
    validar_token_acesso,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obter_usuario_autenticado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    try:
        payload = validar_token_acesso(token)
        seq_usuario = int(payload["sub"])
    except (TokenInvalidoError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    usuario = (
        db.query(Usuario)
        .filter(Usuario.seq_usuario == seq_usuario)
        .filter(Usuario.st_ativo.is_(True))
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario nao encontrado ou inativo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        usuario = autenticar_usuario(
            db,
            form_data.username,
            form_data.password,
        )
    except CredenciaisInvalidasError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha invalidos",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    access_token, expires_at, expires_in = criar_token_acesso(usuario)

    return TokenResponse(
        access_token=access_token,
        expires_at=expires_at,
        expires_in=expires_in,
        usuario=usuario,
    )


@router.get("/me")
def me(usuario: Usuario = Depends(obter_usuario_autenticado)):
    return {
        "seq_usuario": usuario.seq_usuario,
        "ds_usuario": usuario.ds_usuario,
        "ds_nome": usuario.ds_nome,
        "st_ativo": usuario.st_ativo,
    }
