from fastapi import APIRouter
from app.schemas.cidade import CidadeResponse
from app.services.cidade_service import listar_cidades

router = APIRouter()


@router.get("/", response_model=list[CidadeResponse])
def buscar_cidades():
    return listar_cidades()