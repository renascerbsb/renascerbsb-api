from fastapi import APIRouter
from app.schemas.filial import FilialResponse
from app.services.filial_service import listar_filiais

router = APIRouter()


@router.get("/", response_model=list[FilialResponse])
def buscar_filiais():
    return listar_filiais()