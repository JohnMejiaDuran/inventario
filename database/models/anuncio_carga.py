from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class AnuncioCarga(Base):
    __tablename__ = "anuncios_cargas"
    id_anuncio_carga = Column(Integer, primary_key=True, autoincrement=True)
    placa_contenedor = Column(String(100), nullable=False)
    id_transpordor = Column(Integer, ForeignKey("transportadores.id_transportador"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_tipo_producto = Column(Integer, ForeignKey("tipos_productos.id_tipo_producto"), nullable=False)
    id_tipo_unidad = Column(Integer, ForeignKey("tipos_unidades.id_tipo_unidad"), nullable=False)
    unidades_anunciadas = Column(Float, nullable=False)
    peso_anunciado = Column(Float, nullable=False)
    
    transportadores = relationship("Transportador", back_populates="anuncios_cargas")
    productos = relationship("Producto", back_populates="anuncios_cargas")
    tipos_productos = relationship("TipoProducto", back_populates="anuncios_cargas")
    tipos_unidades = relationship("TipoUnidad", back_populates="anuncios_cargas")
    
