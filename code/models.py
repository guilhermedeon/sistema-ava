from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Curso(Base):
    __tablename__ = "cursos"

    id: int = Column(Integer, primary_key=True, index=True)
    titulo: str = Column(String(100), nullable=False)
    descricao: str = Column(String(255), nullable=False)
    carga_horaria: int = Column(Integer, nullable=False)
    qtd_exercicios: int = Column(Integer, nullable=False)
    active: bool = Column(Boolean, nullable=False)


class Aluno(Base):
    __tablename__ = "alunos"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    sobrenome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False)
    idade: int = Column(Integer, nullable=False)
    cpf: str = Column(String(11), nullable=False)
    id_curso: int = Column(Integer, ForeignKey("cursos.id"))

    curso = relationship("Curso")
