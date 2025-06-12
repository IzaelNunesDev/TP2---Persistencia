from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .schema_aluno import AlunoRead
class RegistroFrequenciaBase(BaseModel):
    viagem_id: int
    aluno_id: int
    tipo_registro: str
class RegistroFrequenciaCreate(RegistroFrequenciaBase):
    pass
class RegistroFrequenciaRead(RegistroFrequenciaBase):
    id: int
    data_hora_embarque: datetime
    aluno: AlunoRead

    class Config:
        from_attributes = True
