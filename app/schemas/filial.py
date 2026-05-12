from pydantic import BaseModel


class FilialResponse(BaseModel):
    id: int
    nome: str
    ativo: bool = True