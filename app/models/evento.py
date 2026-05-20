from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, DATABASE_SCHEMA


class Evento(Base):
    __tablename__ = "cd_evento"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_evento: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_nome: Mapped[str] = mapped_column(String(150), nullable=False)
    ds_descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    st_evento_fixo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    ds_recorrencia: Mapped[str | None] = mapped_column(String(50), nullable=True)
    st_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    dh_inclusao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
