from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base

class TipoProducto(Base):
    __tablename__ = "tipos_productos"
    id_tipo_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo_producto = Column(String(100), nullable=False)
    estado_tipo_producto = Column(Integer, nullable=False)
    
    anuncios_cargas = relationship("AnuncioCarga", back_populates="tipo_producto")