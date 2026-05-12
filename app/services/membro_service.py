from datetime import date
from app.schemas.membro import MembroResponse


def listar_membros() -> list[MembroResponse]:
    return [
        MembroResponse(
            id=1,
            nome="Ana Souza",
            telefone="61999990000",
            data_nascimento=date(1990, 5, 12),
            cidade_id=1,
            filial_id=1,
            ativo=True
        ),
        MembroResponse(
            id=2,
            nome="João Lima",
            telefone="61988880000",
            data_nascimento=date(1988, 9, 30),
            cidade_id=1,
            filial_id=1,
            ativo=True
        ),
    ]