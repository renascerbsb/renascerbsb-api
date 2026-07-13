from datetime import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    ds_usuario: str
    ds_senha: str


class UsuarioTokenResponse(BaseModel):
    seq_usuario: int
    ds_usuario: str
    ds_nome: str | None = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    expires_in: int
    usuario: UsuarioTokenResponse


class TokenPayload(BaseModel):
    sub: str
    ds_usuario: str
    exp: int
    iat: int
