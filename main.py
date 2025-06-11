
from fastapi import FastAPI
from app.routers import router_aluno, router_motorista, router_rota, router_ponto_de_parada, router_veiculo, router_viagem, router_incidente, router_registro_frequencia # Importe outros routers aqui

app = FastAPI(
    title="RotaFácil API - TP2",
    description="API para gerenciar o transporte universitário.",
    version="1.0.0"
)

# Inclui os endpoints do aluno no path /alunos
app.include_router(router_aluno.router, prefix="/alunos", tags=["Alunos"])
app.include_router(router_motorista.router, tags=["Motoristas"]) # O prefixo já está no router
app.include_router(router_rota.router, tags=["Rotas"]) # O prefixo já está no router
app.include_router(router_ponto_de_parada.router, tags=["Pontos de Parada"]) # O prefixo já está no router
app.include_router(router_veiculo.router, tags=["Veículos"]) # O prefixo já está no router
app.include_router(router_viagem.router, tags=["Viagens"]) # O prefixo já está no router
app.include_router(router_incidente.router, tags=["Incidentes"]) # O prefixo já está no router
app.include_router(router_registro_frequencia.router, tags=["Frequência"]) # O prefixo já está no router
# Inclua os outros routers aqui (motoristas, rotas, etc.)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API RotaFácil!"}
