import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.trajetoria_etapa import TrajetoriaEtapa
from app.schemas.trajetoria_etapa import (
    TrajetoriaEtapaCreate,
    TrajetoriaEtapaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

logger = logging.getLogger(__name__)


def listar_etapas(
    db: Session,
    seq_trajetoria: int | None = None,
    st_ativo: bool | None = True,
) -> list[TrajetoriaEtapa]:
    try:
        query = db.query(TrajetoriaEtapa)
        if seq_trajetoria is not None:
            query = query.filter(
                TrajetoriaEtapa.seq_trajetoria == seq_trajetoria
            )
        if st_ativo is not None:
            query = query.filter(TrajetoriaEtapa.st_ativo.is_(st_ativo))
        return query.order_by(
            TrajetoriaEtapa.seq_trajetoria,
            TrajetoriaEtapa.nr_ordem,
        ).all()
    except SQLAlchemyError:
        logger.exception("Erro ao listar etapas das trajetorias")
        raise


def buscar_etapa_por_id(
    db: Session,
    seq_trajetoria_etapa: int,
) -> TrajetoriaEtapa | None:
    try:
        return (
            db.query(TrajetoriaEtapa)
            .filter(
                TrajetoriaEtapa.seq_trajetoria_etapa
                == seq_trajetoria_etapa
            )
            .first()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao buscar etapa da trajetoria")
        raise


def criar_etapa(
    db: Session,
    dados: TrajetoriaEtapaCreate,
    seq_usuario_inclusao: int,
) -> TrajetoriaEtapa:
    try:
        etapa = TrajetoriaEtapa(
            **dados.model_dump(),
            st_ativo=True,
            seq_usuario_inclusao=seq_usuario_inclusao,
        )
        db.add(etapa)
        db.commit()
        db.refresh(etapa)
        return etapa
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Trajetoria, tipo de etapa ou usuario inexistente, ou ordem duplicada"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar etapa da trajetoria")
        raise


def atualizar_etapa(
    db: Session,
    seq_trajetoria_etapa: int,
    dados: TrajetoriaEtapaUpdate,
    seq_usuario_alteracao: int,
) -> TrajetoriaEtapa | None:
    try:
        etapa = buscar_etapa_por_id(db, seq_trajetoria_etapa)
        if etapa is None:
            return None

        valores = dados.model_dump()
        for campo, valor in valores.items():
            if campo != "st_ativo" or valor is not None:
                setattr(etapa, campo, valor)
        etapa.seq_usuario_alteracao = seq_usuario_alteracao
        etapa.dh_alteracao = datetime.now()

        db.commit()
        db.refresh(etapa)
        return etapa
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Relacionamento invalido ou ordem ativa duplicada na trajetoria"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar etapa da trajetoria")
        raise


def inativar_etapa(
    db: Session,
    seq_trajetoria_etapa: int,
    seq_usuario_alteracao: int,
) -> TrajetoriaEtapa | None:
    try:
        etapa = buscar_etapa_por_id(db, seq_trajetoria_etapa)
        if etapa is None:
            return None

        etapa.st_ativo = False
        etapa.seq_usuario_alteracao = seq_usuario_alteracao
        etapa.dh_alteracao = datetime.now()
        db.commit()
        db.refresh(etapa)
        return etapa
    except IntegrityError as erro:
        db.rollback()
        raise ConflitoDeDadosError(
            "Usuario de alteracao inexistente"
        ) from erro
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao inativar etapa da trajetoria")
        raise
