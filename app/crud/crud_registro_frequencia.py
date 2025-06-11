from sqlmodel import Session, select
from app.models.registro_frequencia import RegistroFrequencia
from app.schemas.schema_registro_frequencia import RegistroFrequenciaCreate
from datetime import datetime

def create_registro_frequencia(db: Session, registro_in: RegistroFrequenciaCreate) -> RegistroFrequencia:
    registro_obj = RegistroFrequencia(
        **registro_in.model_dump(),
        data_hora_embarque=datetime.now()
    )
    db.add(registro_obj)
    db.commit()
    db.refresh(registro_obj)
    return registro_obj

def get_registros_by_viagem(db: Session, viagem_id: int, skip: int = 0, limit: int = 100) -> list[RegistroFrequencia]:
    return db.exec(
        select(RegistroFrequencia)
        .where(RegistroFrequencia.viagem_id == viagem_id)
        .offset(skip)
        .limit(limit)
    ).all()

def count_registros_frequencia(db: Session) -> int:
    return db.query(RegistroFrequencia).count()
