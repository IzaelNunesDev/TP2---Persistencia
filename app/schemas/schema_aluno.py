from sqlmodel import SQLModel
from pydantic import BaseModel, EmailStr
from typing import Optional
from .schema_usuario import UsuarioRead

class AlunoCreate(BaseModel):

    email: EmailStr
    nome_completo: str
    password: str 
    matricula: str
    telefone: Optional[str] = None
    possui_necessidade_especial: Optional[bool] = False
    documento_identidade: Optional[str] = None

class AlunoRead(BaseModel):
    id: int
    matricula: str
    usuario: UsuarioRead 

    class Config:
        from_attributes = True

class AlunoUpdate(SQLModel):
    matricula: Optional[str] = None
    telefone: Optional[str] = None
    possui_necessidade_especial: Optional[bool] = None
    documento_identidade: Optional[str] = None
    ponto_embarque_preferencial_id: Optional[int] = None
