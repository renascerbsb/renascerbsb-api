from pydantic import BaseModel


class CidadeResponse(BaseModel):
    id: int
    nome: str
    uf: str
    ativo: bool = True