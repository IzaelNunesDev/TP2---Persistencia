from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.logger import get_logger
from app.schemas.schema_incidente import IncidenteCreate, IncidenteRead
from app.crud import crud_incidente, crud_viagem, crud_usuario

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=IncidenteRead, status_code=201)
def create_new_incidente(incidente: IncidenteCreate, session: Session = Depends(get_session)):
    logger.info(f"Criando incidente para viagem {incidente.viagem_id}")
    # Validações
    if not crud_viagem.get_viagem_by_id(session, incidente.viagem_id):
        logger.warning(f"Viagem com id {incidente.viagem_id} não encontrada")
        raise HTTPException(status_code=404, detail=f"Viagem com id {incidente.viagem_id} não encontrada")
    if not crud_usuario.get_usuario_by_id(session, user_id=incidente.reportado_por_usuario_id):
        logger.warning(f"Usuário reportador com id {incidente.reportado_por_usuario_id} não encontrado")
        raise HTTPException(status_code=404, detail=f"Usuário reportador com id {incidente.reportado_por_usuario_id} não encontrado")
    try:
        novo_incidente = crud_incidente.create_incidente(db=session, incidente_in=incidente)
        logger.info(f"Incidente criado com ID {novo_incidente.id}")
        return novo_incidente
    except Exception as e:
        logger.error(f"Erro ao criar incidente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/por-viagem/{viagem_id}", response_model=List[IncidenteRead])
def read_incidentes_from_viagem(viagem_id: int, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    logger.info(f"Listando incidentes para viagem {viagem_id}")
    if not crud_viagem.get_viagem_by_id(session, viagem_id):
        logger.warning(f"Viagem com id {viagem_id} não encontrada ao listar incidentes")
        raise HTTPException(status_code=404, detail=f"Viagem com id {viagem_id} não encontrada")

    incidentes = crud_incidente.get_incidentes_by_viagem(session, viagem_id=viagem_id, skip=skip, limit=limit)
    return incidentes

@router.get("/quantidade", response_model=dict)
def count_incidentes_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando incidentes")
    quantidade = crud_incidente.count_incidentes(session)
    return {"quantidade": quantidade}
