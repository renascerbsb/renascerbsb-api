import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.filial_trajetoria import FilialTrajetoria
from app.schemas.filial_trajetoria import (
    FilialTrajetoriaCreate,
    FilialTrajetoriaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

logger = logging.getLogger(__name__)


MENSAGEM_CONFLITO = (
    "Filial, trajetoria ou usuario inexistente, relacionamento duplicado "
    "ou outra trajetoria padrao ativa para a filial"
)


def listar_filiais_trajetorias(
    db: Session,
    seq_filial: int | None = None,
    seq_trajetoria: int | None = None,
    st_padrao: bool | None = None,
    st_ativo: bool | None = True,
) -> list[FilialTrajetoria]:
    try:
        query = db.query(FilialTrajetoria)
        if seq_filial is not None:
            query = query.filter(FilialTrajetoria.seq_filial == seq_filial)
        if seq_trajetoria is not None:
            query = query.filter(
                FilialTrajetoria.seq_trajetoria == seq_trajetoria
            )
        if st_padrao is not None:
            query = query.filter(FilialTrajetoria.st_padrao.is_(st_padrao))
        if st_ativo is not None:
            query = query.filter(FilialTrajetoria.st_ativo.is_(st_ativo))

        return query.order_by(
            FilialTrajetoria.seq_filial,
            FilialTrajetoria.seq_trajetoria,
        ).all()
    except SQLAlchemyError:
        logger.exception("Erro ao listar trajetorias das filiais")
        raise


def buscar_filial_trajetoria(
    db: Session,
    seq_filial: int,
    seq_trajetoria: int,
) -> FilialTrajetoria | None:
    try:
        return (
            db.query(FilialTrajetoria)
            .filter(FilialTrajetoria.seq_filial == seq_filial)
            .filter(FilialTrajetoria.seq_trajetoria == seq_trajetoria)
            .first()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao buscar trajetoria da filial")
        raise


def criar_filial_trajetoria(
    db: Session,
    dados: FilialTrajetoriaCreate,
    seq_usuario_inclusao: int,
) -> FilialTrajetoria:
    try:
        filial_trajetoria = FilialTrajetoria(
            **dados.model_dump(),
            st_ativo=True,
            seq_usuario_inclusao=seq_usuario_inclusao,
        )
        db.add(filial_trajetoria)
        db.commit()
        db.refresh(filial_trajetoria)
        return filial_trajetoria
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(MENSAGEM_CONFLITO) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar trajetoria da filial")
        raise


def atualizar_filial_trajetoria(
    db: Session,
    seq_filial: int,
    seq_trajetoria: int,
    dados: FilialTrajetoriaUpdate,
    seq_usuario_alteracao: int,
) -> FilialTrajetoria | None:
    try:
        filial_trajetoria = buscar_filial_trajetoria(
            db,
            seq_filial,
            seq_trajetoria,
        )
        if filial_trajetoria is None:
            return None

        filial_trajetoria.st_padrao = dados.st_padrao
        if dados.st_ativo is not None:
            filial_trajetoria.st_ativo = dados.st_ativo
        filial_trajetoria.seq_usuario_alteracao = seq_usuario_alteracao
        filial_trajetoria.dh_alteracao = datetime.now()

        db.commit()
        db.refresh(filial_trajetoria)
        return filial_trajetoria
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(MENSAGEM_CONFLITO) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar trajetoria da filial")
        raise


def inativar_filial_trajetoria(
    db: Session,
    seq_filial: int,
    seq_trajetoria: int,
    seq_usuario_alteracao: int,
) -> FilialTrajetoria | None:
    try:
        filial_trajetoria = buscar_filial_trajetoria(
            db,
            seq_filial,
            seq_trajetoria,
        )
        if filial_trajetoria is None:
            return None

        filial_trajetoria.st_ativo = False
        filial_trajetoria.seq_usuario_alteracao = seq_usuario_alteracao
        filial_trajetoria.dh_alteracao = datetime.now()
        db.commit()
        db.refresh(filial_trajetoria)
        return filial_trajetoria
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(MENSAGEM_CONFLITO) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao inativar trajetoria da filial")
        raise
