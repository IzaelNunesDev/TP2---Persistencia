from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_db
from app.schemas.schema_viagem import ViagemCreate, ViagemRead
from app.crud import crud_viagem, crud_rota, crud_motorista, crud_veiculo

router = APIRouter()

@router.post("/viagens/", response_model=ViagemRead, status_code=201)
def create_new_viagem(viagem: ViagemCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova viagem, associando rota, motorista e veículo.
    """
    # Validações de existência
    if not crud_rota.get_rota_by_id(db, viagem.rota_id):
        raise HTTPException(status_code=404, detail=f"Rota com id {viagem.rota_id} não encontrada")
    # Precisamos de uma função para buscar motorista por ID no crud_motorista
    if not crud_motorista.get_motorista_by_id(db, viagem.motorista_id):
        raise HTTPException(status_code=404, detail=f"Motorista com id {viagem.motorista_id} não encontrado")
    if not crud_veiculo.get_veiculo_by_id(db, viagem.veiculo_id):
        raise HTTPException(status_code=404, detail=f"Veículo com id {viagem.veiculo_id} não encontrado")

    new_viagem = crud_viagem.create_viagem(db=db, viagem_in=viagem)
    # Recarrega o objeto com os relacionamentos para a resposta
    return crud_viagem.get_viagem_by_id(db, new_viagem.id)

@router.get("/viagens/", response_model=List[ViagemRead])
def read_viagens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera uma lista de viagens.
    """
    # Esta função precisaria ser otimizada no CRUD para carregar relacionamentos
    viagens = crud_viagem.get_viagens(db, skip=skip, limit=limit)
    return viagens

@router.get("/viagens/{viagem_id}", response_model=ViagemRead)
def read_viagem(viagem_id: int, db: Session = Depends(get_db)):
    """
    Recupera uma viagem específica pelo ID com todos os detalhes.
    """
    db_viagem = crud_viagem.get_viagem_by_id(db, viagem_id=viagem_id)
    if db_viagem is None:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return db_viagem
