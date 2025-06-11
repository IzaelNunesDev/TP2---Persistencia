from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.crud import crud_aluno
from app.schemas import schema_aluno

router = APIRouter()

@router.post("/", response_model=schema_aluno.AlunoRead, status_code=201)
def create_aluno_endpoint(
    *,
    db: Session = Depends(get_session),
    aluno_in: schema_aluno.AlunoCreate
):
    db_aluno = crud_aluno.get_aluno_by_email(db, email=aluno_in.email)
    if db_aluno:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    return crud_aluno.create_aluno(db=db, aluno=aluno_in)

@router.get("/", response_model=List[schema_aluno.AlunoRead])
def read_alunos_endpoint(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    alunos = crud_aluno.get_alunos(db, skip=skip, limit=limit)
    return alunos
