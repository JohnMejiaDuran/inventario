from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cliente = Column(String(200), nullable=False, unique=True)
    nit = Column(String(20), nullable=False, unique=True)
    estado = Column(Boolean, default=True)
    
    minas = relationship("Mina", back_populates="cliente")