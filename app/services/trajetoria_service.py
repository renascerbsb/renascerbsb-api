import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.trajetoria import Trajetoria
from app.schemas.trajetoria import TrajetoriaCreate, TrajetoriaUpdate
from app.services.service_errors import ConflitoDeDadosError

logger = logging.getLogger(__name__)


def listar_trajetorias(
    db: Session,
    st_ativo: bool | None = True,
) -> list[Trajetoria]:
    try:
        query = db.query(Trajetoria)
        if st_ativo is not None:
            query = query.filter(Trajetoria.st_ativo.is_(st_ativo))
        return query.order_by(Trajetoria.ds_nome).all()
    except SQLAlchemyError:
        logger.exception("Erro ao listar trajetorias")
        raise


def buscar_trajetoria_por_id(
    db: Session,
    seq_trajetoria: int,
) -> Trajetoria | None:
    try:
        return (
            db.query(Trajetoria)
            .filter(Trajetoria.seq_trajetoria == seq_trajetoria)
            .first()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao buscar trajetoria")
        raise


def criar_trajetoria(
    db: Session,
    dados: TrajetoriaCreate,
    seq_usuario_inclusao: int,
) -> Trajetoria:
    try:
        trajetoria = Trajetoria(
            **dados.model_dump(),
            st_ativo=True,
            seq_usuario_inclusao=seq_usuario_inclusao,
        )
        db.add(trajetoria)
        db.commit()
        db.refresh(trajetoria)
        return trajetoria
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Nome de trajetoria duplicado ou usuario de inclusao inexistente"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar trajetoria")
        raise


def atualizar_trajetoria(
    db: Session,
    seq_trajetoria: int,
    dados: TrajetoriaUpdate,
    seq_usuario_alteracao: int,
) -> Trajetoria | None:
    try:
        trajetoria = buscar_trajetoria_por_id(db, seq_trajetoria)
        if trajetoria is None:
            return None

        valores = dados.model_dump()
        for campo, valor in valores.items():
            if campo != "st_ativo" or valor is not None:
                setattr(trajetoria, campo, valor)
        trajetoria.seq_usuario_alteracao = seq_usuario_alteracao
        trajetoria.dh_alteracao = datetime.now()

        db.commit()
        db.refresh(trajetoria)
        return trajetoria
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Nome de trajetoria duplicado ou usuario de alteracao inexistente"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar trajetoria")
        raise


def inativar_trajetoria(
    db: Session,
    seq_trajetoria: int,
    seq_usuario_alteracao: int,
) -> Trajetoria | None:
    try:
        trajetoria = buscar_trajetoria_por_id(db, seq_trajetoria)
        if trajetoria is None:
            return None

        trajetoria.st_ativo = False
        trajetoria.seq_usuario_alteracao = seq_usuario_alteracao
        trajetoria.dh_alteracao = datetime.now()
        db.commit()
        db.refresh(trajetoria)
        return trajetoria
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Usuario de alteracao inexistente"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao inativar trajetoria")
        raise
