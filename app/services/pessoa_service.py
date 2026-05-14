import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, joinedload
from app.models.pessoa import Pessoa
from app.schemas.pessoa import PessoaCreate, PessoaUpdate, PessoaVisitanteCreate

logger = logging.getLogger(__name__)


def listar_pessoas(db: Session) -> list[Pessoa]:
    try:
        return (
            db.query(Pessoa)
            .options(
                joinedload(Pessoa.cidade),
                joinedload(Pessoa.filial),
                joinedload(Pessoa.vinculo),
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
        pessoa = Pessoa(
            ds_nome=dados.ds_nome,
            nr_telefone=dados.nr_telefone,
            dt_nascimento=dados.dt_nascimento,
            seq_cidade=dados.seq_cidade,
            seq_filial=dados.seq_filial,
            seq_vinculo=dados.seq_vinculo,
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
    pessoa_create = PessoaCreate(
        ds_nome=dados.ds_nome,
        nr_telefone=dados.nr_telefone,
        dt_nascimento=None,
        seq_cidade=dados.seq_cidade,
        seq_filial=dados.seq_filial,
        seq_vinculo=3
    )

    return criar_pessoa(db, pessoa_create)

def atualizar_pessoa(
    db: Session,
    seq_pessoa: int,
    dados: PessoaUpdate
) -> Pessoa | None:
    try:
        pessoa = buscar_pessoa_por_id(db, seq_pessoa)

        if pessoa is None:
            return None

        pessoa.ds_nome = dados.ds_nome
        pessoa.nr_telefone = dados.nr_telefone
        pessoa.dt_nascimento = dados.dt_nascimento
        pessoa.seq_cidade = dados.seq_cidade
        pessoa.seq_filial = dados.seq_filial
        pessoa.seq_vinculo = dados.seq_vinculo

        if dados.st_ativo is not None:
            pessoa.st_ativo = dados.st_ativo

        db.commit()
        db.refresh(pessoa)

        return pessoa

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar pessoa")
        raise