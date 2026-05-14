import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.filial import Filial

logger = logging.getLogger(__name__)

def listar_filiais(db: Session) -> list[Filial]:
    try:
        return (
            db.query(Filial)
            .filter(Filial.st_ativo.is_(True))
            .order_by(Filial.ds_nome)
            .all()
        )
    except SQLAlchemyError as e:
        logger.exception("Erro ao listar filiais")
        raise