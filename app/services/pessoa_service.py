import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.pessoa import Pessoa

logger = logging.getLogger(__name__)

def listar_pessoas(db: Session) -> list[Pessoa]:
    try:
        return (
            db.query(Pessoa)
            .filter(Pessoa.st_ativo.is_(True))
            .order_by(Pessoa.ds_nome)
            .all()
        )
    except SQLAlchemyError as e:
        logger.exception("Erro ao listar pessoas")
        raise