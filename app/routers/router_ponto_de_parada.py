from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.logger import get_logger
from app.crud.crud_ponto_de_parada import create_ponto_de_parada, get_pontos_de_parada_by_rota, count_pontos_de_parada, get_ponto_de_parada_by_id, update_ponto_de_parada, delete_ponto_de_parada
from app.crud.crud_rota import get_rota_by_id
from app.schemas.schema_ponto_de_parada import PontoDeParadaCreate, PontoDeParadaRead, PontoDeParadaUpdate

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=PontoDeParadaRead, status_code=201)
def create_new_ponto_de_parada(ponto: PontoDeParadaCreate, session: Session = Depends(get_session)):
    logger.info(f"Criando ponto de parada para rota {ponto.rota_id}")
    # Verifica se a rota existe
    db_rota = get_rota_by_id(session, rota_id=ponto.rota_id)
    if db_rota is None:
        logger.warning(f"Rota com id {ponto.rota_id} não encontrada ao criar ponto de parada")
        raise HTTPException(status_code=404, detail=f"Rota com id {ponto.rota_id} não encontrada")
    try:
        novo_ponto = create_ponto_de_parada(db=session, ponto_in=ponto)
        logger.info(f"Ponto de parada criado com ID {novo_ponto.id}")
        return novo_ponto
    except Exception as e:
        logger.error(f"Erro ao criar ponto de parada: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/por-rota/{rota_id}", response_model=List[PontoDeParadaRead])
def read_pontos_de_parada_from_rota(rota_id: int, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    logger.info(f"Listando pontos de parada para rota {rota_id}")
    # Verifica se a rota existe
    db_rota = get_rota_by_id(session, rota_id=rota_id)
    if db_rota is None:
        logger.warning(f"Rota com id {rota_id} não encontrada ao listar pontos de parada")
        raise HTTPException(status_code=404, detail=f"Rota com id {rota_id} não encontrada")

    pontos = get_pontos_de_parada_by_rota(session, rota_id=rota_id, skip=skip, limit=limit)
    return pontos

@router.get("/quantidade", response_model=dict)
def count_pontos_de_parada_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando pontos de parada")
    quantidade = count_pontos_de_parada(session)
    return {"quantidade": quantidade}

@router.put("/{ponto_de_parada_id}", response_model=PontoDeParadaRead)
def update_ponto_de_parada_route(ponto_de_parada_id: int, ponto_de_parada_in: PontoDeParadaUpdate, db: Session = Depends(get_session)):
    logger.info(f"Atualizando ponto de parada com ID: {ponto_de_parada_id}")
    ponto_de_parada = get_ponto_de_parada_by_id(db, ponto_de_parada_id)
    if not ponto_de_parada:
        logger.error(f"Ponto de parada com ID {ponto_de_parada_id} não encontrado")
        raise HTTPException(status_code=404, detail="Ponto de parada não encontrado")
    ponto_de_parada = update_ponto_de_parada(db, ponto_de_parada, ponto_de_parada_in)
    logger.info(f"Ponto de parada com ID {ponto_de_parada_id} atualizado com sucesso")
    return ponto_de_parada


@router.delete("/{ponto_de_parada_id}", status_code=204)
def delete_ponto_de_parada_route(ponto_de_parada_id: int, db: Session = Depends(get_session)):
    logger.info(f"Deletando ponto de parada com ID: {ponto_de_parada_id}")
    ponto_de_parada = get_ponto_de_parada_by_id(db, ponto_de_parada_id)
    if not ponto_de_parada:
        logger.error(f"Ponto de parada com ID {ponto_de_parada_id} não encontrado")
        raise HTTPException(status_code=404, detail="Ponto de parada não encontrado")
    delete_ponto_de_parada(db, ponto_de_parada)
    logger.info(f"Ponto de parada com ID {ponto_de_parada_id} deletado com sucesso")
    return
