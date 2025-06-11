from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_db
from app.schemas.schema_ponto_de_parada import PontoDeParadaCreate, PontoDeParadaRead
from app.crud import crud_ponto_de_parada, crud_rota

router = APIRouter()

@router.post("/pontos_parada/", response_model=PontoDeParadaRead, status_code=201)
def create_new_ponto_de_parada(ponto: PontoDeParadaCreate, db: Session = Depends(get_db)):
    """
    Cria um novo ponto de parada para uma rota existente.
    """
    # Verifica se a rota existe
    db_rota = crud_rota.get_rota_by_id(db, rota_id=ponto.rota_id)
    if db_rota is None:
        raise HTTPException(status_code=404, detail=f"Rota com id {ponto.rota_id} não encontrada")
    
    return crud_ponto_de_parada.create_ponto_de_parada(db=db, ponto_in=ponto)

@router.get("/rotas/{rota_id}/pontos_parada/", response_model=List[PontoDeParadaRead])
def read_pontos_de_parada_from_rota(rota_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera os pontos de parada de uma rota específica.
    """
    # Verifica se a rota existe
    db_rota = crud_rota.get_rota_by_id(db, rota_id=rota_id)
    if db_rota is None:
        raise HTTPException(status_code=404, detail=f"Rota com id {rota_id} não encontrada")

    pontos = crud_ponto_de_parada.get_pontos_de_parada_by_rota(db, rota_id=rota_id, skip=skip, limit=limit)
    return pontos
