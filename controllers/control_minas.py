from database.db import session
from database.models.minas import Mina
from sqlalchemy.exc import IntegrityError
from database.models.clientes import Cliente

class ControlMina:
    def obtener_minas(self):
        return session.query(Mina).all()

    def crear_mina(self, datos):
        try:
            # Check for existing mine with same name
            existing_name = session.query(Mina).filter_by(nombre_mina=datos['nombre_mina']).first()

            if existing_name:
                raise ValueError(f"Ya existe una mina con el nombre '{datos['nombre_mina']}'")
            
            nueva_mina = Mina(**datos)
            session.add(nueva_mina)
            session.commit()
            return nueva_mina

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar la mina")
        
    def guardar_mina(self, nombre_mina, estado, cliente_nombre):
        try:
            # Validate input fields
            if not nombre_mina or nombre_mina.strip() == '':
                raise ValueError("El nombre de la mina no puede estar vacío")
            
            # Find the corresponding cliente by name
            cliente = session.query(Cliente).filter_by(nombre_cliente=cliente_nombre).first()
            
            if not cliente:
                raise ValueError(f"Cliente '{cliente_nombre}' no encontrado")
            
            # Prepare the data dictionary
            datos = {
                'nombre_mina': nombre_mina.strip(),  # Remove leading/trailing whitespace
                'estado': estado,
                'id_cliente': cliente.id_cliente  # Use the cliente's ID for the foreign key
            }
            
            # Check for existing mine with same name
            existing_name = session.query(Mina).filter_by(nombre_mina=nombre_mina.strip()).first()

            if existing_name:
                raise ValueError(f"Ya existe una mina con el nombre '{nombre_mina.strip()}'")
            
            nueva_mina = Mina(**datos)
            session.add(nueva_mina)
            session.commit()
            return nueva_mina

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar la mina")
        
    def actualizar_mina(self, mina_id, datos):
        try:
            mina = session.query(Mina).get(mina_id)
            if not mina:
                return None

            # Check for name conflicts with other mines
            name_conflict = session.query(Mina).filter(
                Mina.nombre_mina == datos.get('nombre_mina'),
                Mina.id_mina != mina_id
            ).first()

            if name_conflict:
                raise ValueError(f"Ya existe otra mina con el nombre '{datos['nombre_mina']}'")
            
            for key, value in datos.items():
                setattr(mina, key, value)
            session.commit()
            return mina

        except IntegrityError:
            session.rollback()
            raise ValueError("Error de integridad al guardar la mina")
