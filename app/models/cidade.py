from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Cidade(Base):
    __tablename__ = "cidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    uf = Column(String(2), nullable=False)
    ativo = Column(Boolean, default=True)