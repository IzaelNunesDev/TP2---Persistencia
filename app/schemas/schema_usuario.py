from pydantic import BaseModel, EmailStr

# Propriedades base do Usuário (reusável)
class UsuarioBase(BaseModel):
    email: EmailStr
    nome_completo: str

# Schema de Leitura para o Usuário
class UsuarioRead(UsuarioBase):
    id: int
    class Config:
        from_attributes = True
