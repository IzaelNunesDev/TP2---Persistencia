from sqlmodel import Session, select
from app.models.aluno import Aluno
from app.models.usuario import Usuario
from app.schemas.schema_aluno import AlunoCreate
from app.core.security import get_password_hash

def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    return db.exec(select(Usuario).where(Usuario.email == email)).first()

def get_usuario_by_id(db: Session, user_id: int) -> Usuario | None:
    return db.get(Usuario, user_id)


def create_aluno(db: Session, aluno_in: AlunoCreate) -> Aluno:
    # Cria o hash da senha
    hashed_password = get_password_hash(aluno_in.password)
    
    # Cria o objeto Usuario com os dados do schema
    usuario_obj = Usuario(
        email=aluno_in.email,
        nome_completo=aluno_in.nome_completo,
        senha_hash=hashed_password,
        cargo="aluno"
    )
    
    # Cria o objeto Aluno e já o vincula ao usuário
    aluno_obj = Aluno(
        matricula=aluno_in.matricula,
        telefone=aluno_in.telefone,
        documento_identidade=aluno_in.documento_identidade,
        possui_necessidade_especial=aluno_in.possui_necessidade_especial,
        usuario=usuario_obj  # SQLModel é inteligente o suficiente para lidar com isso
    )

    db.add(aluno_obj) # Adiciona apenas o Aluno (o Usuário será adicionado em cascata)
    db.commit()      # Apenas um commit, garantindo a atomicidade
    db.refresh(aluno_obj)
    
    return aluno_obj

def get_alunos(db: Session, skip: int = 0, limit: int = 100) -> list[Aluno]:
    return db.exec(select(Aluno).offset(skip).limit(limit)).all()

def get_aluno_by_id(db: Session, aluno_id: int) -> Aluno | None:
    return db.get(Aluno, aluno_id)

