# Projeto de Gerenciamento de Transporte Universitário

Este é um projeto FastAPI para gerenciar um sistema de transporte universitário, incluindo o cadastro de alunos, motoristas, veículos, rotas e viagens.

## Pré-requisitos

- Python 3.9+
- pip (gerenciador de pacotes do Python)
- Um banco de dados PostgreSQL em execução

## 1. Configuração do Ambiente

Clone o repositório para a sua máquina local:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd TP2---Persistencia
```

Crie e ative um ambiente virtual (recomendado):

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## 2. Configuração do Banco de Dados

1.  **Crie um arquivo `.env`** na raiz do projeto, copiando o exemplo do `.env.example` (se houver) ou criando um novo.
2.  Adicione as suas credenciais do PostgreSQL ao arquivo `.env`:

    ```env
    DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"
    ```

    Substitua `USER`, `PASSWORD`, `HOST`, `PORT` e `DATABASE_NAME` pelos seus dados.

3.  **Aplique as migrações** do Alembic para criar as tabelas no banco de dados:

    ```bash
    alembic upgrade head
    ```

## 3. Executando a Aplicação

Com o ambiente configurado e o banco de dados pronto, inicie o servidor FastAPI com Uvicorn:

```bash
uvicorn main:app --reload
```

O servidor estará rodando em `http://127.0.0.1:8000`.

## 4. Acessando a API

-   **Documentação Interativa (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   **Documentação Alternativa (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
