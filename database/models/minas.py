from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Mina(Base):
    __tablename__ = 'minas'
    id_mina = Column(Integer, primary_key=True, autoincrement=True)
    nombre_mina = Column(String(200), nullable=False, unique=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    estado = Column(Boolean, default=True)
    
    clientes = relationship("Cliente", back_populates="minas")
    lotes = relationship("Lote", back_populates="minas")