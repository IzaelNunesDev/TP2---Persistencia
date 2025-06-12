from sqlmodel import Session, select, func
from app.models.motorista import Motorista
from app.models.usuario import Usuario
from app.schemas.schema_motorista import MotoristaCreate, MotoristaUpdate
from app.core.security import get_password_hash
from app.crud.crud_usuario import get_usuario_by_email

def create_motorista(db: Session, motorista_in: MotoristaCreate) -> Motorista:
    hashed_password = get_password_hash(motorista_in.password)
    usuario_obj = Usuario(
        email=motorista_in.email,
        nome_completo=motorista_in.nome_completo,
        senha_hash=hashed_password,
        cargo="motorista"
    )
    
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

def get_motoristas(db: Session, nome: str = None, skip: int = 0, limit: int = 100) -> list[Motorista]:
    query = select(Motorista)
    if nome:
        query = query.join(Usuario).where(Usuario.nome_completo.ilike(f"%{nome}%"))
    return db.exec(query.offset(skip).limit(limit)).all()

def count_motoristas(db: Session) -> int:
    return db.exec(select(func.count(Motorista.id))).one()

def update_motorista(db: Session, motorista: Motorista, motorista_update: MotoristaUpdate) -> Motorista:
    motorista_data = motorista_update.model_dump(exclude_unset=True)
    for key, value in motorista_data.items():
        setattr(motorista, key, value)
    db.add(motorista)
    db.commit()
    db.refresh(motorista)
    return motorista

def delete_motorista(db: Session, motorista: Motorista):
    db.delete(motorista)
    db.commit()

