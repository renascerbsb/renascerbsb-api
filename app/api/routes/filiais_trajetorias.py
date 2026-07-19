from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.services.filial_trajetoria_service as filial_trajetoria_service
from app.api.routes.auth import obter_usuario_autenticado
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.filial_trajetoria import (
    FilialTrajetoriaCreate,
    FilialTrajetoriaResponse,
    FilialTrajetoriaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

router = APIRouter()


@router.get("/", response_model=list[FilialTrajetoriaResponse])
def listar_filiais_trajetorias(
    seq_filial: int | None = Query(default=None, gt=0),
    seq_trajetoria: int | None = Query(default=None, gt=0),
    st_padrao: bool | None = Query(default=None),
    st_ativo: bool | None = Query(default=True),
    db: Session = Depends(get_db),
):
    return filial_trajetoria_service.listar_filiais_trajetorias(
        db,
        seq_filial,
        seq_trajetoria,
        st_padrao,
        st_ativo,
    )


@router.get(
    "/{seq_filial}/{seq_trajetoria}",
    response_model=FilialTrajetoriaResponse,
)
def buscar_filial_trajetoria(
    seq_filial: int,
    seq_trajetoria: int,
    db: Session = Depends(get_db),
):
    filial_trajetoria = filial_trajetoria_service.buscar_filial_trajetoria(
        db,
        seq_filial,
        seq_trajetoria,
    )
    if filial_trajetoria is None:
        raise HTTPException(
            status_code=404,
            detail="Trajetoria da filial nao encontrada",
        )
    return filial_trajetoria


@router.post(
    "/",
    response_model=FilialTrajetoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_filial_trajetoria(
    dados: FilialTrajetoriaCreate,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        return filial_trajetoria_service.criar_filial_trajetoria(
            db,
            dados,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro


@router.put(
    "/{seq_filial}/{seq_trajetoria}",
    response_model=FilialTrajetoriaResponse,
)
def atualizar_filial_trajetoria(
    seq_filial: int,
    seq_trajetoria: int,
    dados: FilialTrajetoriaUpdate,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        filial_trajetoria = (
            filial_trajetoria_service.atualizar_filial_trajetoria(
                db,
                seq_filial,
                seq_trajetoria,
                dados,
                usuario.seq_usuario,
            )
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if filial_trajetoria is None:
        raise HTTPException(
            status_code=404,
            detail="Trajetoria da filial nao encontrada",
        )
    return filial_trajetoria


@router.delete(
    "/{seq_filial}/{seq_trajetoria}",
    response_model=FilialTrajetoriaResponse,
)
def inativar_filial_trajetoria(
    seq_filial: int,
    seq_trajetoria: int,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        filial_trajetoria = (
            filial_trajetoria_service.inativar_filial_trajetoria(
                db,
                seq_filial,
                seq_trajetoria,
                usuario.seq_usuario,
            )
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if filial_trajetoria is None:
        raise HTTPException(
            status_code=404,
            detail="Trajetoria da filial nao encontrada",
        )
    return filial_trajetoria
