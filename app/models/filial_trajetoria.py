from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, DATABASE_SCHEMA


class FilialTrajetoria(Base):
    __tablename__ = "rl_filial_trajetoria"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_filial: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.cd_filial.seq_filial"),
        primary_key=True,
    )
    seq_trajetoria: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_trajetoria.seq_trajetoria"),
        primary_key=True,
    )
    st_padrao: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    st_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    seq_usuario_inclusao: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_usuario.seq_usuario"),
        nullable=False,
    )
    seq_usuario_alteracao: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_usuario.seq_usuario"),
        nullable=True,
    )
    dh_inclusao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    dh_alteracao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
