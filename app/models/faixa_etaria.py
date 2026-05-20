from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, DATABASE_SCHEMA


class FaixaEtaria(Base):
    __tablename__ = "cd_faixa_etaria"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_faixa_etaria: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_nome: Mapped[str] = mapped_column(String(150), nullable=False)
    nr_idade_minima: Mapped[int] = mapped_column(Integer, nullable=False)
    nr_idade_maxima: Mapped[int | None] = mapped_column(Integer, nullable=True)
    st_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
