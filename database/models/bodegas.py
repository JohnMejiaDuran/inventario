from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class Bodega(Base):
    __tablename__ = 'bodegas'
    id_bodega = Column(Integer, primary_key=True, autoincrement=True)
    nombre_bodega = Column(String(200), nullable=False)
    estado_bodega = Column(Boolean, default=True)
    
    movimientos = relationship("Movimiento", back_populates="bodegas")