from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_db
from app.schemas.schema_veiculo import VeiculoCreate, VeiculoRead
from app.crud import crud_veiculo

router = APIRouter()

@router.post("/veiculos/", response_model=VeiculoRead, status_code=201)
def create_new_veiculo(veiculo: VeiculoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo veículo.
    """
    db_veiculo = crud_veiculo.get_veiculo_by_placa(db, placa=veiculo.placa)
    if db_veiculo:
        raise HTTPException(status_code=400, detail="Placa já cadastrada")
    return crud_veiculo.create_veiculo(db=db, veiculo_in=veiculo)

@router.get("/veiculos/", response_model=List[VeiculoRead])
def read_veiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera uma lista de veículos.
    """
    veiculos = crud_veiculo.get_veiculos(db, skip=skip, limit=limit)
    return veiculos

@router.get("/veiculos/{veiculo_id}", response_model=VeiculoRead)
def read_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """
    Recupera um veículo específico pelo ID.
    """
    db_veiculo = crud_veiculo.get_veiculo_by_id(db, veiculo_id=veiculo_id)
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return db_veiculo
