from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.ministerio import Ministerio

def listar_ministerios(db: Session) -> list[Ministerio]:
    try:
        return (
            db.query(Ministerio)
            .filter(Ministerio.st_ativo.is_(True))
            .order_by(Ministerio.ds_nome)
            .all()
        )
    except SQLAlchemyError as e:

        print(f"Erro: {e}")

        raise