from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class Viaje(Base):
    __tablename__ = 'viajes'
    id_viaje = Column(Integer, primary_key=True, autoincrement=True)
    nombre_viaje = Column(String(200), nullable=False)
    estado_viaje = Column(Boolean, default=True)
    
    movimientos = relationship("Movimiento", back_populates="viajes")