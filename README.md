# Projeto de Gerenciamento de Transporte Universitário
Este é um projeto FastAPI para gerenciar um sistema de transporte universitário, incluindo o cadastro de alunos, motoristas, veículos, rotas e viagens.

## Pré-requisitos
- Python 3.9+
- pip (gerenciador de pacotes do Python)
- Um banco de dados PostgreSQL em execução

## 1. Configuração do Ambiente
Crie e ative um ambiente virtual (
# Windows
python -m venv venv
# Ative o ambiente virtual
./venv\Scripts\activate
# Instale as dependências do projeto:
pip install -r requirements.txt

## 2. Configuração do Banco de Dados

1.  **Crie um arquivo `.env`** na raiz do projeto.
2.  Adicione as suas credenciais do PostgreSQL ao arquivo `.env`:
    DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"

    Substitua `USER`, `PASSWORD`, `HOST`, `PORT` e `DATABASE_NAME` pelos seus dados.

3.  **Gerenciamento do Schema com Alembic**: O schema do banco de dados deste projeto é gerenciado exclusivamente pelo Alembic. Isso garante que a estrutura das tabelas seja consistente e versionada. O arquivo `create_tables.sql` é apenas uma referência e não deve ser usado para criar as tabelas.

4.  **Aplique as migrações** para criar ou atualizar as tabelas no banco de dados. Este comando é a única fonte de verdade para a estrutura do banco:

    alembic upgrade head


## 3. Executando a Aplicação

Com o ambiente configurado e o banco de dados pronto, inicie o servidor FastAPI com Uvicorn:

uvicorn main:app --reload

O servidor estará rodando em `http://127.0.0.1:8000`.

## 4. Acessando a API
-   **Documentação Interativa (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
