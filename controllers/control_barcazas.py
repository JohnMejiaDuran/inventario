from database.db import session
from database.models.barcazas import Barcaza
from sqlalchemy.exc import IntegrityError

class ControlBarcaza:
    def obtener_barcazas(self):
        return session.query(Barcaza).all()

    def crear_barcaza(self, datos):
        try:
            # Check for existing barcaza with same name
            existing_name = session.query(Barcaza).filter_by(nombre_barcaza=datos['nombre_barcaza']).first()
            if existing_name:
                raise ValueError(f"Ya existe una barcaza con el nombre '{datos['nombre_barcaza']}'")
            
            nueva_barcaza = Barcaza(**datos)
            session.add(nueva_barcaza)
            session.commit()
            return nueva_barcaza

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar la barcaza")

    def actualizar_barcaza(self, barcaza_id, datos):
        try:
            barcaza = session.query(Barcaza).get(barcaza_id)
            if not barcaza:
                return None
            old_nombre = barcaza.nombre_barcaza
            # Check for name conflicts with other barcazas
            name_conflict = session.query(Barcaza).filter(
                Barcaza.nombre_barcaza == datos.get('nombre_barcaza'),
                Barcaza.id_barcaza != barcaza_id
            ).first()
            
            if name_conflict:
                raise ValueError(f"Ya existe otra barcaza con el nombre '{datos['nombre_barcaza']}'")
            for key, value in datos.items():
                setattr(barcaza, key, value)
            session.commit()
            return barcaza

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al actualizar la barcaza")

    def eliminar_barcaza(self, barcaza_id):
        barcaza = session.query(Barcaza).get(barcaza_id)
        if not barcaza:
            return None
        session.delete(barcaza)
        session.commit()
        return barcaza