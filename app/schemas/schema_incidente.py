from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .schema_aluno import UsuarioRead # Reutilizar para o 'reportado_por'

# Propriedades base do Incidente
class IncidenteBase(BaseModel):
    descricao: str
    tipo_incidente: str
    status_resolucao: str
    viagem_id: int
    reportado_por_usuario_id: int

# Schema para criação (a data e hora serão geradas no servidor)
class IncidenteCreate(IncidenteBase):
    pass

# Schema para leitura
class IncidenteRead(IncidenteBase):
    id: int
    data_hora_registro: datetime
    reportado_por: UsuarioRead

    class Config:
        from_attributes = True
