from pydantic import BaseModel
from typing import Optional
class RotaBase(BaseModel):
    nome_rota: str
    descricao: str
    turno: str
    limite_atrasos_semanal: int
    ativa: Optional[bool] = True
class RotaCreate(RotaBase):
    pass
class RotaRead(RotaBase):
    id: int

    class Config:
        from_attributes = True
