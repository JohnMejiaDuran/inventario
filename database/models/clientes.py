from sqlalchemy import Column, Integer, String, Boolean
from ..db import Base, engine


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, unique=True)
    nit = Column(String(20), nullable=False, unique=True)
    estado = Column(Boolean, default=True)