from database.db import session
from database.models.tipo_unidades import TipoUnidad
from sqlalchemy.exc import IntegrityError

class ControlTipoUnidad:
        
        def obtener_tipo_unidades(self):
            return session.query(TipoUnidad).all()
    
        def guardar_tipo_unidad(self, datos):
            try:
                existing_name = session.query(TipoUnidad).filter_by(nombre_tipo_unidad=datos['nombre_tipo_unidad']).first()
                
                if existing_name:
                    raise ValueError(f"Ya existe un tipo de unidad con el nombre '{datos['nombre_tipo_unidad']}'")
                
                nuevo_tipo_unidad = TipoUnidad(**datos)
                session.add(nuevo_tipo_unidad)
                session.commit()
                return nuevo_tipo_unidad
    
            except IntegrityError:
                session.rollback()
                raise ValueError("Error de integridad al guardar el tipo unidad")
    
        def actualizar_tipo_unidad(self, id_tipo_unidad, datos):
            try:
                tipo_unidad = session.query(TipoUnidad).get(id_tipo_unidad)
                if not tipo_unidad:
                    return None
                name_conflict = session.query(TipoUnidad).filter(
                    TipoUnidad.nombre_tipo_unidad == datos.get('nombre_tipo_unidad'),
                    TipoUnidad.id_tipo_unidad != id_tipo_unidad
                ).first()
                
                if name_conflict:
                    raise ValueError(f"Ya existe un tipo unidad con el nombre '{datos['nombre_tipo_unidad']}'")
                
                for key, value in datos.items():
                    setattr(tipo_unidad, key, value)
                session.commit()
                return tipo_unidad
    
            except IntegrityError:
                session.rollback()
                raise ValueError("Error de integridad al guardar el tipo unidad")
            
            