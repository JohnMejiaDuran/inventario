from sqlalchemy import Column, Integer, String, Boolean,Float,Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Movimiento(Base):
    __tablename__ = "movimientos"
    id_movimiento = Column(Integer, primary_key=True, autoincrement=True)
    tipo_movimiento = Column(String(200), nullable=False)
    unidades = Column(Float, nullable=True)
    neto_bascula = Column(Float, nullable=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(DateTime, nullable=True)
    hora_fin = Column(DateTime, nullable=True)
    para = Column(Float, nullable=True)
    tiempo_op = Column(Float, nullable=True)
    observaciones = Column(String(255), nullable=True)
    id_bodega = Column(Integer, ForeignKey('bodegas.id_bodega'),nullable=True)
    id_viajes = Column(Integer, ForeignKey('viajes.id_viaje'),nullable=False)
    id_barcaza = Column(Integer, ForeignKey('barcazas.id_barcaza'),nullable=False)
    
    barcazas = relationship("Barcaza", back_populates="movimientos")
    bodegas = relationship("Bodega", back_populates="movimientos")
    viajes = relationship("Viaje", back_populates="movimientos")