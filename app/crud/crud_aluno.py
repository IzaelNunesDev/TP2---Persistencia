from sqlmodel import Session, select
from app.models.aluno import Aluno
from app.models.usuario import Usuario
from app.schemas.schema_aluno import AlunoCreate # O schema precisa ser ajustado

# Esta função agora busca um Usuário, não um Aluno
def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    return db.exec(select(Usuario).where(Usuario.email == email)).first()

def create_aluno(db: Session, aluno_in: AlunoCreate) -> Aluno:
    # Passo 1: Criar o objeto Usuario
    # Idealmente, a senha deveria vir do schema e ser hasheada aqui
    usuario_obj = Usuario(
        email=aluno_in.email,
        nome_completo=aluno_in.nome_completo,
        senha_hash="senha_fake_hash", # Substituir por uma lógica de hashing real
        cargo="aluno"
    )
    db.add(usuario_obj)
    db.commit()
    db.refresh(usuario_obj)

    # Passo 2: Criar o objeto Aluno, ligando ao Usuario recém-criado
    aluno_obj = Aluno(
        matricula=aluno_in.matricula,
        telefone=aluno_in.telefone,
        documento_identidade=aluno_in.documento_identidade,
        possui_necessidade_especial=aluno_in.possui_necessidade_especial,
        usuario_id=usuario_obj.id
    )
    db.add(aluno_obj)
    db.commit()
    db.refresh(aluno_obj)
    
    return aluno_obj

def get_alunos(db: Session, skip: int = 0, limit: int = 100) -> list[Aluno]:
    return db.exec(select(Aluno).offset(skip).limit(limit)).all()
