from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.enums import Genero
import app.services.pessoa_service as pessoa_service
from app.schemas.pessoa import (
    PessoaCreate,
    PessoaFiltros,
    PessoaResponse,
    PessoaUpdate,
    PessoaVisitanteCreate,
)

router = APIRouter()

@router.get("/", response_model=list[PessoaResponse])
def buscar_pessoas(
    seq_pessoa: int | None = Query(default=None),
    ds_nome: str | None = Query(default=None),
    nr_telefone: str | None = Query(default=None),
    tp_genero: Genero | None = Query(default=None),
    dt_nascimento: date | None = Query(default=None),
    seq_cidade: int | None = Query(default=None),
    seq_filial: int | None = Query(default=None),
    seq_vinculo: int | None = Query(default=None),
    seq_faixa_etaria: int | None = Query(default=None),
    seq_lider: int | None = Query(default=None),
    seq_lideres: list[int] | None = Query(default=None),
    st_ativo: bool | None = Query(default=True),
    seq_ministerios: list[int] | None = Query(default=None),
    db: Session = Depends(get_db)
):
    filtros_seq_lideres = seq_lideres or []
    if seq_lider is not None:
        filtros_seq_lideres.append(seq_lider)

    filtros = PessoaFiltros(
        seq_pessoa=seq_pessoa,
        ds_nome=ds_nome,
        nr_telefone=nr_telefone,
        tp_genero=tp_genero,
        dt_nascimento=dt_nascimento,
        seq_cidade=seq_cidade,
        seq_filial=seq_filial,
        seq_vinculo=seq_vinculo,
        seq_faixa_etaria=seq_faixa_etaria,
        seq_lideres=filtros_seq_lideres,
        st_ativo=st_ativo,
        seq_ministerios=seq_ministerios or []
    )

    return pessoa_service.listar_pessoas(db, filtros)

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
