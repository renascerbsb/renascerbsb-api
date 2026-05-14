from datetime import date
from pydantic import BaseModel
from app.schemas.cidade import CidadeResponse
from app.schemas.filial import FilialResponse
from app.schemas.vinculo import VinculoResponse
from app.schemas.ministerio import MinisterioResponse

class PessoaBase(BaseModel):
    ds_nome: str
    nr_telefone: str | None = None
    dt_nascimento: date | None = None
    seq_cidade: int | None = None
    seq_filial: int | None = None
    seq_vinculo: int | None = None

class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(PessoaBase):
    st_ativo: bool | None = None


class PessoaResponse(PessoaBase):
    seq_pessoa: int
    st_ativo: bool

    cidade: CidadeResponse | None = None
    filial: FilialResponse | None = None
    vinculo: VinculoResponse | None = None
    ministerios: list[MinisterioResponse] = []

    class Config:
        from_attributes = True

class PessoaVisitanteCreate(BaseModel):
    ds_nome: str
    nr_telefone: str | None = None
    seq_cidade: int | None = None
    seq_filial: int | None = None