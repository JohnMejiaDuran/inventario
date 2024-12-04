from database.db import session
from database.models.bodegas import Bodega
from sqlalchemy.exc import IntegrityError

class ControlBodega:
    def obtener_bodegas(self):
        return session.query(Bodega).all()

    def crear_bodega(self, datos):
        try:
            # Check for existing bodega with same name
            existing_name = session.query(Bodega).filter_by(nombre_bodega=datos['nombre_bodega']).first()
            if existing_name:
                raise ValueError(f"Ya existe una bodega con el nombre '{datos['nombre_bodega']}'")
            
            nueva_bodega = Bodega(**datos)
            session.add(nueva_bodega)
            session.commit()
            return nueva_bodega

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar la bodega")

    def actualizar_bodega(self, bodega_id, datos):
        try:
            bodega = session.query(Bodega).get(bodega_id)
            if not bodega:
                return None
            old_nombre = bodega.nombre_bodega
            # Check for name conflicts with other bodegas
            name_conflict = session.query(Bodega).filter(
                Bodega.nombre_bodega == datos.get('nombre_bodega'),
                Bodega.id_bodega != bodega_id
            ).first()
            
            if name_conflict:
                raise ValueError(f"Ya existe otra bodega con el nombre '{datos['nombre_bodega']}'")
            for key, value in datos.items():
                setattr(bodega, key, value)
            session.commit()
            return bodega

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al actualizar la bodega")

    def eliminar_bodega(self, bodega_id):
        bodega = session.query(Bodega).get(bodega_id)
        if not bodega:
            return None
        session.delete(bodega)
        session.commit()
        return bodega