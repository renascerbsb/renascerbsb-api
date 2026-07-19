from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TrajetoriaEtapaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    seq_trajetoria: int = Field(gt=0)
    seq_etapa_trajetoria: int = Field(gt=0)
    ds_nome: str = Field(min_length=1, max_length=150)
    ds_descricao: str | None = None
    nr_ordem: int = Field(gt=0)
    nr_prazo_dias: int | None = Field(default=None, ge=0)
    st_obrigatoria: bool = False
    st_permite_pular: bool = True
    st_exige_observacao: bool = False


class TrajetoriaEtapaCreate(TrajetoriaEtapaBase):
    pass


class TrajetoriaEtapaUpdate(TrajetoriaEtapaBase):
    st_ativo: bool | None = None


class TrajetoriaEtapaResponse(TrajetoriaEtapaBase):
    model_config = ConfigDict(from_attributes=True)

    seq_trajetoria_etapa: int
    st_ativo: bool
    seq_usuario_inclusao: int
    ds_nome_usuario_inclusao: str | None
    seq_usuario_alteracao: int | None
    ds_nome_usuario_alteracao: str | None
    dh_inclusao: datetime
    dh_alteracao: datetime | None
