from database.db import session
from database.models.clientes import Cliente
from sqlalchemy.exc import IntegrityError

class ControlCliente:
    def obtener_clientes(self):
        return session.query(Cliente).all()

    def crear_cliente(self, datos):
        try:
            # Check for existing client with same name or NIT
            existing_name = session.query(Cliente).filter_by(nombre_cliente=datos['nombre_cliente']).first()
            existing_nit = session.query(Cliente).filter_by(nit=datos['nit']).first()

            if existing_name:
                raise ValueError(f"Ya existe un cliente con el nombre '{datos['nombre_cliente']}'")
            
            if existing_nit:
                raise ValueError(f"Ya existe un cliente con el NIT '{datos['nit']}'")

            nuevo_cliente = Cliente(**datos)
            session.add(nuevo_cliente)
            session.commit()
            return nuevo_cliente

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar el cliente")

    def actualizar_cliente(self, cliente_id, datos):
        try:
            cliente = session.query(Cliente).get(cliente_id)
            if not cliente:
                return None

            # Check for name conflicts with other clients
            name_conflict = session.query(Cliente).filter(
                Cliente.nombre_cliente == datos.get('nombre_cliente'),
                Cliente.id != cliente_id
            ).first()

            # Check for NIT conflicts with other clients
            nit_conflict = session.query(Cliente).filter(
                Cliente.nit == datos.get('nit'),
                Cliente.id != cliente_id
            ).first()

            if name_conflict:
                raise ValueError(f"Ya existe otro cliente con el nombre '{datos['nombre_cliente']}'")
            
            if nit_conflict:
                raise ValueError(f"Ya existe otro cliente con el NIT '{datos['nit']}'")

            for key, value in datos.items():
                setattr(cliente, key, value)
            session.commit()
            return cliente

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al actualizar el cliente")

    def eliminar_cliente(self, cliente_id):
        cliente = session.query(Cliente).get(cliente_id)
        if cliente:
            session.delete(cliente)
            session.commit()
            return True
        return False