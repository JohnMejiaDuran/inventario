from database.db import session
from database.models.anuncio_carga import AnuncioCarga
from sqlalchemy.exc import IntegrityError

class ControlAnuncioCarga:
        
        def obtener_anuncios_carga(self):
            return session.query(AnuncioCarga).all()
    
        def crear_anuncio_carga(self, datos):
            try:
                nuevo_anuncio_carga = AnuncioCarga(**datos)
                session.add(nuevo_anuncio_carga)
                session.commit()
                return nuevo_anuncio_carga
    
            except IntegrityError:
                session.rollback()
                raise ValueError("Error de integridad al guardar el anuncio de carga")
    
        def actualizar_anuncio_carga(self, id_anuncio_carga, datos):
            try:
                anuncio_carga = session.query(AnuncioCarga).get(id_anuncio_carga)
                if not anuncio_carga:
                    return None
                for key, value in datos.items():
                    setattr(anuncio_carga, key, value)
                session.commit()
                return anuncio_carga
    
            except IntegrityError:
                session.rollback()
                raise ValueError("Error de integridad al guardar el anuncio de carga")