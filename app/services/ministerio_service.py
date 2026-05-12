from app.schemas.ministerio import MinisterioResponse


def listar_ministerios() -> list[MinisterioResponse]:
    return [
        MinisterioResponse(id=1, nome="Ministério infantil"),
        MinisterioResponse(id=2, nome="Decoração"),
        MinisterioResponse(id=3, nome="Louvor"),
        MinisterioResponse(id=4, nome="Comunicação"),
        MinisterioResponse(id=5, nome="Líder de célula"),
        MinisterioResponse(id=6, nome="Adote"),
    ]