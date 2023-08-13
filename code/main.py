from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi
from models import Curso, Aluno
from database import engine, Base, get_db
from repositories import CursoRepository, AlunoRepository
from schemas import CursoRequest, CursoResponse, AlunoRequest, AlunoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


# /api/cursos

# Create
@app.post("/api/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def create(request: CursoRequest, db: Session = Depends(get_db)):
    curso = CursoRepository.save(db, Curso(**request.dict()))
    return CursoResponse.from_orm(curso)

# Read all


@app.get("/api/cursos", response_model=list[CursoResponse])
def find_all(db: Session = Depends(get_db)):
    cursos = CursoRepository.find_all(db)
    return [CursoResponse.from_orm(curso) for curso in cursos]

# Read (by id)


@app.get("/api/cursos/{curso_id}", response_model=CursoResponse, status_code=status.HTTP_200_OK)
def find_by_id(db: Session = Depends(get_db), curso_id: int = None):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso == None:
        raise HTTPException(status_code=404,
                            detail="Curso nao encontrado")
    return CursoResponse.from_orm(curso)

# Delete (by id)


@app.delete("/api/cursos/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(db: Session = Depends(get_db), curso_id: int = None):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso == None:
        raise HTTPException(status_code=404,
                            detail="Curso nao encontrado")
    alunos = AlunoRepository.find_all(db)
    for aluno in alunos:
        if aluno.id_curso == curso_id:
            raise HTTPException(status_code=400,
                                detail="Existem alunos matriculados no curso")
    CursoRepository.delete_by_id(db, curso_id)

# Update (by id)


@app.put("/api/cursos/{curso_id}", response_model=CursoResponse, status_code=status.HTTP_200_OK)
def update_by_id(request: CursoRequest, db: Session = Depends(get_db), curso_id: int = None):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso == None:
        raise HTTPException(status_code=404,
                            detail="Curso nao encontrado")
    curso = Curso(**request.dict())
    curso.id = curso_id
    curso = CursoRepository.save(db, curso)
    return CursoResponse.from_orm(curso)


# /api/alunos
# Create
@app.post("/api/alunos", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def create(request: AlunoRequest, db: Session = Depends(get_db)):
    if not CursoRepository.exists_by_id(db, request.id_curso):
        raise HTTPException(status_code=404,
                            detail="Curso nao encontrado, id invalido")
    aluno = AlunoRepository.save(db, Aluno(**request.dict()))
    return AlunoResponse.from_orm(aluno)

# Read all


@app.get("/api/alunos", response_model=list[AlunoResponse])
def find_all(db: Session = Depends(get_db)):
    alunos = AlunoRepository.find_all(db)
    return [AlunoResponse.from_orm(aluno) for aluno in alunos]

# Read (by id)


@app.get("/api/alunos/{aluno_id}", response_model=AlunoResponse, status_code=status.HTTP_200_OK)
def find_by_id(db: Session = Depends(get_db), aluno_id: int = None):
    aluno = AlunoRepository.find_by_id(db, aluno_id)
    if aluno == None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return AlunoResponse.from_orm(aluno)

# Delete (by id)


@app.delete("/api/alunos/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(db: Session = Depends(get_db), aluno_id: int = None):
    aluno = AlunoRepository.find_by_id(db, aluno_id)
    if aluno == None:
        raise HTTPException(status_code=404,
                            detail="Aluno nao encontrado")
    curso = CursoRepository.find_by_id(db, aluno.id_curso)
    if curso.active == True:
        raise HTTPException(status_code=400,
                            detail="Nao foi possivel excluir o aluno, pois ele esta vinculado a um curso ativo")
    AlunoRepository.delete_by_id(db, aluno_id)

# Update (by id)


@app.put("/api/alunos/{aluno_id}", response_model=AlunoResponse, status_code=status.HTTP_200_OK)
def update_by_id(request: AlunoRequest, db: Session = Depends(get_db), aluno_id: int = None):
    aluno = AlunoRepository.find_by_id(db, aluno_id)
    if aluno == None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    aluno = Aluno(**request.dict())
    aluno.id = aluno_id
    if not CursoRepository.exists_by_id(db,aluno.id_curso):
        raise HTTPException(status_code=404, detail="Curso nao encontrado")
    aluno.curso = CursoRepository.find_by_id(db, aluno.id_curso)
    aluno = AlunoRepository.save(db, aluno)
    return AlunoResponse.from_orm(aluno)


# config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ambiente Virtual de Aprendizagem",
        version="1.0.0",
        summary="Alunos EAD",
        description="Sistema de Ambiente Virtual de Aprendizagem para auxiliar alunos 100% EAD",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
