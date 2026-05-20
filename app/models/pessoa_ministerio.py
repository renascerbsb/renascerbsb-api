from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, DATABASE_SCHEMA


class PessoaMinisterio(Base):
    __tablename__ = "rl_pessoa_ministerio"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_pessoa: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_pessoa.seq_pessoa"),
        primary_key=True
    )

    seq_ministerio: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.cd_ministerio.seq_ministerio"),
        primary_key=True
    )

    dh_inclusao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
