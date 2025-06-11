from sqlmodel import Session, select, func
from app.models.rota import Rota
from app.schemas.schema_rota import RotaCreate

def create_rota(db: Session, rota_in: RotaCreate) -> Rota:
    rota_obj = Rota.model_validate(rota_in)
    db.add(rota_obj)
    db.commit()
    db.refresh(rota_obj)
    return rota_obj

def get_rotas(db: Session, descricao: str = None, skip: int = 0, limit: int = 100) -> list[Rota]:
    query = select(Rota)
    if descricao:
        query = query.where(Rota.descricao.ilike(f"%{descricao}%"))
    return db.exec(query.offset(skip).limit(limit)).all()

def get_rota_by_id(db: Session, rota_id: int) -> Rota | None:
    return db.get(Rota, rota_id)

def count_rotas(db: Session) -> int:
    return db.exec(select(func.count(Rota.id))).one()
