import logging
from datetime import date
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from app.models.faixa_etaria import FaixaEtaria
from app.models.pessoa import Pessoa
from app.models.pessoa_origem import PessoaOrigem
from app.schemas.pessoa import PessoaCreate, PessoaUpdate, PessoaVisitanteCreate

logger = logging.getLogger(__name__)


def calcular_idade(dt_nascimento: date, dt_referencia: date) -> int:
    idade = dt_referencia.year - dt_nascimento.year

    if (dt_referencia.month, dt_referencia.day) < (
        dt_nascimento.month,
        dt_nascimento.day
    ):
        idade -= 1

    return idade


def buscar_seq_faixa_etaria_por_nascimento(
    db: Session,
    dt_nascimento: date | None
) -> int | None:
    if dt_nascimento is None:
        return None

    dt_referencia = db.query(func.current_date()).scalar()
    idade = calcular_idade(dt_nascimento, dt_referencia)

    faixa_etaria = (
        db.query(FaixaEtaria)
        .filter(FaixaEtaria.st_ativo.is_(True))
        .filter(FaixaEtaria.nr_idade_minima <= idade)
        .filter(
            (FaixaEtaria.nr_idade_maxima.is_(None))
            | (FaixaEtaria.nr_idade_maxima >= idade)
        )
        .first()
    )

    if faixa_etaria is None:
        return None

    return faixa_etaria.seq_faixa_etaria


def listar_pessoas(db: Session) -> list[Pessoa]:
    try:
        return (
            db.query(Pessoa)
            .options(
                joinedload(Pessoa.cidade),
                joinedload(Pessoa.filial),
                joinedload(Pessoa.vinculo),
                joinedload(Pessoa.faixa_etaria),
                joinedload(Pessoa.lider),
                joinedload(Pessoa.ministerios),
            )
            .filter(Pessoa.st_ativo.is_(True))
            .order_by(Pessoa.ds_nome)
            .all()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao listar pessoas")
        raise


def buscar_pessoa_por_id(db: Session, seq_pessoa: int) -> Pessoa | None:
    try:
        return (
            db.query(Pessoa)
            .options(
                joinedload(Pessoa.cidade),
                joinedload(Pessoa.filial),
                joinedload(Pessoa.vinculo),
                joinedload(Pessoa.faixa_etaria),
                joinedload(Pessoa.lider),
                joinedload(Pessoa.ministerios),
            )
            .filter(Pessoa.seq_pessoa == seq_pessoa)
            .filter(Pessoa.st_ativo.is_(True))
            .first()
        )
    except SQLAlchemyError:
        logger.exception("Erro ao buscar pessoa por id")
        raise

def criar_pessoa(db: Session, dados: PessoaCreate) -> Pessoa:
    try:
        seq_faixa_etaria = dados.seq_faixa_etaria

        if dados.dt_nascimento is not None:
            seq_faixa_etaria = buscar_seq_faixa_etaria_por_nascimento(
                db,
                dados.dt_nascimento
            )

        pessoa = Pessoa(
            ds_nome=dados.ds_nome,
            nr_telefone=dados.nr_telefone,
            dt_nascimento=dados.dt_nascimento,
            seq_cidade=dados.seq_cidade,
            seq_filial=dados.seq_filial,
            seq_vinculo=dados.seq_vinculo,
            seq_faixa_etaria=seq_faixa_etaria,
            seq_lider=dados.seq_lider,
            st_ativo=True
        )

        db.add(pessoa)
        db.commit()
        db.refresh(pessoa)

        return pessoa

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar pessoa")
        raise


def criar_visitante(db: Session, dados: PessoaVisitanteCreate) -> Pessoa:
    try:
        pessoa = Pessoa(
            ds_nome=dados.ds_nome,
            nr_telefone=dados.nr_telefone,
            dt_nascimento=None,
            seq_cidade=dados.seq_cidade,
            seq_filial=dados.seq_filial,
            seq_vinculo=3,
            seq_faixa_etaria=None,
            seq_lider=None,
            st_ativo=True
        )

        db.add(pessoa)
        db.flush()

        pessoa_origem = PessoaOrigem(
            ds_como_conheceu=dados.ds_como_conheceu.value,
            st_frequenta_igreja=dados.st_frequenta_igreja,
            ds_nome_convidou=dados.ds_nome_convidou,
            seq_evento_frequentou=dados.seq_evento_frequentou,
            ds_observacao=dados.ds_observacao,
            seq_pessoa=pessoa.seq_pessoa,
            seq_pessoa_inclusao=pessoa.seq_pessoa
        )

        db.add(pessoa_origem)
        db.commit()
        db.refresh(pessoa)

        return pessoa
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar visitante")
        raise

def atualizar_pessoa(
    db: Session,
    seq_pessoa: int,
    dados: PessoaUpdate
) -> Pessoa | None:
    try:
        pessoa = buscar_pessoa_por_id(db, seq_pessoa)

        if pessoa is None:
            return None

        seq_faixa_etaria = dados.seq_faixa_etaria

        if dados.dt_nascimento is not None:
            seq_faixa_etaria = buscar_seq_faixa_etaria_por_nascimento(
                db,
                dados.dt_nascimento
            )

        pessoa.ds_nome = dados.ds_nome
        pessoa.nr_telefone = dados.nr_telefone
        pessoa.dt_nascimento = dados.dt_nascimento
        pessoa.seq_cidade = dados.seq_cidade
        pessoa.seq_filial = dados.seq_filial
        pessoa.seq_vinculo = dados.seq_vinculo
        pessoa.seq_faixa_etaria = seq_faixa_etaria
        pessoa.seq_lider = dados.seq_lider

        if dados.st_ativo is not None:
            pessoa.st_ativo = dados.st_ativo

        db.commit()
        db.refresh(pessoa)

        return pessoa

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar pessoa")
        raise
