from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from typing import Optional, List
from .usuario import Usuario

class Motorista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cnh: str = Field(unique=True)
    data_admissao: date
    status_ativo: bool = Field(default=True)

    usuario_id: int = Field(foreign_key="usuario.id", unique=True)
    usuario: Usuario = Relationship(back_populates="motorista")

    viagens: List["Viagem"] = Relationship(back_populates="motorista")
