from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.filial import Filial


def listar_filiais(db: Session) -> list[Filial]:
    try:
        return (
            db.query(Filial)
            .filter(Filial.st_ativo.is_(True))
            .order_by(Filial.ds_nome)
            .all()
        )
    except SQLAlchemyError as e:

        print(f"Erro ao consultar cidades: {e}")

        raise