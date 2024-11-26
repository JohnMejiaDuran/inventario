from database.models.clientes import Cliente  # Asegúrate de que el modelo Cliente está correctamente definido
from .BaseView import BaseView # Suponiendo que has guardado BaseView en un archivo llamado base_view.py

class ClientesView(BaseView):
    def __init__(self, page):
        entity_name = "Cliente"
        model = Cliente
        campos_formulario = [
            ("nombre_cliente", "TextField", "Nombre"),
            ("nit", "TextField", "NIT"),
            ("estado", "Checkbox", "Activo"),
        ]
        
        columnas_tabla = [(
            "nombre_cliente", "Nombre Cliente"), 
            ("nit", "NIT"), 
            ("estado", "Estado")]
        
        super().__init__(page, entity_name, model, campos_formulario, columnas_tabla)