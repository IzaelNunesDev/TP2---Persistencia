from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime

class RegistroFrequencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    viagem_id: int = Field(foreign_key="viagem.id")
    aluno_id: int = Field(foreign_key="aluno.id")
    data_hora_embarque: datetime
    tipo_registro: str

    aluno: Optional["Aluno"] = Relationship(back_populates="registros_frequencia")
    viagem: Optional["Viagem"] = Relationship(back_populates="registros_frequencia")
