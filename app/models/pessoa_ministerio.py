from sqlalchemy import Boolean, ForeignKey, Integer
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

    st_ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )