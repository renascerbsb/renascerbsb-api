from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, DATABASE_SCHEMA


class Usuario(Base):
    __tablename__ = "tb_usuario"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_usuario: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    ds_nome: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ds_senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    st_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    dh_inclusao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
