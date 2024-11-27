from database.db import session
from database.models.clientes import Cliente

class ControlCliente:
    def obtener_clientes(self):
        return session.query(Cliente).all()

    def crear_cliente(self, datos):
        nuevo_cliente = Cliente(**datos)
        session.add(nuevo_cliente)
        session.commit()
        return nuevo_cliente

    def actualizar_cliente(self, cliente_id, datos):
        cliente = session.query(Cliente).get(cliente_id)
        if cliente:
            for key, value in datos.items():
                setattr(cliente, key, value)
            session.commit()
            return cliente
        return None

    def eliminar_cliente(self, cliente_id):
        cliente = session.query(Cliente).get(cliente_id)
        if cliente:
            session.delete(cliente)
            session.commit()
            return True
        return False