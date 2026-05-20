from pydantic import BaseModel


class FaixaEtariaResponse(BaseModel):
    seq_faixa_etaria: int
    ds_nome: str
    nr_idade_minima: int
    nr_idade_maxima: int | None = None
    st_ativo: bool

    class Config:
        from_attributes = True
