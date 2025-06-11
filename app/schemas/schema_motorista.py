from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from .schema_aluno import UsuarioRead # Reutiliza o schema de leitura do usuário

# Schema para criação de Motorista (recebe dados do usuário e do motorista)
class MotoristaCreate(BaseModel):
    # Dados do usuário a ser criado
    email: EmailStr
    nome_completo: str
    password: str
    
    # Dados específicos do motorista
    cnh: str
    data_admissao: date

# Schema de Leitura para o Motorista (retorna dados completos)
class MotoristaRead(BaseModel):
    id: int
    cnh: str
    data_admissao: date
    status_ativo: bool
    usuario: UsuarioRead # Aninha os dados do usuário para uma resposta completa

    class Config:
        from_attributes = True
