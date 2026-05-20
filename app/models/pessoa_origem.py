from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, DATABASE_SCHEMA


class PessoaOrigem(Base):
    __tablename__ = "tb_pessoa_origem"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_pessoa_origem: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_como_conheceu: Mapped[str] = mapped_column(String(50), nullable=False)
    st_frequenta_igreja: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    ds_nome_convidou: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seq_evento_frequentou: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.cd_evento.seq_evento"),
        nullable=True
    )
    ds_observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    seq_pessoa: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_pessoa.seq_pessoa"),
        nullable=False,
        unique=True
    )
    seq_pessoa_inclusao: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_pessoa.seq_pessoa"),
        nullable=False
    )
    dh_inclusao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    evento_frequentou = relationship("Evento")
    pessoa = relationship("Pessoa", foreign_keys=[seq_pessoa])
    pessoa_inclusao = relationship("Pessoa", foreign_keys=[seq_pessoa_inclusao])
