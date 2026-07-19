from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, DATABASE_SCHEMA
from app.models.usuario import Usuario


class TrajetoriaEtapa(Base):
    __tablename__ = "tb_trajetoria_etapa"
    __table_args__ = {"schema": DATABASE_SCHEMA}

    seq_trajetoria_etapa: Mapped[int] = mapped_column(Integer, primary_key=True)
    seq_trajetoria: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{DATABASE_SCHEMA}.tb_trajetoria.seq_trajetoria"),
        nullable=False,
    )
    seq_etapa_trajetoria: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            f"{DATABASE_SCHEMA}.cd_etapa_trajetoria.seq_etapa_trajetoria"
        ),
        nullable=False,
    )
    ds_nome: Mapped[str] = mapped_column(String(150), nullable=False)
    ds_descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    nr_ordem: Mapped[int] = mapped_column(Integer, nullable=False)
    nr_prazo_dias: Mapped[int | None] = mapped_column(Integer, nullable=True)
    st_obrigatoria: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    st_permite_pular: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    st_exige_observacao: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
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

    usuario_inclusao: Mapped[Usuario] = relationship(
        Usuario,
        foreign_keys=[seq_usuario_inclusao],
        lazy="joined",
    )
    usuario_alteracao: Mapped[Usuario | None] = relationship(
        Usuario,
        foreign_keys=[seq_usuario_alteracao],
        lazy="joined",
    )

    @property
    def ds_nome_usuario_inclusao(self) -> str | None:
        return self.usuario_inclusao.ds_nome if self.usuario_inclusao else None

    @property
    def ds_nome_usuario_alteracao(self) -> str | None:
        return self.usuario_alteracao.ds_nome if self.usuario_alteracao else None
