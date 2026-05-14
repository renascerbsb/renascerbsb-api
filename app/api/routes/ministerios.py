from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ministerio import MinisterioResponse
from app.services.ministerio_service import listar_ministerios

router = APIRouter()

@router.get("/", response_model=list[MinisterioResponse])
def buscar_ministerios(db: Session = Depends(get_db)):
    return listar_ministerios(db)
