from sqlmodel import Field, SQLModel
from typing import Optional
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
