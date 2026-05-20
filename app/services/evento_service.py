import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate

logger = logging.getLogger(__name__)


def listar_eventos(db: Session) -> list[Evento]:
    try:
        return (
            db.query(Evento)
            .filter(Evento.st_ativo.is_(True))
            .order_by(Evento.ds_nome)
            .all()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao listar eventos")
        raise


def buscar_evento_por_id(db: Session, seq_evento: int) -> Evento | None:
    try:
        return (
            db.query(Evento)
            .filter(Evento.seq_evento == seq_evento)
            .filter(Evento.st_ativo.is_(True))
            .first()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao buscar evento por id")
        raise


def criar_evento(db: Session, dados: EventoCreate) -> Evento:
    try:
        evento = Evento(
            ds_nome=dados.ds_nome,
            ds_descricao=dados.ds_descricao,
            st_evento_fixo=dados.st_evento_fixo,
            ds_recorrencia=dados.ds_recorrencia,
            st_ativo=True
        )

        db.add(evento)
        db.commit()
        db.refresh(evento)

        return evento
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar evento")
        raise


def atualizar_evento(
    db: Session,
    seq_evento: int,
    dados: EventoUpdate
) -> Evento | None:
    try:
        evento = buscar_evento_por_id(db, seq_evento)

        if evento is None:
            return None

        evento.ds_nome = dados.ds_nome
        evento.ds_descricao = dados.ds_descricao
        evento.st_evento_fixo = dados.st_evento_fixo
        evento.ds_recorrencia = dados.ds_recorrencia

        if dados.st_ativo is not None:
            evento.st_ativo = dados.st_ativo

        db.commit()
        db.refresh(evento)

        return evento
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar evento")
        raise


def inativar_evento(db: Session, seq_evento: int) -> Evento | None:
    try:
        evento = buscar_evento_por_id(db, seq_evento)

        if evento is None:
            return None

        evento.st_ativo = False
        db.commit()
        db.refresh(evento)

        return evento
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao inativar evento")
        raise
