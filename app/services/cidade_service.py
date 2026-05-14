from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.cidade import Cidade


def listar_cidades(db: Session):

    try:

        return (
            db.query(Cidade)
            .filter(Cidade.st_ativo.is_(True))
            .order_by(Cidade.ds_nome)
            .all()
        )

    except SQLAlchemyError as e:

        print(f"Erro ao consultar cidades: {e}")

        raise