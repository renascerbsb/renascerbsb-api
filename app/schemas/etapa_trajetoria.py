from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EtapaTrajetoriaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    ds_nome: str = Field(min_length=1, max_length=100)
    ds_descricao: str | None = Field(default=None, max_length=300)
    color_tag: str = Field(min_length=1)
    prime_icon: str = Field(default="pi-list-check", max_length=15)

    @field_validator("prime_icon", mode="before")
    @classmethod
    def preencher_prime_icon_padrao(cls, valor: Any) -> Any:
        if valor is None:
            return "pi-list-check"
        if isinstance(valor, str) and not valor.strip():
            return "pi-list-check"
        return valor


class EtapaTrajetoriaCreate(EtapaTrajetoriaBase):
    pass


class EtapaTrajetoriaUpdate(EtapaTrajetoriaBase):
    st_ativo: bool | None = None


class EtapaTrajetoriaResponse(EtapaTrajetoriaBase):
    model_config = ConfigDict(from_attributes=True)

    seq_etapa_trajetoria: int
    st_ativo: bool
