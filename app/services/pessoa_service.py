from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.pessoa import Pessoa


def listar_pessoas(db: Session) -> list[Pessoa]:
    try:
        return (
            db.query(Pessoa)
            .filter(Pessoa.st_ativo.is_(True))
            .order_by(Pessoa.ds_nome)
            .all()
        )
    except SQLAlchemyError as e:

        print(f"Erro: {e}")

        raise