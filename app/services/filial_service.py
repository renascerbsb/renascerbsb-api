from app.schemas.filial import FilialResponse


def listar_filiais() -> list[FilialResponse]:
    return [
        FilialResponse(id=1, nome="Renascer Hall BSB"),
        FilialResponse(id=2, nome="Renascer Jardim Ingá"),
    ]