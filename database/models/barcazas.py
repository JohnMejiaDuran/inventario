from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class Barcaza(Base):
    __tablename__ = "barcazas"
    id_barcaza = Column(Integer, primary_key=True, autoincrement=True)
    nombre_barcaza = Column(String(200), nullable=False)
    estado_barcaza = Column(Boolean, default=True)
    
    movimientos = relationship("Movimiento", back_populates="barcazas")