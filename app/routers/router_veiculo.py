from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.logger import get_logger
from app.schemas.schema_veiculo import VeiculoCreate, VeiculoRead
from app.crud import crud_veiculo

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=VeiculoRead, status_code=201)
def create_new_veiculo(veiculo: VeiculoCreate, session: Session = Depends(get_session)):
    """
    Cria um novo veículo.
    """
    logger.info(f"Criando veículo com placa {veiculo.placa}")
    db_veiculo = crud_veiculo.get_veiculo_by_placa(session, placa=veiculo.placa)
    if db_veiculo:
        logger.warning(f"Veículo com placa {veiculo.placa} já cadastrado.")
        raise HTTPException(status_code=400, detail="Veículo com esta placa já cadastrado")
    try:
        new_veiculo = crud_veiculo.create_veiculo(db=session, veiculo_in=veiculo)
        logger.info(f"Veículo criado com ID {new_veiculo.id}")
        return new_veiculo
    except Exception as e:
        logger.error(f"Erro ao criar veículo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[VeiculoRead])
def read_veiculos(placa: str = None, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Recupera uma lista de veículos.
    """
    logger.info(f"Listando veículos com filtro: placa='{placa}'")
    veiculos = crud_veiculo.get_veiculos(session, placa=placa, skip=skip, limit=limit)
    return veiculos

@router.get("/{veiculo_id}", response_model=VeiculoRead)
def read_veiculo(veiculo_id: int, session: Session = Depends(get_session)):
    """
    Recupera um veículo específico pelo ID.
    """
    logger.info(f"Buscando veículo com ID {veiculo_id}")
    db_veiculo = crud_veiculo.get_veiculo_by_id(session, veiculo_id=veiculo_id)
    if db_veiculo is None:
        logger.warning(f"Veículo com ID {veiculo_id} não encontrado")
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return db_veiculo

@router.get("/quantidade", response_model=dict)
def count_veiculos_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando veículos")
    quantidade = crud_veiculo.count_veiculos(session)
    return {"quantidade": quantidade}
