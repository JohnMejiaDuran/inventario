from database.db import session
from database.models.tipos_productos import TipoProducto
from sqlalchemy.exc import IntegrityError

class ControlTipoProducto:
    
    def obtener_tipo_productos(self):
        return session.query(TipoProducto).all()

    def crear_producto(self, datos):
        try:
            existing_name = session.query(TipoProducto).filter_by(nombre_tipo_producto=datos['nombre_tipo_producto']).first()
            
            if existing_name:
                raise ValueError(f"Ya existe un tipo de producto con el nombre '{datos['nombre_tipo_producto']}'")
            
            nuevo_tipo_producto = TipoProducto(**datos)
            session.add(nuevo_tipo_producto)
            session.commit()
            return nuevo_tipo_producto

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el tipo producto")

    def actualizar_tipo_producto(self, id_tipo_producto, datos):
        try:
            tipo_producto = session.query(TipoProducto).get(id_tipo_producto)
            if not tipo_producto:
                return None
            name_conflict = session.query(TipoProducto).filter(
                TipoProducto.nombre_tipo_producto == datos.get('nombre_tipo_producto'),
                TipoProducto.id_tipo_producto != id_tipo_producto
            ).first()
            
            if name_conflict:
                raise ValueError(f"Ya existe un tipo producto con el nombre '{datos['nombre_tipo_producto']}'")
            
            for key, value in datos.items():
                setattr(tipo_producto, key, value)
            session.commit()
            return tipo_producto

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el tipo producto")