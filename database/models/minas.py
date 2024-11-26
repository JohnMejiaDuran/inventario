from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base


class Mina(Base):
    __tablename__ = 'minas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, unique=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    estado = Column(Boolean, default=True)
    
    # Add this relationship
    cliente = relationship("Cliente", back_populates="minas")
    