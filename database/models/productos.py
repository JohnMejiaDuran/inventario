from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(100), nullable=False)
    estado_pruducto = Column(Integer, nullable=False)

    anuncios_cargas = relationship("AnuncioCarga", back_populates="productos")