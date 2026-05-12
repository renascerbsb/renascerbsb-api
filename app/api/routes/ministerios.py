from fastapi import APIRouter
from app.schemas.ministerio import MinisterioResponse
from app.services.ministerio_service import listar_ministerios

router = APIRouter()


@router.get("/", response_model=list[MinisterioResponse])
def buscar_ministerios():
    return listar_ministerios()