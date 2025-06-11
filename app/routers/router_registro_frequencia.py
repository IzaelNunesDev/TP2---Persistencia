from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.logger import get_logger
from app.schemas.schema_registro_frequencia import RegistroFrequenciaCreate, RegistroFrequenciaRead
from app.crud import crud_registro_frequencia, crud_viagem, crud_aluno

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=RegistroFrequenciaRead, status_code=201)
def create_new_registro_frequencia(registro: RegistroFrequenciaCreate, session: Session = Depends(get_session)):
    """
    Registra a frequência (embarque/desembarque) de um aluno em uma viagem.
    """
    logger.info(f"Registrando frequência para aluno {registro.aluno_id} na viagem {registro.viagem_id}")
    # Validações
    if not crud_viagem.get_viagem_by_id(session, registro.viagem_id):
        logger.warning(f"Viagem com id {registro.viagem_id} não encontrada")
        raise HTTPException(status_code=404, detail=f"Viagem com id {registro.viagem_id} não encontrada")
    if not crud_aluno.get_aluno_by_id(session, aluno_id=registro.aluno_id):
        logger.warning(f"Aluno com id {registro.aluno_id} não encontrado")
        raise HTTPException(status_code=404, detail=f"Aluno com id {registro.aluno_id} não encontrado")
    try:
        novo_registro = crud_registro_frequencia.create_registro_frequencia(db=session, registro_in=registro)
        logger.info(f"Registro de frequência criado com ID {novo_registro.id}")
        return novo_registro
    except Exception as e:
        logger.error(f"Erro ao registrar frequência: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/por-viagem/{viagem_id}", response_model=List[RegistroFrequenciaRead])
def read_frequencia_from_viagem(viagem_id: int, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Recupera todos os registros de frequência de uma viagem específica.
    """
    logger.info(f"Listando registros de frequência para viagem {viagem_id}")
    if not crud_viagem.get_viagem_by_id(session, viagem_id):
        logger.warning(f"Viagem com id {viagem_id} não encontrada ao listar frequências")
        raise HTTPException(status_code=404, detail=f"Viagem com id {viagem_id} não encontrada")

    registros = crud_registro_frequencia.get_registros_by_viagem(session, viagem_id=viagem_id, skip=skip, limit=limit)
    return registros

@router.get("/quantidade", response_model=dict)
def count_registros_frequencia_endpoint(session: Session = Depends(get_session)):
    logger.info("Contando registros de frequência")
    quantidade = crud_registro_frequencia.count_registros_frequencia(session)
    return {"quantidade": quantidade}
