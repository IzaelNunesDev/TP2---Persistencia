from sqlmodel import Field, SQLModel
from typing import Optional

class PontoDeParada(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_ponto: str
    endereco: str
    latitude: float
    longitude: float
    ordem: int
    rota_id: int = Field(foreign_key="rota.id")
