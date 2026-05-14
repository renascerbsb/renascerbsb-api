from pydantic import BaseModel


class MinisterioResponse(BaseModel):
    seq_ministerio: int
    ds_nome: str
    st_ativo: bool = True