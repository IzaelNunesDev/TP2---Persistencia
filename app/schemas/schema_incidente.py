from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .schema_aluno import UsuarioRead 

class IncidenteBase(BaseModel):
    descricao: str
    tipo_incidente: str
    status_resolucao: str
    viagem_id: int
    reportado_por_usuario_id: int

class IncidenteCreate(IncidenteBase):
    pass

class IncidenteRead(IncidenteBase):
    id: int
    data_hora_registro: datetime
    reportado_por: UsuarioRead

    class Config:
        from_attributes = True
