from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from .usuario import Usuario
from .ponto_de_parada import PontoDeParada

class Aluno(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    matricula: str = Field(unique=True)
    telefone: Optional[str] = None
    possui_necessidade_especial: bool = Field(default=False)
    documento_identidade: Optional[str] = None

    usuario_id: int = Field(foreign_key="usuario.id", unique=True)
    usuario: Usuario = Relationship(back_populates="aluno")

    ponto_embarque_preferencial_id: Optional[int] = Field(default=None, foreign_key="pontodeparada.id")
    ponto_embarque_preferencial: Optional[PontoDeParada] = Relationship()
