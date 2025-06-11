from sqlmodel import Session, select
from app.models.ponto_de_parada import PontoDeParada
from app.schemas.schema_ponto_de_parada import PontoDeParadaCreate

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
        .offset(skip)
        .limit(limit)
    ).all()

def count_pontos_de_parada(db: Session) -> int:
    return db.query(PontoDeParada).count()
