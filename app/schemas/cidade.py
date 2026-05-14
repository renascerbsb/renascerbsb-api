from pydantic import BaseModel


class CidadeResponse(BaseModel):
    seq_cidade: int
    ds_nome: str
    uf: str
    st_ativo: bool

    class Config:
        from_attributes = True