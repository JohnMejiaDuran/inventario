from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Lote(Base):
    __tablename__ = 'lotes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_lote = Column(String(200), nullable=False, unique=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    id_mina = Column(Integer, ForeignKey('minas.id'), nullable=False)
    estado = Column(Boolean, default=True)
    
    clientes = relationship("Cliente", back_populates="lotes")  # Relación con Cliente
    minas = relationship("Mina", back_populates="lotes")