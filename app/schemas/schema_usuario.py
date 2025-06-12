from pydantic import BaseModel, EmailStr
class UsuarioBase(BaseModel):
    email: EmailStr
    nome_completo: str
class UsuarioRead(UsuarioBase):
    id: int
    class Config:
        from_attributes = True
