import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.vinculo import Vinculo

logger = logging.getLogger(__name__)

def listar_vinculos(db: Session) -> list[Vinculo]:
    try:
        logger.info("Listando vínculos ativos")

        return (
            db.query(Vinculo)
            .filter(Vinculo.st_ativo.is_(True))
            .order_by(Vinculo.ds_nome)
            .all()
        )

    except SQLAlchemyError:
        logger.exception("Erro ao listar vínculos")
        raise