from database.db import session
from database.models.viajes import Viaje
from sqlalchemy.exc import IntegrityError

class ControlViaje:
    def obtener_viajes(self):
        return session.query(Viaje).all()

    def crear_viaje(self, datos):
        try:
            # Check for existing viaje with same name
            existing_name = session.query(Viaje).filter_by(nombre_viaje=datos['nombre_viaje']).first()
            if existing_name:
                raise ValueError(f"Ya existe un viaje con el nombre '{datos['nombre_viaje']}'")
            
            nuevo_viaje = Viaje(**datos)
            session.add(nuevo_viaje)
            session.commit()
            return nuevo_viaje

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el viaje")

    def actualizar_viaje(self, viaje_id, datos):
        try:
            viaje = session.query(Viaje).get(viaje_id)
            if not viaje:
                return None
            old_nombre = viaje.nombre_viaje
            # Check for name conflicts with other viajes
            name_conflict = session.query(Viaje).filter(
                Viaje.nombre_viaje == datos.get('nombre_viaje'),
                Viaje.id_viaje != viaje_id
            ).first()
            
            if name_conflict:
                raise ValueError(f"Ya existe otro viaje con el nombre '{datos['nombre_viaje']}'")
            for key, value in datos.items():
                setattr(viaje, key, value)
            session.commit()
            return viaje

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al actualizar el viaje")

    def eliminar_viaje(self, viaje_id):
        viaje = session.query(Viaje).get(viaje_id)
        if not viaje:
            return None
        session.delete(viaje)
        session.commit()
        return viaje