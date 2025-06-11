from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from app.core.database import get_session
from app.core.logger import get_logger
from app.schemas.schema_motorista import MotoristaCreate, MotoristaRead
from typing import List
from app.crud import crud_motorista

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=MotoristaRead, status_code=201)
def create_new_motorista(motorista: MotoristaCreate, session: Session = Depends(get_session)):
    """
    Cria um novo motorista (e um usuário associado).
    """
    logger.info(f"Criando motorista com email {motorista.email}")
    db_user = crud_motorista.get_usuario_by_email(session, email=motorista.email)
    if db_user:
        logger.warning(f"Email {motorista.email} já cadastrado.")
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    try:
        motorista = crud_motorista.create_motorista(db=session, motorista_in=motorista)
        logger.info(f"Motorista criado com ID {motorista.id}")
        return motorista
    except Exception as e:
        logger.error(f"Erro ao criar motorista: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[MotoristaRead])
def read_motoristas(
    session: Session = Depends(get_session),
    nome: str = None,
    skip: int = 0,
    limit: int = 100
):
    logger.info(f"Listando motoristas com filtro: nome='{nome}'")
    motoristas = crud_motorista.get_motoristas(session, nome=nome, skip=skip, limit=limit)
    return motoristas

@router.get("/quantidade", response_model=dict)
def count_motoristas_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando motoristas")
    quantidade = crud_motorista.count_motoristas(session)
    return {"quantidade": quantidade}
