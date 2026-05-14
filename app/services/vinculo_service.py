from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.vinculo import Vinculo


def listar_vinculos(db: Session) -> list[Vinculo]:

    try:

        return (
            db.query(Vinculo)
            .filter(Vinculo.st_ativo.is_(True))
            .order_by(Vinculo.ds_nome)
            .all()
        )

    except SQLAlchemyError as e:

        print(f"Erro ao listar vínculos: {e}")

        raise