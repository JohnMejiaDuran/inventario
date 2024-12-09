from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ..db import Base
from sqlalchemy.sql import func

class TipoUnidad(Base):
    __tablename__ = "tipo_unidades"
    id_tipo_unidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo_unidad = Column(String(100), nullable=False)
    estado_tipo_unidad = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())
    