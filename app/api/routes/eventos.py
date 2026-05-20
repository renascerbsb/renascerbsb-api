from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.evento_service as evento_service
from app.core.database import get_db
from app.schemas.evento import EventoCreate, EventoResponse, EventoUpdate

router = APIRouter()


@router.get("/", response_model=list[EventoResponse])
def buscar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar_eventos(db)


@router.get("/{seq_evento}", response_model=EventoResponse)
def buscar_evento(seq_evento: int, db: Session = Depends(get_db)):
    evento = evento_service.buscar_evento_por_id(db, seq_evento)

    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )

    return evento


@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(dados: EventoCreate, db: Session = Depends(get_db)):
    return evento_service.criar_evento(db, dados)


@router.put("/{seq_evento}", response_model=EventoResponse)
def atualizar_evento(
    seq_evento: int,
    dados: EventoUpdate,
    db: Session = Depends(get_db)
):
    evento = evento_service.atualizar_evento(db, seq_evento, dados)

    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )

    return evento


@router.delete("/{seq_evento}", response_model=EventoResponse)
def inativar_evento(seq_evento: int, db: Session = Depends(get_db)):
    evento = evento_service.inativar_evento(db, seq_evento)

    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )

    return evento
