from sqlmodel import Field, SQLModel
from typing import Optional

class Rota(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_rota: str
    descricao: str
    turno: str
    limite_atrasos_semanal: int
    ativa: bool = Field(default=True)
