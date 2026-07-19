import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.etapa_trajetoria import EtapaTrajetoria
from app.schemas.etapa_trajetoria import (
    EtapaTrajetoriaCreate,
    EtapaTrajetoriaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

logger = logging.getLogger(__name__)


def listar_etapas_trajetoria(
    db: Session,
    st_ativo: bool | None = True,
) -> list[EtapaTrajetoria]:
    try:
        query = db.query(EtapaTrajetoria)
        if st_ativo is not None:
            query = query.filter(EtapaTrajetoria.st_ativo.is_(st_ativo))
        return query.order_by(EtapaTrajetoria.ds_nome).all()
    except SQLAlchemyError:
        logger.exception("Erro ao listar etapas de trajetoria")
        raise


def buscar_etapa_trajetoria_por_id(
    db: Session,
    seq_etapa_trajetoria: int,
) -> EtapaTrajetoria | None:
    try:
        return (
            db.query(EtapaTrajetoria)
            .filter(
                EtapaTrajetoria.seq_etapa_trajetoria == seq_etapa_trajetoria
            )
            .first()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao buscar etapa de trajetoria")
        raise


def criar_etapa_trajetoria(
    db: Session,
    dados: EtapaTrajetoriaCreate,
) -> EtapaTrajetoria:
    try:
        etapa = EtapaTrajetoria(**dados.model_dump(), st_ativo=True)
        db.add(etapa)
        db.commit()
        db.refresh(etapa)
        return etapa
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Ja existe uma etapa de trajetoria com esse nome"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar etapa de trajetoria")
        raise


def atualizar_etapa_trajetoria(
    db: Session,
    seq_etapa_trajetoria: int,
    dados: EtapaTrajetoriaUpdate,
) -> EtapaTrajetoria | None:
    try:
        etapa = buscar_etapa_trajetoria_por_id(db, seq_etapa_trajetoria)
        if etapa is None:
            return None

        for campo, valor in dados.model_dump().items():
            if campo != "st_ativo" or valor is not None:
                setattr(etapa, campo, valor)

        db.commit()
        db.refresh(etapa)
        return etapa
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Ja existe uma etapa de trajetoria com esse nome"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar etapa de trajetoria")
        raise


def inativar_etapa_trajetoria(
    db: Session,
    seq_etapa_trajetoria: int,
) -> EtapaTrajetoria | None:
    try:
        etapa = buscar_etapa_trajetoria_por_id(db, seq_etapa_trajetoria)
        if etapa is None:
            return None

        etapa.st_ativo = False
        db.commit()
        db.refresh(etapa)
        return etapa
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao inativar etapa de trajetoria")
        raise
