from sqlmodel import Session, select, func
from app.models.aluno import Aluno
from app.schemas.schema_aluno import AlunoUpdate
from app.models.usuario import Usuario
from app.schemas.schema_aluno import AlunoCreate
from app.core.security import get_password_hash

def create_aluno(db: Session, aluno_in: AlunoCreate) -> Aluno:
    hashed_password = get_password_hash(aluno_in.password)
    usuario_obj = Usuario(
        email=aluno_in.email,
        nome_completo=aluno_in.nome_completo,
        senha_hash=hashed_password,
        cargo="aluno"
    )
    
    aluno_obj = Aluno(
        matricula=aluno_in.matricula,
        telefone=aluno_in.telefone,
        documento_identidade=aluno_in.documento_identidade,
        possui_necessidade_especial=aluno_in.possui_necessidade_especial,
        usuario=usuario_obj  
    )

    db.add(aluno_obj) 
    db.commit()      
    db.refresh(aluno_obj)
    
    return aluno_obj

def get_alunos(db: Session, nome: str = None, skip: int = 0, limit: int = 100) -> list[Aluno]:
    query = select(Aluno)
    if nome:    
        query = query.join(Usuario).where(Usuario.nome_completo.ilike(f"%{nome}%"))
    return db.exec(query.offset(skip).limit(limit)).all()

def get_aluno_by_id(db: Session, aluno_id: int) -> Aluno | None:
    return db.get(Aluno, aluno_id)

def count_alunos(db: Session) -> int:
    return db.exec(select(func.count(Aluno.id))).one()

def update_aluno(db: Session, aluno: Aluno, aluno_update: AlunoUpdate) -> Aluno:
    aluno_data = aluno_update.model_dump(exclude_unset=True)
    for key, value in aluno_data.items():
        setattr(aluno, key, value)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

def delete_aluno(db: Session, aluno: Aluno):
    db.delete(aluno)
    db.commit()
