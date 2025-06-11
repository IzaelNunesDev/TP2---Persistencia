from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .rota import Rota
    from .aluno import Aluno

class PontoDeParada(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_ponto: str
    endereco: str
    latitude: float
    longitude: float
    ordem: int
    rota_id: int = Field(foreign_key="rota.id")

    rota: Optional["Rota"] = Relationship(back_populates="pontos_de_parada")
    alunos_preferenciais: List["Aluno"] = Relationship(back_populates="ponto_embarque_preferencial")
