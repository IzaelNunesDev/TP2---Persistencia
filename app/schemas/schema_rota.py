from pydantic import BaseModel
from typing import Optional

# Propriedades base da Rota
class RotaBase(BaseModel):
    nome_rota: str
    descricao: str
    turno: str
    limite_atrasos_semanal: int
    ativa: Optional[bool] = True

# Schema para criação de Rota
class RotaCreate(RotaBase):
    pass

# Schema para leitura de Rota
class RotaRead(RotaBase):
    id: int

    class Config:
        from_attributes = True
