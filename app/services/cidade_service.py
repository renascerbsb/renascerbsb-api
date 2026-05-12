from app.schemas.cidade import CidadeResponse


def listar_cidades() -> list[CidadeResponse]:
    return [
        CidadeResponse(id=1, nome="Brasília", uf="DF"),
        CidadeResponse(id=2, nome="Goiânia", uf="GO"),
        CidadeResponse(id=3, nome="Valparaíso", uf="GO"),
        CidadeResponse(id=4, nome="Águas Lindas", uf="GO"),
    ]