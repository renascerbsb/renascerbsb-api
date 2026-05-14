from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.filial import FilialResponse
from app.services.filial_service import listar_filiais

router = APIRouter()


@router.get("/", response_model=list[FilialResponse])
def buscar_filiais(
    db: Session = Depends(get_db)
):
    return listar_filiais(db)