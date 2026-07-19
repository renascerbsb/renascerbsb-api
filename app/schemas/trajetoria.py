from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TrajetoriaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    ds_nome: str = Field(min_length=1, max_length=150)
    ds_descricao: str | None = None
    nr_versao: int = Field(default=1, gt=0)


class TrajetoriaCreate(TrajetoriaBase):
    pass


class TrajetoriaUpdate(TrajetoriaBase):
    st_ativo: bool | None = None


class TrajetoriaResponse(TrajetoriaBase):
    model_config = ConfigDict(from_attributes=True)

    seq_trajetoria: int
    st_ativo: bool
    seq_usuario_inclusao: int
    ds_nome_usuario_inclusao: str | None
    seq_usuario_alteracao: int | None
    ds_nome_usuario_alteracao: str | None
    dh_inclusao: datetime
    dh_alteracao: datetime | None
