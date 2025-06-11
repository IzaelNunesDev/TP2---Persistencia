from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_db
from app.schemas.schema_registro_frequencia import RegistroFrequenciaCreate, RegistroFrequenciaRead
from app.crud import crud_registro_frequencia, crud_viagem, crud_aluno

router = APIRouter()

@router.post("/frequencia/", response_model=RegistroFrequenciaRead, status_code=201)
def create_new_registro_frequencia(registro: RegistroFrequenciaCreate, db: Session = Depends(get_db)):
    """
    Registra a frequência (embarque/desembarque) de um aluno em uma viagem.
    """
    # Validações
    if not crud_viagem.get_viagem_by_id(db, registro.viagem_id):
        raise HTTPException(status_code=404, detail=f"Viagem com id {registro.viagem_id} não encontrada")
    if not crud_aluno.get_aluno_by_id(db, aluno_id=registro.aluno_id):
        raise HTTPException(status_code=404, detail=f"Aluno com id {registro.aluno_id} não encontrado")

    return crud_registro_frequencia.create_registro_frequencia(db=db, registro_in=registro)

@router.get("/viagens/{viagem_id}/frequencia/", response_model=List[RegistroFrequenciaRead])
def read_frequencia_from_viagem(viagem_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera todos os registros de frequência de uma viagem específica.
    """
    if not crud_viagem.get_viagem_by_id(db, viagem_id):
        raise HTTPException(status_code=404, detail=f"Viagem com id {viagem_id} não encontrada")

    registros = crud_registro_frequencia.get_registros_by_viagem(db, viagem_id=viagem_id, skip=skip, limit=limit)
    return registros
