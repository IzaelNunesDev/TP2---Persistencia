from fastapi import APIRouter, Depends
import logging
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.logger import get_logger
from app.crud import crud_usuario
from app.schemas import schema_usuario

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=List[schema_usuario.UsuarioRead])
def read_usuarios_endpoint(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    logger.info("Listando usuários")
    usuarios = crud_usuario.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/quantidade", response_model=dict)
def count_usuarios_endpoint(db: Session = Depends(get_session)):
    logger.info("Contando usuários")
    quantidade = crud_usuario.count_usuarios(db)
    return {"quantidade": quantidade}
