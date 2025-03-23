from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    celular = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    codigo_ativacao = Column(String, nullable=True)
