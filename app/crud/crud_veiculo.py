from sqlmodel import Session, select, func
from app.models.veiculo import Veiculo
from app.schemas.schema_veiculo import VeiculoCreate, VeiculoUpdate

def create_veiculo(db: Session, veiculo_in: VeiculoCreate) -> Veiculo:
    veiculo_obj = Veiculo.model_validate(veiculo_in)
    db.add(veiculo_obj)
    db.commit()
    db.refresh(veiculo_obj)
    return veiculo_obj

def get_veiculos(db: Session, placa: str = None, skip: int = 0, limit: int = 100) -> list[Veiculo]:
    query = select(Veiculo)
    if placa:
        query = query.where(Veiculo.placa.ilike(f"%{placa}%"))
    return db.exec(query.offset(skip).limit(limit)).all()

def get_veiculo_by_id(db: Session, veiculo_id: int) -> Veiculo | None:
    return db.get(Veiculo, veiculo_id)

def get_veiculo_by_placa(db: Session, placa: str) -> Veiculo | None:
    return db.exec(select(Veiculo).where(Veiculo.placa == placa)).first()

def count_veiculos(db: Session) -> int:
    return db.exec(select(func.count(Veiculo.id))).one()

def update_veiculo(db: Session, veiculo: Veiculo, veiculo_update: VeiculoUpdate) -> Veiculo:
    veiculo_data = veiculo_update.model_dump(exclude_unset=True)
    for key, value in veiculo_data.items():
        setattr(veiculo, key, value)
    db.add(veiculo)
    db.commit()
    db.refresh(veiculo)
    return veiculo

def delete_veiculo(db: Session, veiculo: Veiculo):
    db.delete(veiculo)
    db.commit()
