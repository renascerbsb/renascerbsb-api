from datetime import date

from pydantic import BaseModel


class PessoaResponse(BaseModel):
    seq_pessoa: int
    ds_nome: str
    nr_telefone: str | None = None
    dt_nascimento: date | None = None
    seq_cidade: int | None = None
    seq_filial: int | None = None
    seq_vinculo: int | None = None
    st_ativo: bool

    class Config:
        from_attributes = True