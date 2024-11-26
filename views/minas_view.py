# minas_view.py

from database.models.minas import Mina
from database.models.clientes import Cliente
from .BaseView import BaseView
from sqlalchemy.orm import sessionmaker
from database.db import engine

Session = sessionmaker(bind=engine)
session = Session()

class MinasView(BaseView):
    def __init__(self, page):
        entity_name = "Mina"
        model = Mina
        campos_formulario = [
            ("nombre_mina", "TextField", "Nombre"),
            ("id_cliente", "Dropdown", "Cliente"),
            ("estado", "Checkbox", "Activo"),
        ]
        columnas_tabla = [
            ("nombre_mina", "Nombre Mina"),
            ("cliente_nombre", "Cliente"),
            ("estado", "Estado"),
        ]

        # Definir cómo cargar las opciones del dropdown
        dropdown_fields = {
            "id_cliente": self.obtener_opciones_clientes
        }

        super().__init__(page, entity_name, model, campos_formulario, columnas_tabla, dropdown_fields)

    def obtener_opciones_clientes(self):
        """Retorna las opciones para el dropdown de clientes."""
        try:
            clientes = session.query(Cliente).all()
            print(f"Clientes obtenidos en MinasView: {clientes}")  # Debug
            return [{"key": cliente.id, "text": cliente.nombre_cliente} for cliente in clientes]
        except Exception as ex:
            print(f"Error al obtener clientes para el dropdown en MinasView: {ex}")
            return []