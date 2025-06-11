from pydantic import BaseModel
from typing import Optional

# Propriedades base do Ponto de Parada
class PontoDeParadaBase(BaseModel):
    nome_ponto: str
    endereco: str
    latitude: float
    longitude: float
    ordem: int
    rota_id: int

# Schema para criação
class PontoDeParadaCreate(PontoDeParadaBase):
    pass

# Schema para leitura
class PontoDeParadaRead(PontoDeParadaBase):
    id: int

    class Config:
        from_attributes = True
