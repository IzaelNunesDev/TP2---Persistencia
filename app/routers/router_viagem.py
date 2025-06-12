from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.crud.crud_viagem import create_viagem, get_viagens, count_viagens, get_viagem_by_id, update_viagem, delete_viagem
from app.schemas.schema_viagem import ViagemCreate, ViagemRead, ViagemUpdate
from app.core.logger import get_logger
from app.crud import crud_rota, crud_motorista, crud_veiculo

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=ViagemRead, status_code=201)
def create_new_viagem(viagem: ViagemCreate, session: Session = Depends(get_session)):
    """
    Cria uma nova viagem, associando rota, motorista e veículo.
    """
    logger.info(f"Criando viagem para rota {viagem.rota_id}")
    # Validações de existência
    if not crud_rota.get_rota_by_id(session, viagem.rota_id):
        logger.warning(f"Rota com id {viagem.rota_id} não encontrada")
        raise HTTPException(status_code=404, detail=f"Rota com id {viagem.rota_id} não encontrada")
    if not crud_motorista.get_motorista_by_id(session, viagem.motorista_id):
        logger.warning(f"Motorista com id {viagem.motorista_id} não encontrado")
        raise HTTPException(status_code=404, detail=f"Motorista com id {viagem.motorista_id} não encontrado")
    if not crud_veiculo.get_veiculo_by_id(session, viagem.veiculo_id):
        logger.warning(f"Veículo com id {viagem.veiculo_id} não encontrado")
        raise HTTPException(status_code=404, detail=f"Veículo com id {viagem.veiculo_id} não encontrado")

    try:
        new_viagem = create_viagem(db=session, viagem_in=viagem)
        logger.info(f"Viagem criada com ID {new_viagem.id}")
        # Recarrega o objeto com os relacionamentos para a resposta
        return get_viagem_by_id(session, new_viagem.id)
    except Exception as e:
        logger.error(f"Erro ao criar viagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[ViagemRead])
def read_viagens(session: Session = Depends(get_session), ano: int = None, skip: int = 0, limit: int = 100):
    """
    Recupera uma lista de viagens, opcionalmente filtrada por ano.
    """
    logger.info(f"Listando viagens com filtro: ano='{ano}'")
    viagens = get_viagens(session, ano=ano, skip=skip, limit=limit)
    return viagens

@router.get("/{viagem_id}", response_model=ViagemRead)
def read_viagem(viagem_id: int, session: Session = Depends(get_session)):
    """
    Recupera uma viagem específica pelo ID com todos os detalhes.
    """
    logger.info(f"Buscando viagem com ID {viagem_id}")
    db_viagem = get_viagem_by_id(session, viagem_id=viagem_id)
    if db_viagem is None:
        logger.warning(f"Viagem com ID {viagem_id} não encontrada")
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return db_viagem

@router.get("/quantidade", response_model=dict)
def count_viagens_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando viagens")
    quantidade = count_viagens(session)
    return {"quantidade": quantidade}

@router.put("/{viagem_id}", response_model=ViagemRead)
def update_viagem_route(viagem_id: int, viagem_in: ViagemUpdate, db: Session = Depends(get_session)):
    logger.info(f"Atualizando viagem com ID: {viagem_id}")
    viagem = get_viagem_by_id(db, viagem_id)
    if not viagem:
        logger.error(f"Viagem com ID {viagem_id} não encontrada")
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    viagem = update_viagem(db, viagem, viagem_in)
    logger.info(f"Viagem com ID {viagem_id} atualizada com sucesso")
    return viagem


@router.delete("/{viagem_id}", status_code=204)
def delete_viagem_route(viagem_id: int, db: Session = Depends(get_session)):
    logger.info(f"Deletando viagem com ID: {viagem_id}")
    viagem = get_viagem_by_id(db, viagem_id)
    if not viagem:
        logger.error(f"Viagem com ID {viagem_id} não encontrada")
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    delete_viagem(db, viagem)
    logger.info(f"Viagem com ID {viagem_id} deletado com sucesso")
    return
