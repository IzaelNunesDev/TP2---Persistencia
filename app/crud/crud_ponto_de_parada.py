from sqlmodel import Session, select, func
from app.models.ponto_de_parada import PontoDeParada
from app.schemas.schema_ponto_de_parada import PontoDeParadaCreate, PontoDeParadaUpdate

def create_ponto_de_parada(db: Session, ponto_in: PontoDeParadaCreate) -> PontoDeParada:
    ponto_obj = PontoDeParada.model_validate(ponto_in)
    db.add(ponto_obj)
    db.commit()
    db.refresh(ponto_obj)
    return ponto_obj

def get_pontos_de_parada_by_rota(db: Session, rota_id: int, skip: int = 0, limit: int = 100) -> list[PontoDeParada]:
    return db.exec(
        select(PontoDeParada)
        .where(PontoDeParada.rota_id == rota_id)
        .order_by(PontoDeParada.ordem)
        .offset(skip)
        .limit(limit)
    ).all()

def get_ponto_de_parada_by_id(db: Session, ponto_de_parada_id: int) -> PontoDeParada | None:
    return db.get(PontoDeParada, ponto_de_parada_id)

def count_pontos_de_parada(db: Session) -> int:
    return db.exec(select(func.count(PontoDeParada.id))).one()

def update_ponto_de_parada(db: Session, ponto_de_parada: PontoDeParada, ponto_de_parada_update: PontoDeParadaUpdate) -> PontoDeParada:
    ponto_de_parada_data = ponto_de_parada_update.model_dump(exclude_unset=True)
    for key, value in ponto_de_parada_data.items():
        setattr(ponto_de_parada, key, value)
    db.add(ponto_de_parada)
    db.commit()
    db.refresh(ponto_de_parada)
    return ponto_de_parada

def delete_ponto_de_parada(db: Session, ponto_de_parada: PontoDeParada):
    db.delete(ponto_de_parada)
    db.commit()
