from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.services.etapa_trajetoria_service as etapa_service
from app.core.database import get_db
from app.schemas.etapa_trajetoria import (
    EtapaTrajetoriaCreate,
    EtapaTrajetoriaResponse,
    EtapaTrajetoriaUpdate,
)
from app.services.service_errors import ConflitoDeDadosError

router = APIRouter()


@router.get("/", response_model=list[EtapaTrajetoriaResponse])
def listar_etapas_trajetoria(
    st_ativo: bool | None = Query(default=True),
    db: Session = Depends(get_db),
):
    return etapa_service.listar_etapas_trajetoria(db, st_ativo)


@router.get("/{seq_etapa_trajetoria}", response_model=EtapaTrajetoriaResponse)
def buscar_etapa_trajetoria(
    seq_etapa_trajetoria: int,
    db: Session = Depends(get_db),
):
    etapa = etapa_service.buscar_etapa_trajetoria_por_id(
        db,
        seq_etapa_trajetoria,
    )
    if etapa is None:
        raise HTTPException(status_code=404, detail="Etapa de trajetoria nao encontrada")
    return etapa


@router.post(
    "/",
    response_model=EtapaTrajetoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_etapa_trajetoria(
    dados: EtapaTrajetoriaCreate,
    db: Session = Depends(get_db),
):
    try:
        return etapa_service.criar_etapa_trajetoria(db, dados)
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro


@router.put("/{seq_etapa_trajetoria}", response_model=EtapaTrajetoriaResponse)
def atualizar_etapa_trajetoria(
    seq_etapa_trajetoria: int,
    dados: EtapaTrajetoriaUpdate,
    db: Session = Depends(get_db),
):
    try:
        etapa = etapa_service.atualizar_etapa_trajetoria(
            db,
            seq_etapa_trajetoria,
            dados,
        )
    except ConflitoDeDadosError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    if etapa is None:
        raise HTTPException(status_code=404, detail="Etapa de trajetoria nao encontrada")
    return etapa


@router.delete("/{seq_etapa_trajetoria}", response_model=EtapaTrajetoriaResponse)
def inativar_etapa_trajetoria(
    seq_etapa_trajetoria: int,
    db: Session = Depends(get_db),
):
    etapa = etapa_service.inativar_etapa_trajetoria(db, seq_etapa_trajetoria)
    if etapa is None:
        raise HTTPException(status_code=404, detail="Etapa de trajetoria nao encontrada")
    return etapa
