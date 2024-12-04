from database.db import session
from database.models.movimientos import Movimiento
from sqlalchemy.exc import IntegrityError

class ControlMovimientos:
    def obtener_movimientos(self):
        return session.query(Movimiento).all()

    def crear_movimiento(self, datos):
        try:
            nuevo_movimiento = Movimiento(**datos)
            session.add(nuevo_movimiento)
            session.commit()
            return nuevo_movimiento

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el movimiento")

    def actualizar_movimiento(self, movimiento_id, datos):
        try:
            movimiento = session.query(Movimiento).get(movimiento_id)
            if not movimiento:
                return None
            for key, value in datos.items():
                setattr(movimiento, key, value)
            session.commit()
            return movimiento

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al actualizar el movimiento")

    def eliminar_movimiento(self, movimiento_id):
        movimiento = session.query(Movimiento).get(movimiento_id)
        if not movimiento:
            return None
        session.delete(movimiento)
        session.commit()
        return movimiento
    