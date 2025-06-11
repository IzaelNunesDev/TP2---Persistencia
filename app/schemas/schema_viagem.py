from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Importa os schemas de leitura das outras entidades para aninhamento
from .schema_rota import RotaRead
from .schema_motorista import MotoristaRead
from .schema_veiculo import VeiculoRead

# Propriedades base da Viagem
class ViagemBase(BaseModel):
    data_viagem: date
    hora_partida: datetime
    status: str
    vagas_ocupadas: int = 0
    rota_id: int
    motorista_id: int
    veiculo_id: int

# Schema para criação
class ViagemCreate(ViagemBase):
    pass

# Schema para leitura (com dados aninhados)
class ViagemRead(ViagemBase):
    id: int
    rota: RotaRead
    motorista: MotoristaRead
    veiculo: VeiculoRead

    class Config:
        from_attributes = True
