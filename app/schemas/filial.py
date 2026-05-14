from pydantic import BaseModel


class FilialResponse(BaseModel):
    seq_filial: int
    ds_nome: str
    st_ativo: bool

    class Config:
        from_attributes = True