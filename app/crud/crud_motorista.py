from sqlmodel import Session, select
from app.models.motorista import Motorista
from app.models.usuario import Usuario
from app.schemas.schema_motorista import MotoristaCreate
from app.core.security import get_password_hash
from app.crud.crud_usuario import get_usuario_by_email

def create_motorista(db: Session, motorista_in: MotoristaCreate) -> Motorista:
    # Cria o hash da senha
    hashed_password = get_password_hash(motorista_in.password)
    
    # Cria o objeto Usuario
    usuario_obj = Usuario(
        email=motorista_in.email,
        nome_completo=motorista_in.nome_completo,
        senha_hash=hashed_password,
        cargo="motorista"
    )
    
    # Cria o objeto Motorista e o vincula ao usuário
    motorista_obj = Motorista(
        cnh=motorista_in.cnh,
        data_admissao=motorista_in.data_admissao,
        usuario=usuario_obj
    )

    db.add(motorista_obj)
    db.commit()
    db.refresh(motorista_obj)
    
    return motorista_obj

def get_motorista_by_id(db: Session, motorista_id: int) -> Motorista | None:
    return db.get(Motorista, motorista_id)

