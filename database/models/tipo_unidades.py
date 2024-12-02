from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base

class TipoUnidad(Base):
    __tablename__ = "tipos_unidades"
    id_tipo_unidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo_unidad = Column(String(100), nullable=False)
    estado_tipo_unidad = Column(Integer, nullable=False)
    
    anuncios_cargas = relationship("AnuncioCarga", back_populates="tipos_unidades")