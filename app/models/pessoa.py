from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, DATABASE_SCHEMA


class Pessoa(Base):
    __tablename__ = "tb_pessoa"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_pessoa: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_nome: Mapped[str] = mapped_column(String(200), nullable=False)
    nr_telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    dt_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)

    seq_cidade: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.cd_cidade.seq_cidade"),
        nullable=True
    )

    seq_filial: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.cd_filial.seq_filial"),
        nullable=True
    )

    seq_vinculo: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.cd_vinculo.seq_vinculo"),
        nullable=True
    )

    ministerios = relationship(
        "Ministerio",
        secondary=f"{DATABASE_SCHEMA}.rl_pessoa_ministerio",
        primaryjoin=f"Pessoa.seq_pessoa == PessoaMinisterio.seq_pessoa",
        secondaryjoin=f"Ministerio.seq_ministerio == PessoaMinisterio.seq_ministerio",
        viewonly=True
    )

    st_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    cidade = relationship("Cidade")
    filial = relationship("Filial")
    vinculo = relationship("Vinculo")