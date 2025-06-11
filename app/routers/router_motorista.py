from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from app.core.database import get_session
from app.crud.crud_motorista import create_motorista, get_motoristas, count_motoristas, get_motorista_by_id, update_motorista, delete_motorista
from app.crud.crud_usuario import get_usuario_by_email
from app.schemas.schema_motorista import MotoristaCreate, MotoristaRead, MotoristaUpdate
from typing import List
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=MotoristaRead, status_code=201)
def create_motorista_endpoint(
    *,
    db: Session = Depends(get_session),
    motorista_in: MotoristaCreate
):
    """
    Cria um novo motorista (e um usuário associado).
    """
    logger.info(f"Criando motorista com email {motorista_in.email}")
    db_user = get_usuario_by_email(db, email=motorista_in.email)
    if db_user:
        logger.warning(f"Email {motorista_in.email} já cadastrado.")
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    try:
        motorista = create_motorista(db=db, motorista_in=motorista_in)
        logger.info(f"Motorista criado com ID {motorista.id}")
        return motorista
    except Exception as e:
        logger.error(f"Erro ao criar motorista: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[MotoristaRead])
def read_motoristas(
    *,
    db: Session = Depends(get_session),
    nome: str = None,
    skip: int = 0,
    limit: int = 100
):
    logger.info(f"Listando motoristas com filtro: nome='{nome}'")
    motoristas = get_motoristas(db, nome=nome, skip=skip, limit=limit)
    return motoristas

@router.get("/quantidade", response_model=dict)
def count_motoristas_endpoint(
    *,
    db: Session = Depends(get_session)
):
    logger.info("Contando motoristas")
    quantidade = count_motoristas(db)
    return {"quantidade": quantidade}

@router.put("/{motorista_id}", response_model=MotoristaRead)
def update_motorista_route(
    *,
    motorista_id: int,
    motorista_in: MotoristaUpdate,
    db: Session = Depends(get_session)
):
    logger.info(f"Atualizando motorista com ID: {motorista_id}")
    motorista = get_motorista_by_id(db, motorista_id)
    if not motorista:
        logger.error(f"Motorista com ID {motorista_id} não encontrado")
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    motorista = update_motorista(db, motorista, motorista_in)
    logger.info(f"Motorista com ID {motorista_id} atualizado com sucesso")
    return motorista


@router.delete("/{motorista_id}", status_code=204)
def delete_motorista_route(motorista_id: int, db: Session = Depends(get_session)):
    logger.info(f"Deletando motorista com ID: {motorista_id}")
    motorista = get_motorista_by_id(db, motorista_id)
    if not motorista:
        logger.error(f"Motorista com ID {motorista_id} não encontrado")
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    delete_motorista(db, motorista)
    logger.info(f"Motorista com ID {motorista_id} deletado com sucesso")
    return
