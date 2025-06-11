from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_db
from app.schemas.schema_rota import RotaCreate, RotaRead
from app.crud import crud_rota

router = APIRouter()

@router.post("/rotas/", response_model=RotaRead, status_code=201)
def create_new_rota(rota: RotaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova rota.
    """
    return crud_rota.create_rota(db=db, rota_in=rota)

@router.get("/rotas/", response_model=List[RotaRead])
def read_rotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera uma lista de rotas.
    """
    rotas = crud_rota.get_rotas(db, skip=skip, limit=limit)
    return rotas

@router.get("/rotas/{rota_id}", response_model=RotaRead)
def read_rota(rota_id: int, db: Session = Depends(get_db)):
    """
    Recupera uma rota específica pelo ID.
    """
    db_rota = crud_rota.get_rota_by_id(db, rota_id=rota_id)
    if db_rota is None:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return db_rota
