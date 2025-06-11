from pydantic import BaseModel
from typing import Optional

# Propriedades base do Veículo
class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    capacidade_passageiros: int
    status_manutencao: str
    adaptado_pcd: Optional[bool] = False
    ano_fabricacao: int

# Schema para criação
class VeiculoCreate(VeiculoBase):
    pass

# Schema para leitura
class VeiculoRead(VeiculoBase):
    id: int

    class Config:
        from_attributes = True
