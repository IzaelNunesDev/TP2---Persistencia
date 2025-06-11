from sqlmodel import Session, select
from app.models.incidente import Incidente
from app.schemas.schema_incidente import IncidenteCreate
from datetime import datetime

def create_incidente(db: Session, incidente_in: IncidenteCreate) -> Incidente:
    # Cria o objeto do modelo, adicionando a data e hora do registro
    incidente_obj = Incidente(
        **incidente_in.model_dump(),
        data_hora_registro=datetime.now()
    )
    db.add(incidente_obj)
    db.commit()
    db.refresh(incidente_obj)
    return incidente_obj

def get_incidentes_by_viagem(db: Session, viagem_id: int, skip: int = 0, limit: int = 100) -> list[Incidente]:
    return db.exec(
        select(Incidente)
        .where(Incidente.viagem_id == viagem_id)
        .offset(skip)
        .limit(limit)
    ).all()
