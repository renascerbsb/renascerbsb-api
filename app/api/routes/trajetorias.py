from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.services.trajetoria_service as trajetoria_service
from app.api.routes.auth import obter_usuario_autenticado
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.trajetoria import (
    TrajetoriaCreate,
    TrajetoriaResponse,
    TrajetoriaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

router = APIRouter()


@router.get("/", response_model=list[TrajetoriaResponse])
def listar_trajetorias(
    st_ativo: bool | None = Query(default=True),
    db: Session = Depends(get_db),
):
    return trajetoria_service.listar_trajetorias(db, st_ativo)


@router.get("/{seq_trajetoria}", response_model=TrajetoriaResponse)
def buscar_trajetoria(
    seq_trajetoria: int,
    db: Session = Depends(get_db),
):
    trajetoria = trajetoria_service.buscar_trajetoria_por_id(db, seq_trajetoria)
    if trajetoria is None:
        raise HTTPException(status_code=404, detail="Trajetoria nao encontrada")
    return trajetoria


@router.post(
    "/",
    response_model=TrajetoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_trajetoria(
    dados: TrajetoriaCreate,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        return trajetoria_service.criar_trajetoria(
            db,
            dados,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro


@router.put("/{seq_trajetoria}", response_model=TrajetoriaResponse)
def atualizar_trajetoria(
    seq_trajetoria: int,
    dados: TrajetoriaUpdate,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        trajetoria = trajetoria_service.atualizar_trajetoria(
            db,
            seq_trajetoria,
            dados,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if trajetoria is None:
        raise HTTPException(status_code=404, detail="Trajetoria nao encontrada")
    return trajetoria


@router.delete("/{seq_trajetoria}", response_model=TrajetoriaResponse)
def inativar_trajetoria(
    seq_trajetoria: int,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        trajetoria = trajetoria_service.inativar_trajetoria(
            db,
            seq_trajetoria,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if trajetoria is None:
        raise HTTPException(status_code=404, detail="Trajetoria nao encontrada")
    return trajetoria
