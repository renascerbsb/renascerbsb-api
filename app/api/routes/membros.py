from fastapi import APIRouter
from app.schemas.membro import MembroResponse
from app.services.membro_service import listar_membros

router = APIRouter()

@router.get("/", response_model=list[MembroResponse])
def buscar_membros():
    return listar_membros()