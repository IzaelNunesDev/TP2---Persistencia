from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    placa: str = Field(unique=True)
    modelo: str
    capacidade_passageiros: int
    status_manutencao: str
    adaptado_pcd: bool = Field(default=False)
    ano_fabricacao: int

    viagens: List["Viagem"] = Relationship(back_populates="veiculo")
