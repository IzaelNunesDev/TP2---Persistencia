from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    placa: str = Field(unique=True, index=True)
    modelo: str
    cor: Optional[str] = Field(default=None)
    ano_fabricacao: int
    capacidade_passageiros: int
    status_manutencao: str
    adaptado_pcd: bool = Field(default=False)

    viagens: List["Viagem"] = Relationship(back_populates="veiculo")
