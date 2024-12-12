from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(100), nullable=False)
    estado_producto = Column(Boolean, default=True)


