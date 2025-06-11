from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.schema_motorista import MotoristaCreate, MotoristaRead
from app.crud import crud_motorista

router = APIRouter()

@router.post("/motoristas/", response_model=MotoristaRead, status_code=201)
def create_new_motorista(motorista: MotoristaCreate, db: Session = Depends(get_db)):
    """
    Cria um novo motorista (e um usuário associado).
    """
    db_user = crud_motorista.get_usuario_by_email(db, email=motorista.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    return crud_motorista.create_motorista(db=db, motorista_in=motorista)
