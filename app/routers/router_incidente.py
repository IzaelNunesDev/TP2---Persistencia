from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_db
from app.schemas.schema_incidente import IncidenteCreate, IncidenteRead
from app.crud import crud_incidente, crud_viagem
from app.crud.crud_aluno import get_usuario_by_id 

router = APIRouter()

@router.post("/incidentes/", response_model=IncidenteRead, status_code=201)
def create_new_incidente(incidente: IncidenteCreate, db: Session = Depends(get_db)):
    """
    Registra um novo incidente para uma viagem.
    """
    # Validações
    if not crud_viagem.get_viagem_by_id(db, incidente.viagem_id):
        raise HTTPException(status_code=404, detail=f"Viagem com id {incidente.viagem_id} não encontrada")
    if not get_usuario_by_id(db, incidente.reportado_por_usuario_id):
        raise HTTPException(status_code=404, detail=f"Usuário reportador com id {incidente.reportado_por_usuario_id} não encontrado")

    return crud_incidente.create_incidente(db=db, incidente_in=incidente)

@router.get("/viagens/{viagem_id}/incidentes/", response_model=List[IncidenteRead])
def read_incidentes_from_viagem(viagem_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera os incidentes de uma viagem específica.
    """
    if not crud_viagem.get_viagem_by_id(db, viagem_id):
        raise HTTPException(status_code=404, detail=f"Viagem com id {viagem_id} não encontrada")

    incidentes = crud_incidente.get_incidentes_by_viagem(db, viagem_id=viagem_id, skip=skip, limit=limit)
    return incidentes
