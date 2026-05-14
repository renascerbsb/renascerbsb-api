import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.ministerio import Ministerio

logger = logging.getLogger(__name__)

def listar_ministerios(db: Session) -> list[Ministerio]:
    try:
        return (
            db.query(Ministerio)
            .filter(Ministerio.st_ativo.is_(True))
            .order_by(Ministerio.ds_nome)
            .all()
        )
    except SQLAlchemyError as e:
        logger.exception("Erro ao listar ministerios")
        raise