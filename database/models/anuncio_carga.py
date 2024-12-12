from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from ..db import Base

class AnuncioCarga(Base):
    __tablename__ = "anuncios_cargas"
    id_anuncio_carga = Column(String(10), primary_key=True, unique=True)
    fecha_anuncio = Column(Date, nullable=True)
    cabezote = Column(String(20), nullable=True)
    empresa_de_transporte = Column(String(200), nullable=True)
    nit_empresa = Column(String(20), nullable=True)
    remolque = Column(String(20), nullable=True)
    tipo_vehiculo= Column(String(20), nullable=True)
    nombre_conductor = Column(String(200), nullable=True)
    numero_contacto_conductor = Column(String(20), nullable=True)
    numero_cedula = Column(String(20), nullable=True)
    documento_guia_transporte = Column(String(20), nullable=True)
    producto = Column(String(200), nullable=True)
    cantidad_a_cargar_gls = Column(Float, nullable=True)
    origen_destino = Column(String(200), nullable=True)
    enturnador = Column(String(200), nullable=True)
    cant = Column(Integer, nullable=True)
    orden_de_servicio = Column(String(20), nullable=True)
    ingreso = Column(Boolean, default=False)
    retiro = Column(Boolean, default=False)
    nal = Column(String (20), nullable=True)
    control_aduanero = Column(Boolean, default=True)
    cliente = Column(String(200), nullable=True)
    nit_cliente = Column(String(20), nullable=True)
    empresa_autorizada = Column(String(200), nullable=True)
    nit_empresa_autorizada = Column(String(20), nullable=True)
    nombre_barcaza = Column(String(200), nullable=True)
    nombre_remolcador = Column(String(200), nullable=True)
    numero_de_viaje = Column(String(20), nullable=True)
    fecha_de_llegada = Column(Date, nullable=True)
    manifiesto = Column(String(20), nullable=True)
    fecha_llegada = Column(Date, nullable=True)
    declaracion_importacion = Column(String(20), nullable=True)
    fecha_declaracion = Column(Date, nullable=True)
    levante = Column(String(20), nullable=True)
    fecha_leante = Column(Date, nullable=True)
    numero_contenedor = Column(String(20), nullable=True)
    longitud = Column(Integer, nullable=True)
    tipo_contenedor = Column(String(20), nullable=True)
    tara = Column(Integer, nullable=True)
    peso_declarado = Column(Integer, nullable=True)
    cantidad_a_cargar = Column(Integer, nullable=True)
    imo = Column(Integer, nullable=True)
    precintos_de_seguridad = Column(String(20), nullable=True)
    BL = Column(String(20), nullable=True)
    fecha_programacion_cargue_descargue = Column(Date, nullable=True)
    observaciones = Column(String(200), nullable=True)
    
    
    
    
    

    
