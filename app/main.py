from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.database import engine
# Import all models to ensure they are registered with SQLModel's metadata
from app.models.aluno import Aluno
from app.models.incidente import Incidente
from app.models.motorista import Motorista
from app.models.ponto_de_parada import PontoDeParada
from app.models.registro_frequencia import RegistroFrequencia
from app.models.rota import Rota
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo
from app.models.viagem import Viagem

from app.routers import (
    router_aluno,
    router_incidente,
    router_motorista,
    router_ponto_de_parada,
    router_registro_frequencia,
    router_rota,
    router_usuario,
    router_veiculo,
    router_viagem
)

def create_db_and_tables():
    # NOTE: This is a destructive operation, suitable for development environments.
    # It will delete and recreate all data on application startup.
    print("Dropping and recreating database tables...")
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("Database tables recreated successfully.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    create_db_and_tables()
    yield
    print("Application shutdown.")

app = FastAPI(
    title="API de Gerenciamento de Transporte Escolar",
    description="Uma API para gerenciar as operações de um sistema de transporte escolar.",
    version="1.0.0",
    lifespan=lifespan
)

# Incluindo os routers na aplicação principal
app.include_router(router_aluno.router, prefix="/api/v1/alunos", tags=["Alunos"])
app.include_router(router_incidente.router, prefix="/api/v1/incidentes", tags=["Incidentes"])
app.include_router(router_motorista.router, prefix="/api/v1/motoristas", tags=["Motoristas"])
app.include_router(router_ponto_de_parada.router, prefix="/api/v1/pontos-de-parada", tags=["Pontos de Parada"])
app.include_router(router_registro_frequencia.router, prefix="/api/v1/registros-frequencia", tags=["Registros de Frequência"])
app.include_router(router_rota.router, prefix="/api/v1/rotas", tags=["Rotas"])
app.include_router(router_usuario.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(router_veiculo.router, prefix="/api/v1/veiculos", tags=["Veículos"])
app.include_router(router_viagem.router, prefix="/api/v1/viagens", tags=["Viagens"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Transporte Escolar"}
