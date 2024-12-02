import flet as ft
from controllers.control_transportadores import ControlTransportador

class TransportadoresView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlTransportador()
        page.title = "Transportadores"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.transportador_seleccionado = None
        self.insert_transportador = ft.TextField(label="Transportador", expand=True)
        self.estado_transportador = ft.Checkbox(label="Activo", value=True)
        
        #Modal edit transportador
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        self.button_save = ft.ElevatedButton(
            text="Guardar transportador",
            on_click=self.guardar_transportador
        )
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo transportador", size=20, weight=ft.FontWeight.BOLD),
                self.insert_transportador,
                self.estado_transportador,
                self.button_save,
                ft.Column(
                    controls=[
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ]
        )
        self.cargar_transportadores()
    
    def cargar_transportadores(self):
        self.data_table.rows = []
        for index, transportador in enumerate(self.controlador.obtener_transportadores()):
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(transportador.nombre_transportador)),
                        ft.DataCell(ft.Text("Activo" if transportador.estado else "Inactivo")),
                        ft.DataCell(
                            ft.Row([
                                ft.TextButton("Editar", on_click=lambda _:self.editar_transportador(transportador)),
                                ft.TextButton("Eliminar", on_click=lambda _:self.eliminar_transportador(transportador))
                            ])
                        )
                    ]
                )
            )
    
    def guardar_transportador(self, _):
        if self.modal_edit:
            self.controlador.actualizar_transportador(
                self.modal_edit,
                self.modal_nombre.value,
                self.modal_estado.value
            )
            self.modal_open = False
            self.modal_edit = None
        else:
            self.controlador.guardar_transportador(
                self.insert_transportador.value,
                self.estado_transportador.value
            )
        self.insert_transportador.value = ""
        self.estado_transportador.value = True
        self.cargar_transportadores()
        
    def ir_atras(self, e):
        """Maneja el evento de clic en el botón 'Atrás'."""
        self.page.go("/datos")