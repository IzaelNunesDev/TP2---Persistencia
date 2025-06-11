from sqlmodel import Session, select
from app.models.usuario import Usuario

def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    """Busca um usuário pelo seu endereço de e-mail."""
    return db.exec(select(Usuario).where(Usuario.email == email)).first()

def get_usuario_by_id(db: Session, user_id: int) -> Usuario | None:
    """Busca um usuário pelo seu ID."""
    return db.get(Usuario, user_id)
