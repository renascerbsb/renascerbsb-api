from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.pessoa_service as pessoa_service
from app.schemas.pessoa import (PessoaCreate, PessoaResponse, PessoaUpdate, PessoaVisitanteCreate)

router = APIRouter()

@router.get("/", response_model=list[PessoaResponse])
def buscar_pessoas(db: Session = Depends(get_db)):
    return pessoa_service.listar_pessoas(db)

@router.get("/{seq_pessoa}", response_model=PessoaResponse)
def buscar_pessoa(seq_pessoa: int, db: Session = Depends(get_db)):
    pessoa = pessoa_service.buscar_pessoa_por_id(db, seq_pessoa)

    if pessoa is None:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    return pessoa

@router.post( "/", response_model=PessoaResponse, status_code=status.HTTP_201_CREATED)
def criar_pessoa( dados: PessoaCreate, db: Session = Depends(get_db)):
    return pessoa_service.criar_pessoa(db, dados)

@router.post("/visitante", response_model=PessoaResponse, status_code=status.HTTP_201_CREATED)
def criar_visitante(dados: PessoaVisitanteCreate,db: Session = Depends(get_db)):
    return pessoa_service.criar_visitante(db, dados)

@router.put("/{seq_pessoa}", response_model=PessoaResponse)
def atualizar_pessoa(seq_pessoa: int,dados: PessoaUpdate,db: Session = Depends(get_db)):
    
    pessoa = pessoa_service.atualizar_pessoa(db, seq_pessoa, dados)

    if pessoa is None:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    return pessoa