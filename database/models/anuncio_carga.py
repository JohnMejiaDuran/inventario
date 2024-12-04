from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class AnuncioCarga(Base):
    __tablename__ = "anuncios_cargas"
    id_anuncio_carga = Column(Integer, primary_key=True, autoincrement=True)
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"), nullable=False)
    placa_contenedor = Column(String(100), nullable=False)
    id_transpordor = Column(Integer, ForeignKey("transportadores.id_transportador"), nullable=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_tipo_producto = Column(Integer, ForeignKey("tipos_productos.id_tipo_producto"), nullable=False)
    tipo_unidad = Column(String(100), nullable=False)
    unidades_anunciadas = Column(Float, nullable=False)
    peso_anunciado = Column(Float, nullable=False)
    
    # Add back_populates to both sides of the relationship
    lotes = relationship("Lote", back_populates="anuncio_cargas")
    transportadores = relationship("Transportador", back_populates="anuncio_cargas")
    productos = relationship("Producto", back_populates="anuncio_cargas")
    tipo_productos = relationship("TipoProducto", back_populates="anuncio_cargas")
    
