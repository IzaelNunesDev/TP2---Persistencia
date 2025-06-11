from pydantic import BaseModel, EmailStr
from typing import Optional

# Propriedades compartilhadas
class AlunoBase(BaseModel):
    email: EmailStr
    nome_completo: str
    matricula: str
    telefone: Optional[str] = None
    possui_necessidade_especial: Optional[bool] = False
    documento_identidade: Optional[str] = None

# Schema para criação (recebido pela API)
class AlunoCreate(AlunoBase):
    pass

# Schema para atualização (recebido pela API)
class AlunoUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    
# Schema para leitura (enviado pela API)
class AlunoRead(AlunoBase):
    id: int

    class Config:
        from_attributes = True
