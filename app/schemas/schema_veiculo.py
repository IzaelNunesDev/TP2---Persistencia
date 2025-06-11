from typing import Optional
from sqlmodel import SQLModel

# Propriedades base do Veículo
class VeiculoBase(SQLModel):
    placa: str
    modelo: str
    cor: Optional[str] = None
    ano_fabricacao: int
    capacidade_passageiros: int
    status_manutencao: str
    adaptado_pcd: bool = False

# Schema para criação
class VeiculoCreate(VeiculoBase):
    pass

# Schema para leitura
class VeiculoRead(VeiculoBase):
    id: int

    class Config:
        from_attributes = True


class VeiculoUpdate(SQLModel):
    placa: Optional[str] = None
    modelo: Optional[str] = None
    cor: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    capacidade_passageiros: Optional[int] = None
    status_manutencao: Optional[str] = None
    adaptado_pcd: Optional[bool] = None
