from sqlmodel import Session, select
from app.models.aluno import Aluno
from app.schemas.schema_aluno import AlunoCreate, AlunoUpdate

def get_aluno_by_email(db: Session, email: str) -> Aluno | None:
    return db.exec(select(Aluno).where(Aluno.email == email)).first()

def create_aluno(db: Session, aluno: AlunoCreate) -> Aluno:
    db_aluno = Aluno.model_validate(aluno)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def get_alunos(db: Session, skip: int = 0, limit: int = 100) -> list[Aluno]:
    return db.exec(select(Aluno).offset(skip).limit(limit)).all()
