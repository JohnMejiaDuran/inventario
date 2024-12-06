from database.db import session
from database.models.clientes import Cliente
from sqlalchemy.exc import IntegrityError
from database.models.minas import Mina
from database.models.lotes import Lote

class ControlCliente:
    def obtener_clientes(self):
        return session.query(Cliente).all()

    def crear_cliente(self, datos):
        try:
            # Check for existing client with same name or NIT
            existing_name = session.query(Cliente).filter_by(nombre_cliente=datos['nombre_cliente']).first()
            existing_prefijo = session.query(Cliente).filter_by(prefijo_cliente=datos['prefijo_cliente']).first()
            existing_nit = session.query(Cliente).filter_by(nit=datos['nit']).first()

            if existing_name:
                raise ValueError(f"Ya existe un cliente con el nombre '{datos['nombre_cliente']}'")
            
            if existing_prefijo:
                raise ValueError(f"Ya existe un cliente con el prefijo '{datos['prefijo_cliente']}'")
            
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
            old_nombre = cliente.nombre_cliente
            # Check for name conflicts with other clients
            name_conflict = session.query(Cliente).filter(
                Cliente.nombre_cliente == datos.get('nombre_cliente'),
                Cliente.id_cliente != cliente_id
            ).first()
            
            prefijo_conflict = session.query(Cliente).filter(
                Cliente.prefijo_cliente == datos.get('prefijo_cliente'),
                Cliente.id_cliente != cliente_id
            ).first()
            
            # Check for NIT conflicts with other clients
            nit_conflict = session.query(Cliente).filter(
                Cliente.nit == datos.get('nit'),
                Cliente.id_cliente != cliente_id
            ).first()

            if name_conflict:
                raise ValueError(f"Ya existe otro cliente con el nombre '{datos['nombre_cliente']}'")
            
            if prefijo_conflict:
                raise ValueError(f"Ya existe otro cliente con el prefijo '{datos['prefijo_cliente']}'")
            
            if nit_conflict:
                raise ValueError(f"Ya existe otro cliente con el NIT '{datos['nit']}'")

            for key, value in datos.items():
                setattr(cliente, key, value)
                
            if old_nombre != datos.get('nombre_cliente'):
                #Update Cliente records
                session.query(Cliente).filter(Cliente.id_cliente == old_nombre).update(
                    {Cliente.id_cliente: datos
                     ['nombre_cliente']},
                    synchronize_session='fetch'
                )
                
                # Update Mina records
                session.query(Mina).filter(Mina.id_cliente == old_nombre).update(
                    {Mina.id_cliente: datos['nombre_cliente']},
                    synchronize_session='fetch'
                )
                
                # Update Lote records
                session.query(Lote).filter(Lote.id_cliente == old_nombre).update(
                    {Lote.id_cliente: datos['nombre_cliente']},
                    synchronize_session='fetch'
                )
            
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
    
    def obtener_cliente_por_id(self, cliente_id):
        return session.query(Cliente).get(cliente_id)
    
    def obtener_prefijo_cliente(self, cliente_id):
        cliente = session.query(Cliente).get(int(cliente_id))
        return cliente.prefijo_cliente if cliente else None