from pydantic import BaseModel


class VinculoResponse(BaseModel):
    id: int
    nome: str
    ativo: bool = True