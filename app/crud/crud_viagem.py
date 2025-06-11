from sqlmodel import Session, select, func
from sqlalchemy import extract
from app.models.viagem import Viagem
from app.schemas.schema_viagem import ViagemCreate, ViagemUpdate

def create_viagem(db: Session, viagem_in: ViagemCreate) -> Viagem:
    viagem_obj = Viagem.model_validate(viagem_in)
    db.add(viagem_obj)
    db.commit()
    db.refresh(viagem_obj)
    return viagem_obj

def get_viagens(db: Session, ano: int = None, skip: int = 0, limit: int = 100) -> list[Viagem]:
    query = select(Viagem)
    if ano:
        query = query.where(extract('year', Viagem.data_viagem) == ano)
    return db.exec(query.offset(skip).limit(limit)).all()

def get_viagem_by_id(db: Session, viagem_id: int) -> Viagem | None:
    # Usando select para poder carregar os relacionamentos com options
    # Isso é mais eficiente do que o lazy loading padrão em muitos casos.
    from app.models.rota import Rota
    from app.models.motorista import Motorista
    from app.models.veiculo import Veiculo
    from sqlmodel import select
    from sqlalchemy.orm import selectinload

    result = db.exec(
        select(Viagem).options(
            selectinload(Viagem.rota),
            selectinload(Viagem.motorista),
            selectinload(Viagem.veiculo)
        ).where(Viagem.id == viagem_id)
    ).first()
    return result

def count_viagens(db: Session) -> int:
    return db.exec(select(func.count(Viagem.id))).one()

def update_viagem(db: Session, viagem: Viagem, viagem_update: ViagemUpdate) -> Viagem:
    viagem_data = viagem_update.model_dump(exclude_unset=True)
    for key, value in viagem_data.items():
        setattr(viagem, key, value)
    db.add(viagem)
    db.commit()
    db.refresh(viagem)
    return viagem

def delete_viagem(db: Session, viagem: Viagem):
    db.delete(viagem)
    db.commit()
