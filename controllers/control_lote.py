from database.db import session
from database.models.lotes import Lote
from sqlalchemy.exc import IntegrityError

class ControlLote:
    def obtener_lotes(self):
        return session.query(Lote).all()

    def crear_lote(self, datos):
        try:
            # Check for existing lot with same name
            existing_name = session.query(Lote).filter_by(nombre_lote=datos['nombre_lote']).first()

            if existing_name:
                raise ValueError(f"Ya existe un lote con el nombre '{datos['nombre_lote']}'")
            
            nuevo_lote = Lote(**datos)
            session.add(nuevo_lote)
            session.commit()
            return nuevo_lote

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el lote")

    def actualizar_lote(self, lote_id, datos):
        try:
            lote = session.query(Lote).get(lote_id)
            if not lote:
                return None

            # Check for name conflicts with other lots
            name_conflict = session.query(Lote).filter(
                Lote.nombre_lote == datos.get('nombre_lote'),
                Lote.id != lote_id
            ).first()

            if name_conflict:
                raise ValueError(f"Ya existe otro lote con el nombre '{datos['nombre_lote']}'")
            
            for key, value in datos.items():
                setattr(lote, key, value)
            session.commit()
            return lote

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el lote")