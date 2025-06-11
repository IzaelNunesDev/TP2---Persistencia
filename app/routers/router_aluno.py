from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.logger import get_logger
from app.crud.crud_aluno import create_aluno, get_alunos, count_alunos, get_aluno_by_id, update_aluno, delete_aluno
from app.crud.crud_usuario import get_usuario_by_email
from app.schemas.schema_aluno import AlunoCreate, AlunoRead, AlunoUpdate

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=AlunoRead, status_code=201)
def create_aluno_endpoint(
    *,
    db: Session = Depends(get_session),
    aluno_in: AlunoCreate
):
    logger.info(f"Tentando criar aluno com email: {aluno_in.email}")
    db_user = get_usuario_by_email(db, email=aluno_in.email)
    if db_user:
        logger.warning(f"Email {aluno_in.email} já cadastrado.")
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    try:
        aluno = create_aluno(db=db, aluno_in=aluno_in)
        logger.info(f"Aluno criado com ID {aluno.id}")
        return aluno
    except Exception as e:
        logger.error(f"Erro ao criar aluno: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=List[AlunoRead])
def read_alunos_endpoint(
    db: Session = Depends(get_session),
    nome: str = None,
    skip: int = 0,
    limit: int = 100
):
    logger.info(f"Listando alunos com filtro: nome='{nome}'")
    alunos = get_alunos(db, nome=nome, skip=skip, limit=limit)
    return alunos

@router.get("/quantidade", response_model=dict)
def count_alunos_endpoint(db: Session = Depends(get_session)):
    logger.info("Contando alunos")
    quantidade = count_alunos(db)
    return {"quantidade": quantidade}

@router.put("/{aluno_id}", response_model=AlunoRead)
def update_aluno_route(aluno_id: int, aluno_in: AlunoUpdate, db: Session = Depends(get_session)):
    logger.info(f"Atualizando aluno com ID: {aluno_id}")
    aluno = get_aluno_by_id(db, aluno_id)
    if not aluno:
        logger.error(f"Aluno com ID {aluno_id} não encontrado")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno = update_aluno(db, aluno, aluno_in)
    logger.info(f"Aluno com ID {aluno_id} atualizado com sucesso")
    return aluno

@router.delete("/{aluno_id}", status_code=204)
def delete_aluno_route(aluno_id: int, db: Session = Depends(get_session)):
    logger.info(f"Deletando aluno com ID: {aluno_id}")
    aluno = get_aluno_by_id(db, aluno_id)
    if not aluno:
        logger.error(f"Aluno com ID {aluno_id} não encontrado")
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    delete_aluno(db, aluno)
    logger.info(f"Aluno com ID {aluno_id} deletado com sucesso")
    return
