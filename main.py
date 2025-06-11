
from fastapi import FastAPI
from app.routers import router_aluno # Importe outros routers aqui

app = FastAPI(
    title="RotaFácil API - TP2",
    description="API para gerenciar o transporte universitário.",
    version="1.0.0"
)

# Inclui os endpoints do aluno no path /alunos
app.include_router(router_aluno.router, prefix="/alunos", tags=["Alunos"])
# Inclua os outros routers aqui (motoristas, rotas, etc.)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API RotaFácil!"}
