from fastapi import APIRouter
from app.schemas.vinculo import VinculoResponse
from app.services.vinculo_service import listar_vinculos

router = APIRouter()


@router.get("/", response_model=list[VinculoResponse])
def buscar_vinculos():
    return listar_vinculos()