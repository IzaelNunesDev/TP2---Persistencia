from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date, datetime

class Viagem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_viagem: date
    hora_partida: datetime
    status: str
    vagas_ocupadas: int
    rota_id: int = Field(foreign_key="rota.id")
    motorista_id: int = Field(foreign_key="motorista.id")
    veiculo_id: int = Field(foreign_key="veiculo.id")

    rota: Optional["Rota"] = Relationship(back_populates="viagens")
    motorista: Optional["Motorista"] = Relationship(back_populates="viagens")
    veiculo: Optional["Veiculo"] = Relationship(back_populates="viagens")

    registros_frequencia: List["RegistroFrequencia"] = Relationship(back_populates="viagem")
    incidentes: List["Incidente"] = Relationship(back_populates="viagem")
