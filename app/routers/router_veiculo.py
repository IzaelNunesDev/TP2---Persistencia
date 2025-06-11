from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.crud.crud_veiculo import create_veiculo, get_veiculos, count_veiculos, get_veiculo_by_id, update_veiculo, delete_veiculo, get_veiculo_by_placa
from app.schemas.schema_veiculo import VeiculoCreate, VeiculoRead, VeiculoUpdate
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=VeiculoRead, status_code=201)
def create_new_veiculo(veiculo: VeiculoCreate, session: Session = Depends(get_session)):
    """
    Cria um novo veículo.
    """
    logger.info(f"Criando veículo com placa {veiculo.placa}")
    db_veiculo = get_veiculo_by_placa(session, placa=veiculo.placa)
    if db_veiculo:
        logger.warning(f"Veículo com placa {veiculo.placa} já cadastrado.")
        raise HTTPException(status_code=400, detail="Veículo com esta placa já cadastrado")
    try:
        new_veiculo = create_veiculo(db=session, veiculo_in=veiculo)
        logger.info(f"Veículo criado com ID {new_veiculo.id}")
        return new_veiculo
    except Exception as e:
        logger.error(f"Erro ao criar veículo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[VeiculoRead])
def read_veiculos(session: Session = Depends(get_session), placa: str = None, skip: int = 0, limit: int = 100):
    """
    Recupera uma lista de veículos.
    """
    logger.info(f"Listando veículos com filtro: placa='{placa}'")
    veiculos = get_veiculos(session, placa=placa, skip=skip, limit=limit)
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
    quantidade = count_veiculos(session)
    return {"quantidade": quantidade}

@router.put("/{veiculo_id}", response_model=VeiculoRead)
def update_veiculo_route(veiculo_id: int, veiculo_in: VeiculoUpdate, db: Session = Depends(get_session)):
    logger.info(f"Atualizando veiculo com ID: {veiculo_id}")
    veiculo = get_veiculo_by_id(db, veiculo_id)
    if not veiculo:
        logger.error(f"Veiculo com ID {veiculo_id} não encontrado")
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")
    veiculo = update_veiculo(db, veiculo, veiculo_in)
    logger.info(f"Veiculo com ID {veiculo_id} atualizado com sucesso")
    return veiculo


@router.delete("/{veiculo_id}", status_code=204)
def delete_veiculo_route(veiculo_id: int, db: Session = Depends(get_session)):
    logger.info(f"Deletando veiculo com ID: {veiculo_id}")
    veiculo = get_veiculo_by_id(db, veiculo_id)
    if not veiculo:
        logger.error(f"Veiculo com ID {veiculo_id} não encontrado")
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")
    delete_veiculo(db, veiculo)
    logger.info(f"Veiculo com ID {veiculo_id} deletado com sucesso")
    return
