from sqlmodel import SQLModel
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from .schema_usuario import UsuarioRead 

class MotoristaCreate(BaseModel):
    email: EmailStr
    nome_completo: str
    password: str
    cnh: str
    data_admissao: date

class MotoristaRead(BaseModel):
    id: int
    cnh: str
    data_admissao: date
    status_ativo: bool
    usuario: UsuarioRead

    class Config:
        from_attributes = True

class MotoristaUpdate(SQLModel):
    cnh: Optional[str] = None
    data_admissao: Optional[date] = None
    status_ativo: Optional[bool] = None
