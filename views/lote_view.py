# minas_view.py
import flet as ft
from controllers.control_cliente import ControlCliente
from controllers.control_lote import ControlLote

class LoteView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador_lote = ControlLote()
        self.controlador_cliente = ControlCliente()
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
            ]
        )
        self.insert_mina = ft.TextField(label="Mina", expand=True)
        self.insert_cantidad = ft.TextField(label="Cantidad", expand=True)
        # Active status checkbox
        self.estado_lote = ft.Checkbox(label="Activo", value=True)
        # Edit lote
        self.lote_seleccionado = None
        self.modal_lote = ft.TextField(label="Lote")
        self.modal_cliente = ft.TextField(label="Cliente")
        self.modal_mina = ft.TextField(label="Mina")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        # Save button with custom click handler
        self.button_save = ft.ElevatedButton(
            text="Guardar lote",
            # on_click=self.guardar_lote
        )
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Lote")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Mina")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )
        # Main content layout
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo lote", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.insert_lote, self.insert_cliente, self.insert_mina]),
                self.estado_lote,
                self.button_save,
                ft.Column(
                    controls=[
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                )
            ],
        )
        self.cargar_lotes()
    def ir_atras(self, _):
        self.page.go("/datos")
    
    def cargar_lotes(self):
        lotes = self.controlador_lote.obtener_lotes()
        self.data_table.rows = []
        for lote in lotes:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(lote.id))),
                        ft.DataCell(ft.Text(lote.nombre_lote)),
                        ft.DataCell(ft.Text(lote.cliente.nombre_cliente)),
                        ft.DataCell(ft.Text(lote.mina.nombre_mina)),
                        ft.DataCell(ft.Text(str(lote.cantidad))),
                        ft.DataCell(ft.Text("Activo" if lote.estado else "Inactivo")),
                        ft.DataCell(
                            ft.Row([
                                ft.TextButton("Editar", on_click=lambda _, lote=lote: self.editar_lote(lote)),
                                ft.TextButton("Eliminar", on_click=lambda _, lote=lote: self.eliminar_lote(lote))
                            ],
                                spacing=10
                            )
                        )
                    ]
                )
            )