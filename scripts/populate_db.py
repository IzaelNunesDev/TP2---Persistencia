import requests
import json
import logging
from pathlib import Path
import os

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL base da API
BASE_URL = "http://127.0.0.1:8000/api/v1"

# Dicionário de endpoints
ENDPOINTS = {
    "alunos": "/alunos/",
    "motoristas": "/motoristas/",
    "veiculos": "/veiculos/",
    "rotas": "/rotas/",
    "pontos_parada": "/pontos-de-parada/",
    "viagens": "/viagens/",
    "incidentes": "/incidentes/",
    "registros_frequencia": "/registros-frequencia/"
}

# Função para postar dados
def post_data(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP
        logging.info(f"Sucesso ao criar registro em {endpoint}: {response.json()['id']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao postar em {endpoint} com dados {data}: {e}")
        if e.response is not None:
            logging.error(f"Detalhe do erro: {e.response.text}")
        return None

def main():
    # Carrega os dados mockados
    data_path = Path(__file__).parent.parent / "data" / "mock_data.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        mock_data = json.load(f)

    logging.info("Iniciando a população do banco de dados...")

    # Dicionário para armazenar os IDs criados
    created_ids = {
        "alunos": [],
        "motoristas": [],
        "veiculos": [],
        "rotas": [],
        "viagens": [],
        "usuarios": []
    }

    # A ordem de população é importante devido às dependências
    # 1. Usuários (Alunos e Motoristas)
    for aluno in mock_data.get("alunos", []):
        result = post_data(ENDPOINTS["alunos"], aluno)
        if result:
            created_ids["alunos"].append(result['id'])
            created_ids["usuarios"].append(result['usuario']['id'])

    for motorista_data in mock_data.get("motoristas", []):
        motorista_payload = {
            **motorista_data,
            "data_admissao": motorista_data.get("data_admissao", "2023-01-15")
        }
        result = post_data(ENDPOINTS["motoristas"], motorista_payload)
        if result:
            created_ids["motoristas"].append(result['id'])
            created_ids["usuarios"].append(result['usuario']['id'])

    # 2. Veículos e Rotas
    for veiculo_data in mock_data.get("veiculos", []):
        veiculo_payload = {
            "placa": veiculo_data.get("placa"),
            "modelo": veiculo_data.get("modelo"),
            "capacidade_passageiros": veiculo_data.get("capacidade"),
            "ano_fabricacao": veiculo_data.get("ano"),
            "status_manutencao": veiculo_data.get("status_manutencao", "Disponível"),
            "adaptado_pcd": veiculo_data.get("adaptado_pcd", False)
        }
        result = post_data(ENDPOINTS["veiculos"], veiculo_payload)
        if result:
            created_ids["veiculos"].append(result['id'])

    for rota_data in mock_data.get("rotas", []):
        # Adapta o mock para o schema esperado pela API
        rota_payload = {
            "nome_rota": rota_data.get("nome"),
            "descricao": rota_data.get("descricao"),
            "turno": rota_data.get("turno", "Manhã"),  # Adiciona valor padrão
            "limite_atrasos_semanal": rota_data.get("limite_atrasos_semanal", 5), # Adiciona valor padrão
            "ativa": rota_data.get("ativa", True)
        }
        result = post_data(ENDPOINTS["rotas"], rota_payload)
        if result:
            created_ids["rotas"].append(result['id'])

    # 3. Pontos de Parada (dependem de Rotas)
    for i, ponto_data in enumerate(mock_data.get("pontos_parada", [])):
        if created_ids["rotas"] and ponto_data["rota_id"] <= len(created_ids["rotas"]):
            ponto_payload = {
                "rota_id": created_ids["rotas"][ponto_data["rota_id"] - 1],
                "nome_ponto": ponto_data.get("nome"),
                "endereco": ponto_data.get("endereco", f"Endereço do {ponto_data.get('nome')}"),
                "latitude": ponto_data.get("latitude"),
                "longitude": ponto_data.get("longitude"),
                "ordem": ponto_data.get("ordem", i + 1)
            }
            post_data(ENDPOINTS["pontos_parada"], ponto_payload)

    # 4. Viagens (dependem de Rotas, Veículos, Motoristas)
    for viagem in mock_data.get("viagens", []):
        if all(k in created_ids for k in ["rotas", "veiculos", "motoristas"]):
            viagem["rota_id"] = created_ids["rotas"][viagem["rota_id"] - 1]
            viagem["veiculo_id"] = created_ids["veiculos"][viagem["veiculo_id"] - 1]
            viagem["motorista_id"] = created_ids["motoristas"][viagem["motorista_id"] - 1]
            result = post_data(ENDPOINTS["viagens"], viagem)
            if result:
                created_ids["viagens"].append(result['id'])

    # 5. Incidentes e Registros de Frequência (dependem de Viagens, Alunos, Usuários)
    for incidente in mock_data.get("incidentes", []):
        if created_ids["viagens"] and created_ids["usuarios"]:
            incidente["viagem_id"] = created_ids["viagens"][incidente["viagem_id"] - 1]
            incidente["reportador_id"] = created_ids["usuarios"][incidente["reportador_id"] - 1]
            post_data(ENDPOINTS["incidentes"], incidente)

    for registro in mock_data.get("registros_frequencia", []):
        if created_ids["viagens"] and created_ids["alunos"]:
            registro["viagem_id"] = created_ids["viagens"][registro["viagem_id"] - 1]
            registro["aluno_id"] = created_ids["alunos"][registro["aluno_id"] - 1]
            post_data(ENDPOINTS["registros_frequencia"], registro)

    logging.info("População do banco de dados concluída.")

if __name__ == "__main__":
    main()
