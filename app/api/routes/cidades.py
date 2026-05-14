from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cidade import CidadeResponse
from app.services.cidade_service import listar_cidades

router = APIRouter()


@router.get("/", response_model=list[CidadeResponse])
def buscar_cidades(db: Session = Depends(get_db)):
    return listar_cidades(db)