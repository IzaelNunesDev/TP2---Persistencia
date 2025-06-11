from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.logger import get_logger
from app.crud import crud_aluno, crud_usuario
from app.schemas import schema_aluno

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=schema_aluno.AlunoRead, status_code=201)
def create_aluno_endpoint(
    *,
    db: Session = Depends(get_session),
    aluno_in: schema_aluno.AlunoCreate
):
    logger.info(f"Tentando criar aluno com email: {aluno_in.email}")
    db_user = crud_usuario.get_usuario_by_email(db, email=aluno_in.email)
    if db_user:
        logger.warning(f"Email {aluno_in.email} já cadastrado.")
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    try:
        aluno = crud_aluno.create_aluno(db=db, aluno_in=aluno_in)
        logger.info(f"Aluno criado com ID {aluno.id}")
        return aluno
    except Exception as e:
        logger.error(f"Erro ao criar aluno: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[schema_aluno.AlunoRead])
def read_alunos_endpoint(
    db: Session = Depends(get_session),
    nome: str = None,
    skip: int = 0,
    limit: int = 100
):
    logger.info(f"Listando alunos com filtro: nome='{nome}'")
    alunos = crud_aluno.get_alunos(db, nome=nome, skip=skip, limit=limit)
    return alunos

@router.get("/quantidade", response_model=dict)
def count_alunos_endpoint(db: Session = Depends(get_session)):
    logger.info("Contando alunos")
    quantidade = crud_aluno.count_alunos(db)
    return {"quantidade": quantidade}
