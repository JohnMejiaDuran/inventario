from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Lote(Base):
    __tablename__ = 'lotes'
    id_lote = Column(Integer, primary_key=True, autoincrement=True)
    nombre_lote = Column(String(200), nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    id_mina = Column(Integer, ForeignKey('minas.id_mina'), nullable=True)

    
    clientes = relationship("Cliente", back_populates="lotes")  # Relación con Cliente
    minas = relationship("Mina", back_populates="lotes")