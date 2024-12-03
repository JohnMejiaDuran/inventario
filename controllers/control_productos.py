from database.db import session
from database.models.productos import Producto
from sqlalchemy.exc import IntegrityError

class ControlProducto:
    
    def obtener_productos(self):
        return session.query(Producto).all()

    def crear_producto(self, datos):
        try:
            existing_name = session.query(Producto).filter_by(nombre_producto=datos['nombre_producto']).first()
            
            if existing_name:
                raise ValueError(f"Ya existe un producto con el nombre '{datos['nombre_producto']}'")
            
            nuevo_producto = Producto(**datos)
            session.add(nuevo_producto)
            session.commit()
            return nuevo_producto

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el producto")

    def actualizar_producto(self, id_producto, datos):
        try:
            producto = session.query(Producto).get(id_producto)
            if not producto:
                return None
            name_conflict = session.query(Producto).filter(
                Producto.nombre_producto == datos.get('nombre_producto'),
                Producto.id_producto != id_producto
            ).first()
            
            if name_conflict:
                raise ValueError(f"Ya existe otro producto con el nombre '{datos['nombre_producto']}'")
            
            for key, value in datos.items():
                setattr(producto, key, value)
            session.commit()
            return producto

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el producto")