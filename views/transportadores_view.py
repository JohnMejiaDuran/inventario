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
        self.nombre_transportador = ft.TextField(label="Transportador", expand=True)
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
            rows=[],
            
        )
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo transportador", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_transportador,
                self.estado_transportador,
                self.button_save,
                ft.Column(
                    controls=[
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH
                    
                )
            ]
        )
        self.cargar_transportadores()
    
    def cargar_transportadores(self):
        self.data_table.rows = []
        for index, transportador in enumerate(self.controlador.obtener_transportadores()):
            estado_text = "ACTIVO" if transportador.estado_transportador else "INACTIVO"
            estado_text_color = None if transportador.estado_transportador else ft.colors.WHITE
            estado_bgcolor = None if transportador.estado_transportador else ft.colors.RED_400
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(transportador.nombre_transportador)),
                        ft.DataCell(ft.Container(
                            content=ft.Text(
                                estado_text,
                                color=estado_text_color          
                            ),
                            bgcolor=estado_bgcolor,
                            padding=ft.padding.all(5)
                        )),
                        ft.DataCell(
                            ft.Row([
                                ft.TextButton("Editar", on_click=lambda e, transportador=transportador: self.abrir_modal_editar(e, transportador)),
                            ])
                        )
                    ]
                )
            )
    
    def guardar_transportador(self, _):
        if not self.nombre_transportador.value:
            self.mostrar_mensaje("El nombre del transportador es requerido.", es_error=True)
            return
        
        datos_transportador = {
            "nombre_transportador": self.nombre_transportador.value.upper(),
            "estado_transportador": self.estado_transportador.value
        }
        
        try:
            self.controlador.crear_transportador(datos_transportador)
            self.cargar_transportadores()
            self.nombre_transportador.value = ""
            self.estado_transportador.value = True
            
            self.mostrar_mensaje("Transportador guardado correctamente.")
        
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar el transportador: {str(e)}", es_error=True)
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet."""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.RED if es_error else ft.colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
        
    def ir_atras(self, e):
        """Maneja el evento de clic en el botón 'Atrás'."""
        self.page.go("/datos")
        
    def abrir_modal_editar(self, e, transportador):
        self.transportador_seleccionado = transportador
        
        self.modal_edit = ft.Container(
            expand=True,
            bgcolor=ft.colors.BLACK45,
            content=ft.Container(
                width=500,
                height=300,
                padding=20,
                bgcolor=ft.colors.WHITE,
                content=ft.Column(
                    controls=[
                        ft.Text("Editar transportador", size=20, weight=ft.FontWeight.BOLD),
                        self.modal_nombre,
                        self.modal_estado,
                        ft.Row(
                            controls=[
                                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                                ft.TextButton("Actualizar", on_click=self.actualizar_transportador),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                )
            ),
            alignment=ft.alignment.center
        )
        
        self.modal_nombre.value = transportador.nombre_transportador
        self.modal_estado.value = transportador.estado_transportador
        self.page.overlay.append(self.modal_edit)
        self.modal_open = True
        self.page.update()
        
    def cerrar_modal (self, e=None):
        """Close the edit modal."""
        self.modal_open = False

        # Cerrar y remover el modal del overlay
        if self.modal_edit and self.modal_edit in self.page.overlay:
            self.page.overlay.remove(self.modal_edit)
            self.modal_edit = None  # Limpiar la referencia

        self.page.update()
        print("Modal de edición cerrado.")  # Debug
        
    def actualizar_transportador(self, e):
        if not self.modal_nombre.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        # Prepare updated client data
        datos_actualizados = {
            "nombre_transportador": self.modal_nombre.value.upper(),
            "estado_transportador": self.modal_estado.value
        }

        try:
            # Use the controller to update the client
            transportador_actualizado = self.controlador.actualizar_transportador(self.transportador_seleccionado.id_transportador, datos_actualizados)
            
            if transportador_actualizado:
                # Reload the clients table
                self.cargar_transportadores()
                
                # Close the modal
                self.cerrar_modal()
                
                # Show success message
                self.mostrar_mensaje("Transportador actualizado exitosamente")
            
        except ValueError as error:
            # Handle validation errors
            self.mostrar_mensaje(str(error), es_error=True)