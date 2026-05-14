from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.pessoa import PessoaResponse
from app.services.pessoa_service import listar_pessoas

router = APIRouter()


@router.get("/", response_model=list[PessoaResponse])
def buscar_pessoas(db: Session = Depends(get_db)):
    return listar_pessoas(db)