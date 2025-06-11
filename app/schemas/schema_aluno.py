from pydantic import BaseModel, EmailStr
from typing import Optional
from .schema_usuario import UsuarioRead

# Schema para criação de Aluno (recebe tudo que precisa)
class AlunoCreate(BaseModel):
    # Dados do usuário
    email: EmailStr
    nome_completo: str
    password: str # Adicionamos o campo de senha
    
    # Dados específicos do aluno
    matricula: str
    telefone: Optional[str] = None
    possui_necessidade_especial: Optional[bool] = False
    documento_identidade: Optional[str] = None

# Schema de Leitura para o Aluno (pode incluir o usuário)
class AlunoRead(BaseModel):
    id: int
    matricula: str
    usuario: UsuarioRead # Aninhamos o usuário para uma resposta completa

    class Config:
        from_attributes = True

class AlunoUpdate(SQLModel):
    matricula: Optional[str] = None
    telefone: Optional[str] = None
    possui_necessidade_especial: Optional[bool] = None
    documento_identidade: Optional[str] = None
    ponto_embarque_preferencial_id: Optional[int] = None
