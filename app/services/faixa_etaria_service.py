import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.faixa_etaria import FaixaEtaria

logger = logging.getLogger(__name__)


def listar_faixas_etarias(db: Session) -> list[FaixaEtaria]:
    try:
        logger.info("Listando faixas etarias ativas")

        return (
            db.query(FaixaEtaria)
            .filter(FaixaEtaria.st_ativo.is_(True))
            .order_by(FaixaEtaria.nr_idade_minima, FaixaEtaria.ds_nome)
            .all()
        )

    except SQLAlchemyError:
        logger.exception("Erro ao listar faixas etarias")
        raise
