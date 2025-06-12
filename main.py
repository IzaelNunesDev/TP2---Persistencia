
from fastapi import FastAPI, APIRouter
from app.routers import router_aluno, router_motorista, router_rota, router_ponto_de_parada, router_veiculo, router_viagem, router_incidente, router_registro_frequencia

app = FastAPI(
    title="RotaFácil API - TP2",
    description="API para gerenciar o transporte universitário.",
    version="1.0.0"
)

# --- Roteador Principal da API v1 ---
api_router = APIRouter(prefix="/api/v1")

# Adiciona os routers de cada recurso ao router principal da API
api_router.include_router(router_aluno.router, prefix="/alunos", tags=["Alunos"])
api_router.include_router(router_motorista.router, prefix="/motoristas", tags=["Motoristas"])
api_router.include_router(router_rota.router, prefix="/rotas", tags=["Rotas"])
api_router.include_router(router_ponto_de_parada.router, prefix="/pontos-de-parada", tags=["Pontos de Parada"])
api_router.include_router(router_veiculo.router, prefix="/veiculos", tags=["Veículos"])
api_router.include_router(router_viagem.router, prefix="/viagens", tags=["Viagens"])
api_router.include_router(router_incidente.router, prefix="/incidentes", tags=["Incidentes"])
api_router.include_router(router_registro_frequencia.router, prefix="/registros-frequencia", tags=["Frequência"])

# Inclui o router da API no app principal
app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"message": "Bem-vindo à API RotaFácil!"}
