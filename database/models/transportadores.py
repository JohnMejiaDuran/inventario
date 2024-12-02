from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class Transportador(Base):
    __tablename__ = 'transportadores'
    id_transportador = Column(Integer, primary_key=True, autoincrement=True)
    nombre_transportador = Column(String(200), nullable=False, unique=True)
    estado = Column(Boolean, default=True)
    
    anuncios_cargas = relationship("AnuncioCarga", back_populates="transportadores")
    
    
    