from sqlmodel import SQLModel
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from .schema_rota import RotaRead
from .schema_motorista import MotoristaRead
from .schema_veiculo import VeiculoRead
class ViagemBase(BaseModel):
    data_viagem: date
    hora_partida: datetime
    status: str
    vagas_ocupadas: int = 0
    rota_id: int
    motorista_id: int
    veiculo_id: int
class ViagemCreate(ViagemBase):
    pass
class ViagemRead(ViagemBase):
    id: int
    rota: RotaRead
    motorista: MotoristaRead
    veiculo: VeiculoRead
class ViagemUpdate(SQLModel):
    data_viagem: Optional[date] = None
    hora_partida: Optional[datetime] = None
    status: Optional[str] = None
    vagas_ocupadas: Optional[int] = None
    rota_id: Optional[int] = None
    motorista_id: Optional[int] = None
    veiculo_id: Optional[int] = None

    class Config:
        from_attributes = True
