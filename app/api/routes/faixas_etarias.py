from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.faixa_etaria import FaixaEtariaResponse
from app.services.faixa_etaria_service import listar_faixas_etarias

router = APIRouter()


@router.get("/", response_model=list[FaixaEtariaResponse])
def buscar_faixas_etarias(db: Session = Depends(get_db)):
    return listar_faixas_etarias(db)
