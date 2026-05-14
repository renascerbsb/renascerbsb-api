from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, DATABASE_SCHEMA


class Filial(Base):
    __tablename__ = "cd_filial"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_filial: Mapped[int] = mapped_column(Integer, primary_key=True)

    ds_nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    st_ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )