from datetime import datetime
from pydantic import BaseModel


class EventoBase(BaseModel):
    ds_nome: str
    ds_descricao: str | None = None
    st_evento_fixo: bool = False
    ds_recorrencia: str | None = None


class EventoCreate(EventoBase):
    pass


class EventoUpdate(EventoBase):
    st_ativo: bool | None = None


class EventoResponse(EventoBase):
    seq_evento: int
    st_ativo: bool
    dh_inclusao: datetime

    class Config:
        from_attributes = True
