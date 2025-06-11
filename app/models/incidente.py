from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime

class Incidente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    tipo_incidente: str
    data_hora_registro: datetime
    status_resolucao: str
    viagem_id: int = Field(foreign_key="viagem.id")
    reportado_por_usuario_id: int = Field(foreign_key="usuario.id")

    viagem: Optional["Viagem"] = Relationship(back_populates="incidentes")
    reportado_por: Optional["Usuario"] = Relationship(back_populates="incidentes_reportados")
