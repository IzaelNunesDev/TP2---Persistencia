from pydantic import BaseModel, EmailStr
from typing import Optional

# Propriedades base do Usuário (reusável)
class UsuarioBase(BaseModel):
    email: EmailStr
    nome_completo: str

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

# Schema de Leitura para o Usuário
class UsuarioRead(UsuarioBase):
    id: int
    class Config:
        from_attributes = True

# Schema de Leitura para o Aluno (pode incluir o usuário)
class AlunoRead(BaseModel):
    id: int
    matricula: str
    usuario: UsuarioRead # Aninhamos o usuário para uma resposta completa

    class Config:
        from_attributes = True
