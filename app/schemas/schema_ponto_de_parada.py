from sqlmodel import SQLModel
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


class PontoDeParadaUpdate(SQLModel):
    nome_ponto: Optional[str] = None
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ordem: Optional[int] = None
    rota_id: Optional[int] = None
