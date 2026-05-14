from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vinculo import VinculoResponse
from app.services.vinculo_service import listar_vinculos

router = APIRouter()


@router.get("/", response_model=list[VinculoResponse])
def buscar_vinculos(db: Session = Depends(get_db)):
    return listar_vinculos(db)