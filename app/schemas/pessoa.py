from datetime import date, datetime
from pydantic import BaseModel, Field
from app.enums import ComoConheceuIgreja
from app.schemas.cidade import CidadeResponse
from app.schemas.faixa_etaria import FaixaEtariaResponse
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
    seq_faixa_etaria: int | None = None
    seq_lider: int | None = None


class PessoaCreate(PessoaBase):
    seq_ministerios: list[int] = Field(default_factory=list)


class PessoaUpdate(PessoaBase):
    st_ativo: bool | None = None
    seq_ministerios: list[int] = Field(default_factory=list)


class PessoaLiderResponse(BaseModel):
    seq_pessoa: int
    ds_nome: str
    nr_telefone: str | None = None

    class Config:
        from_attributes = True


class PessoaResponse(PessoaBase):
    seq_pessoa: int
    st_ativo: bool
    dh_inclusao: datetime

    cidade: CidadeResponse | None = None
    filial: FilialResponse | None = None
    vinculo: VinculoResponse | None = None
    faixa_etaria: FaixaEtariaResponse | None = None
    lider: PessoaLiderResponse | None = None
    ministerios: list[MinisterioResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class PessoaVisitanteCreate(BaseModel):
    ds_nome: str
    nr_telefone: str | None = None
    seq_cidade: int | None = None
    seq_filial: int | None = None
    ds_como_conheceu: ComoConheceuIgreja
    st_frequenta_igreja: bool = False
    ds_nome_convidou: str | None = None
    seq_evento_frequentou: int | None = None
    ds_observacao: str | None = None
