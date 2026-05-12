from pydantic import BaseModel
from datetime import date


class MembroResponse(BaseModel):
    id: int
    nome: str
    telefone: str | None = None
    data_nascimento: date | None = None
    cidade_id: int | None = None
    filial_id: int | None = None
    ativo: bool = True