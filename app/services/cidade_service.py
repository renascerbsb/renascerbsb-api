import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.cidade import Cidade


logger = logging.getLogger(__name__)

def listar_cidades(db: Session):

    try:

        return (
            db.query(Cidade)
            .filter(Cidade.st_ativo.is_(True))
            .order_by(Cidade.ds_nome)
            .all()
        )

    except SQLAlchemyError as e:
        logger.exception("Erro ao listar cidades")
        raise