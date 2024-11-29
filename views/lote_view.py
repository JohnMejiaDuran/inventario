# minas_view.py
import flet as ft
from controllers.control_cliente import ControlCliente
from controllers.control_lote import ControlLote
from controllers.control_minas import ControlMina

class LoteView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador_lote = ControlLote()
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        
        page.title = "Lotes"
        # Navigation button
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        
        # Input fields
        self.insert_lote = ft.TextField(label="Lote", expand=True)
        self.insert_cliente = ft.Dropdown(
            label="Cliente", 
            options=[
                ft.dropdown.Option(cliente.nombre_cliente) 
                for cliente in self.controlador_cliente.obtener_clientes()
                if cliente.estado
            ],
            on_change=self.actualizar_minas
        )
        self.insert_mina = ft.Dropdown(label="Mina")
        # Active status checkbox
        # self.estado_lote = ft.Checkbox(label="Activo", value=True)
        # Edit lote
        self.lote_seleccionado = None
        self.modal_lote = ft.TextField(label="Lote")
        self.modal_cliente = ft.TextField(label="Cliente")
        self.modal_mina = ft.TextField(label="Mina")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        # Save button with custom click handler
        self.button_save = ft.ElevatedButton(
            text="Guardar lote",
            on_click=self.guardar_lote
        )
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Lote"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Cliente"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Mina"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("No. Contrato"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Booking"),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Acciones"),heading_row_alignment=ft.MainAxisAlignment.CENTER)
            ],
            rows=[]
        )
        # Main content layout
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo lote", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.insert_lote,
                    self.insert_cliente,
                    self.insert_mina
                    ]),
                # self.estado_lote,
                self.button_save,
                ft.Column(
                    controls=[
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )
            ],
        )
        self.cargar_lotes()
 
    def ir_atras(self, _):
        self.page.go("/datos")

    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet."""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.RED if es_error else ft.colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def actualizar_minas(self, e):
        """Al seleccionar un cliente me trae sus minas """
        cliente_seleccionado = self.insert_cliente.value
        self.insert_mina.options = []
        # obtener la mina del cliente seleccionado
        minas = self.controlador_mina.obtener_minas()
        minas = [mina for mina in minas if mina.id_cliente == cliente_seleccionado]
        if minas:
            self.insert_mina.options = [
                ft.dropdown.Option(mina.nombre_mina) for mina in minas
                if mina.estado 
            ]
        self.page.update()
        
    
    def guardar_lote(self, _):
        """Guardar lote"""
        datos_lote = {
            'nombre_lote': self.insert_lote.value.upper(),
            'id_cliente': self.insert_cliente.value,
            'id_mina': self.insert_mina.value if self.insert_mina.value else None,
            # 'estado': self.estado_lote.value
        }

        try:
            self.controlador_lote.crear_lote(datos_lote)
            self.mostrar_mensaje("Lote creado exitosamente")
            
            self.insert_lote.value = ""
            self.insert_cliente.value = ""
            self.insert_mina.value = ""
            self.cargar_lotes()
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)
    
    def cargar_prefijo(self):
        clientes = self.controlador_cliente.obtener_clientes()
        prefijo = [cliente.prefijo_cliente for cliente in clientes if cliente.nombre_cliente == self.insert_cliente.value]
        print(prefijo[0])   
    
    
    def cargar_lotes(self):
        lotes = self.controlador_lote.obtener_lotes()
        self.data_table.rows = []
        for lote in lotes:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(lote.id_lote))),
                        ft.DataCell(ft.Text(lote.nombre_lote)),
                        ft.DataCell(ft.Text(lote.id_cliente,)),
                        ft.DataCell(ft.Text(lote.id_mina, )),
                        ft.DataCell(ft.Text("6263233.2.1",)),
                        ft.DataCell(ft.Text("2656512",)),
                        # ft.DataCell(ft.Text("Activo" if lote.estado else "Inactivo")),
                        ft.DataCell(
                            ft.Row([
                                ft.TextButton("Editar", on_click=lambda _: self.cargar_prefijo()),
                            ],
                                spacing=5
                            )
                        )
                    ]
                )
            )
        self.page.update()