from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Apenas um engine é criado por aplicação
engine = create_engine(settings.DATABASE_URL, echo=True) # echo=True para ver os comandos SQL gerados

def create_db_and_tables():
    # Esta função não será necessária com Alembic, mas é bom tê-la para testes iniciais
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
