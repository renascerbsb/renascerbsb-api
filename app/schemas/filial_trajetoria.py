from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FilialTrajetoriaCreate(BaseModel):
    seq_filial: int = Field(gt=0)
    seq_trajetoria: int = Field(gt=0)
    st_padrao: bool = False


class FilialTrajetoriaUpdate(BaseModel):
    st_padrao: bool
    st_ativo: bool | None = None


class FilialTrajetoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seq_filial: int
    seq_trajetoria: int
    st_padrao: bool
    st_ativo: bool
    seq_usuario_inclusao: int
    seq_usuario_alteracao: int | None
    dh_inclusao: datetime
    dh_alteracao: datetime | None
