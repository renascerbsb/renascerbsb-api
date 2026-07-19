from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, DATABASE_SCHEMA


class EtapaTrajetoria(Base):
    __tablename__ = "cd_etapa_trajetoria"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_etapa_trajetoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_nome: Mapped[str] = mapped_column(String(100), nullable=False)
    ds_descricao: Mapped[str | None] = mapped_column(String(300), nullable=True)
    color_tag: Mapped[str] = mapped_column(String, nullable=False)
    prime_icon: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        default="pi-list-check",
    )
    st_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
