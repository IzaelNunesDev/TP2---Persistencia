from sqlmodel import Session, select
from app.models.veiculo import Veiculo
from app.schemas.schema_veiculo import VeiculoCreate

def create_veiculo(db: Session, veiculo_in: VeiculoCreate) -> Veiculo:
    veiculo_obj = Veiculo.model_validate(veiculo_in)
    db.add(veiculo_obj)
    db.commit()
    db.refresh(veiculo_obj)
    return veiculo_obj

def get_veiculos(db: Session, skip: int = 0, limit: int = 100) -> list[Veiculo]:
    return db.exec(select(Veiculo).offset(skip).limit(limit)).all()

def get_veiculo_by_id(db: Session, veiculo_id: int) -> Veiculo | None:
    return db.get(Veiculo, veiculo_id)

def get_veiculo_by_placa(db: Session, placa: str) -> Veiculo | None:
    return db.exec(select(Veiculo).where(Veiculo.placa == placa)).first()
