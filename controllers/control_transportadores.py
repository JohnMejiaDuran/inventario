from database.db import session
from database.models.transportadores import Transportador
from sqlalchemy.exc import IntegrityError

class ControlTransportador:
    def obtener_transportadores(self):
        return session.query(Transportador).all()

    def crear_transportador(self, datos):
        try:
            nuevo_transportador = Transportador(**datos)
            session.add(nuevo_transportador)
            session.commit()
            return nuevo_transportador

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el transportador")

    def actualizar_transportador(self, transportador_id, datos):
        try:
            transportador = session.query(Transportador).get(transportador_id)
            if not transportador:
                return None

            for key, value in datos.items():
                setattr(transportador, key, value)
            session.commit()
            return transportador

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el transportador")