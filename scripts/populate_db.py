# FILE: scripts/populate_db.py

import requests
import logging

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
    "viagens": "/viagens/",
    "registros_frequencia": "/registros-frequencia/"
}

# Função para postar dados
def post_data(endpoint, data):
    """Envia um POST request para o endpoint especificado e retorna a resposta JSON."""
    try:
        url = f"{BASE_URL}{endpoint}"
        logging.info(f"Enviando POST para {url} com dados: {data}")
        response = requests.post(url, json=data)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP (4xx ou 5xx)
        
        response_json = response.json()
        logging.info(f"Sucesso! Registro criado em {endpoint} com ID: {response_json.get('id', 'N/A')}")
        return response_json
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao postar em {endpoint} com dados {data}: {e}")
        if e.response is not None:
            logging.error(f"Detalhe do erro: {e.response.text}")
        return None

def main():
    logging.info("Iniciando a população do banco de dados com o cenário 'Mariana na Viagem UFC'...")

    # Passo 1: Criar o Motorista
    logging.info("--- Passo 1: Criando Motorista ---")
    motorista_payload = {
        "email": "carlos.souza@rotafacil.com",
        "nome_completo": "Carlos Souza",
        "password": "senhaMotorista456",
        "cnh": "98765432100",
        "data_admissao": "2022-08-15"
    }
    motorista_response = post_data(ENDPOINTS["motoristas"], motorista_payload)
    if not motorista_response:
        logging.error("Falha ao criar motorista. Abortando.")
        return
    motorista_id = motorista_response['id']

    # Passo 2: Criar o Aluno
    logging.info("--- Passo 2: Criando Aluno ---")
    aluno_payload = {
        "email": "mariana.lima@aluno.ufc.br",
        "nome_completo": "Mariana Lima",
        "password": "senhaAluno789",
        "matricula": "554433",
        "telefone": "85912345678",
        "possui_necessidade_especial": False
    }
    aluno_response = post_data(ENDPOINTS["alunos"], aluno_payload)
    if not aluno_response:
        logging.error("Falha ao criar aluno. Abortando.")
        return
    aluno_id = aluno_response['id']

    # Passo 3: Criar a Rota
    logging.info("--- Passo 3: Criando Rota ---")
    rota_payload = {
        "nome_rota": "Rota UFC - Manhã",
        "descricao": "Rota circular que passa pelos principais bairros e termina no Campus do Pici.",
        "turno": "Manhã",
        "limite_atrasos_semanal": 3,
        "ativa": True
    }
    rota_response = post_data(ENDPOINTS["rotas"], rota_payload)
    if not rota_response:
        logging.error("Falha ao criar rota. Abortando.")
        return
    rota_id = rota_response['id']

    # Passo 4: Criar o Veículo
    logging.info("--- Passo 4: Criando Veículo ---")
    veiculo_payload = {
        "placa": "PQP2I23",
        "modelo": "Marcopolo Torino S - Adaptado",
        "capacidade_passageiros": 42,
        "status_manutencao": "Disponível",
        "adaptado_pcd": True,
        "ano_fabricacao": 2023
    }
    veiculo_response = post_data(ENDPOINTS["veiculos"], veiculo_payload)
    if not veiculo_response:
        logging.error("Falha ao criar veículo. Abortando.")
        return
    veiculo_id = veiculo_response['id']

    # Passo 5: Criar a Viagem (Juntando tudo)
    logging.info("--- Passo 5: Criando a Viagem (Conectando as entidades) ---")
    viagem_payload = {
        "data_viagem": "2024-05-22",
        "hora_partida": "2024-05-22T06:30:00", # Mantido sem 'Z' para compatibilidade geral
        "status": "Agendada",
        "vagas_ocupadas": 0,
        "rota_id": rota_id,
        "motorista_id": motorista_id,
        "veiculo_id": veiculo_id
    }
    viagem_response = post_data(ENDPOINTS["viagens"], viagem_payload)
    if not viagem_response:
        logging.error("Falha ao criar viagem. Abortando.")
        return
    viagem_id = viagem_response['id']

    # Passo 6: Registrar a Frequência do Aluno na Viagem (A Ligação Final)
    logging.info("--- Passo 6: Registrando Frequência (A Ligação Final) ---")
    registro_payload = {
        "viagem_id": viagem_id,
        "aluno_id": aluno_id,
        "tipo_registro": "embarque"
    }
    registro_response = post_data(ENDPOINTS["registros_frequencia"], registro_payload)
    if not registro_response:
        logging.error("Falha ao registrar frequência. Abortando.")
        return

    logging.info("=" * 50)
    logging.info("Cenário completo criado com sucesso!")
    logging.info(f"Aluna Mariana (ID {aluno_id}) registrada na Viagem (ID {viagem_id}).")
    logging.info("=" * 50)

if __name__ == "__main__":
    main()