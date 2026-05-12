from pydantic import BaseModel


class MinisterioResponse(BaseModel):
    id: int
    nome: str
    ativo: bool = True