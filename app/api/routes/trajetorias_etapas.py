from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.services.trajetoria_etapa_service as etapa_service
from app.api.routes.auth import obter_usuario_autenticado
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.trajetoria_etapa import (
    TrajetoriaEtapaCreate,
    TrajetoriaEtapaResponse,
    TrajetoriaEtapaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

router = APIRouter()


@router.get("/", response_model=list[TrajetoriaEtapaResponse])
def listar_etapas(
    seq_trajetoria: int | None = Query(default=None, gt=0),
    st_ativo: bool | None = Query(default=True),
    db: Session = Depends(get_db),
):
    return etapa_service.listar_etapas(db, seq_trajetoria, st_ativo)


@router.get("/{seq_trajetoria_etapa}", response_model=TrajetoriaEtapaResponse)
def buscar_etapa(
    seq_trajetoria_etapa: int,
    db: Session = Depends(get_db),
):
    etapa = etapa_service.buscar_etapa_por_id(db, seq_trajetoria_etapa)
    if etapa is None:
        raise HTTPException(status_code=404, detail="Etapa da trajetoria nao encontrada")
    return etapa


@router.post(
    "/",
    response_model=TrajetoriaEtapaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_etapa(
    dados: TrajetoriaEtapaCreate,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        return etapa_service.criar_etapa(
            db,
            dados,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro


@router.put("/{seq_trajetoria_etapa}", response_model=TrajetoriaEtapaResponse)
def atualizar_etapa(
    seq_trajetoria_etapa: int,
    dados: TrajetoriaEtapaUpdate,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        etapa = etapa_service.atualizar_etapa(
            db,
            seq_trajetoria_etapa,
            dados,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if etapa is None:
        raise HTTPException(status_code=404, detail="Etapa da trajetoria nao encontrada")
    return etapa


@router.delete("/{seq_trajetoria_etapa}", response_model=TrajetoriaEtapaResponse)
def inativar_etapa(
    seq_trajetoria_etapa: int,
    usuario: Usuario = Depends(obter_usuario_autenticado),
    db: Session = Depends(get_db),
):
    try:
        etapa = etapa_service.inativar_etapa(
            db,
            seq_trajetoria_etapa,
            usuario.seq_usuario,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if etapa is None:
        raise HTTPException(status_code=404, detail="Etapa da trajetoria nao encontrada")
    return etapa
