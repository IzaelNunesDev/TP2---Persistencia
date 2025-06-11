from sqlmodel import Session, select
from app.models.rota import Rota
from app.schemas.schema_rota import RotaCreate

def create_rota(db: Session, rota_in: RotaCreate) -> Rota:
    rota_obj = Rota.model_validate(rota_in)
    db.add(rota_obj)
    db.commit()
    db.refresh(rota_obj)
    return rota_obj

def get_rotas(db: Session, skip: int = 0, limit: int = 100) -> list[Rota]:
    return db.exec(select(Rota).offset(skip).limit(limit)).all()

def get_rota_by_id(db: Session, rota_id: int) -> Rota | None:
    return db.get(Rota, rota_id)
