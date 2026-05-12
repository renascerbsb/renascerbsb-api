from app.schemas.vinculo import VinculoResponse


def listar_vinculos() -> list[VinculoResponse]:
    return [
        VinculoResponse(id=6, nome="Bispo(a)"),
        VinculoResponse(id=2, nome="Pastor"),
        VinculoResponse(id=4, nome="Presbítero(a)"),
        VinculoResponse(id=5, nome="Diácono/Diaconisa"),
        VinculoResponse(id=1, nome="Membro"),
        VinculoResponse(id=3, nome="Visitante"),
        VinculoResponse(id=7, nome="Líder de célula"),
        VinculoResponse(id=8, nome="Voluntário(a)"),
        VinculoResponse(id=9, nome="Criança"),
        VinculoResponse(id=10, nome="Outro"),
    ]