from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.logger import get_logger
from app.schemas.schema_rota import RotaCreate, RotaRead
from app.crud import crud_rota

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=RotaRead, status_code=201)
def create_new_rota(rota: RotaCreate, session: Session = Depends(get_session)):
    """
    Cria uma nova rota.
    """
    logger.info(f"Criando rota com nome '{rota.nome_rota}'")
    try:
        nova_rota = crud_rota.create_rota(db=session, rota_in=rota)
        logger.info(f"Rota '{nova_rota.nome_rota}' criada com ID {nova_rota.id}")
        return nova_rota
    except Exception as e:
        logger.error(f"Erro ao criar rota: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[RotaRead])
def read_rotas(descricao: str = None, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Recupera uma lista de rotas.
    """
    logger.info(f"Listando rotas com filtro: descricao='{descricao}'")
    rotas = crud_rota.get_rotas(session, descricao=descricao, skip=skip, limit=limit)
    return rotas

@router.get("/{rota_id}", response_model=RotaRead)
def read_rota(rota_id: int, session: Session = Depends(get_session)):
    """
    Recupera uma rota específica pelo ID.
    """
    logger.info(f"Buscando rota com ID {rota_id}")
    db_rota = crud_rota.get_rota_by_id(session, rota_id=rota_id)
    if db_rota is None:
        logger.warning(f"Rota com ID {rota_id} não encontrada")
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return db_rota

@router.get("/quantidade", response_model=dict)
def count_rotas_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando rotas")
    quantidade = crud_rota.count_rotas(session)
    return {"quantidade": quantidade}
