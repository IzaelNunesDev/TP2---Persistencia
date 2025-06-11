import logging
import sys

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Saída para o console
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)
