from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Rota(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_rota: str
    descricao: str
    turno: str
    limite_atrasos_semanal: int
    ativa: bool = Field(default=True)

    pontos_de_parada: List["PontoDeParada"] = Relationship(back_populates="rota")
    viagens: List["Viagem"] = Relationship(back_populates="rota")
