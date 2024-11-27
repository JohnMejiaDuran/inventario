# minas_view.py

from database.models.minas import Mina
from database.models.clientes import Cliente
from database.models.lotes import Lote
from .BaseView import BaseView
from sqlalchemy.orm import sessionmaker
from database.db import engine

Session = sessionmaker(bind=engine)
session = Session()

class LoteView(BaseView):
    def __init__(self, page):
        entity_name = "Lote"
        model = Lote
        campos_formulario = [
            ("nombre_lote", "TextField", "Nombre"),
            ("id_cliente", "Dropdown", "Cliente"),
            ("id_mina", "Dropdown", "Mina"),
            ("estado", "Checkbox", "Activo"),
        ]
        columnas_tabla = [
            ("nombre_lote", "Nombre Lote"),
            ("cliente_nombre", "Cliente"),
            ("cliente_mina", "Mina"),
            ("estado", "Estado"),
        ]

        # Definir cómo cargar las opciones del dropdown
        dropdown_fields = {
            "id_cliente": self.obtener_opciones_clientes,
            "id_mina": self.obtener_opciones_minas,
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
    
    def obtener_opciones_minas(self, id_cliente=None):
        """Retorna las opciones para el dropdown de minas filtradas por cliente."""
        try:
            if id_cliente:
                minas = session.query(Mina).filter_by(id_cliente=id_cliente).all()
            else:
                minas = []
            return [{"key": mina.id, "text": mina.nombre_mina} for mina in minas]
        except Exception as ex:
            print(f"Error al obtener minas: {ex}")
            return []