from pydantic import BaseModel


class VinculoResponse(BaseModel):
    seq_vinculo: int
    ds_nome: str
    st_ativo: bool

    class Config:
        from_attributes = True