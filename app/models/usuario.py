from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .aluno import Aluno
    from .motorista import Motorista

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_completo: str
    email: str = Field(unique=True)
    senha_hash: str
    cargo: Optional[str] = None
    nivel_permissao: Optional[str] = None

    aluno: Optional["Aluno"] = Relationship(back_populates="usuario")
    motorista: Optional["Motorista"] = Relationship(back_populates="usuario")
