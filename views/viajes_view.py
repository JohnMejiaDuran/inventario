import flet as ft
from controllers.control_viajes import ControlViaje

class ViajeView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlViaje()
        page.title = "viajes"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.barcaza_seleccionada = None
        
        # New viaje input fields
        self.nombre_viaje = ft.TextField(label="Nombre de viaje", expand=True)
        self.estado_viaje = ft.Checkbox(label="Activo", value=True)
        
        # Modal edit viaje fields
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        
        # Save button
        self.button_save = ft.ElevatedButton(
            text="Guardar viaje",
            on_click=self.guardar_viaje
        )
        
        # Data table for viajes
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[],
        )
        
        # Main content layout
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nueva viaje", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_viaje,
                self.estado_viaje,
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
        
        # Load existing viajes
        self.cargar_viajes()
    
    def cargar_viajes(self):
        """Cargar la lista de viajes en la tabla"""
        self.data_table.rows = []
        for index, viaje in enumerate(self.controlador.obtener_viajes()):
            estado_text = "ACTIVO" if viaje.estado_viaje else "INACTIVO"
            estado_text_color = None if viaje.estado_viaje else ft.colors.WHITE
            estado_bgcolor = None if viaje.estado_viaje else ft.colors.RED_400
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(viaje.nombre_viaje)),
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
                                ft.TextButton("Editar", on_click=lambda e, viaje=viaje: self.abrir_modal_editar(e, viaje)),
                            ])
                        )
                    ]
                )
            )
    
    def guardar_viaje(self, _):
        """Guardar una nueva viaje"""
        if not self.nombre_viaje.value:
            self.mostrar_mensaje("El nombre de la viaje es requerido.", es_error=True)
            return
        
        
        datos_viaje = {
            "nombre_viaje": self.nombre_viaje.value.upper(),

            "estado_viaje": self.estado_viaje.value
        }
        
        try:
            self.controlador.crear_viaje(datos_viaje)
            self.cargar_viajes()
            self.nombre_viaje.value = ""
            self.estado_viaje.value = True
            
            self.mostrar_mensaje("viaje guardada correctamente.")
        
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar la viaje: {str(e)}", es_error=True)
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet"""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.RED if es_error else ft.colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
        
    def ir_atras(self, e):
        """Maneja el evento de clic en el botón 'Atrás'"""
        self.page.go("/datos")
        
    def abrir_modal_editar(self, e, viaje):
        """Abrir modal para editar una viaje"""
        self.viaje_seleccionada = viaje
        
        self.modal_edit = ft.Container(
            expand=True,
            bgcolor=ft.colors.BLACK45,
            content=ft.Container(
                width=500,
                height=350,
                padding=20,
                bgcolor=ft.colors.WHITE,
                content=ft.Column(
                    controls=[
                        ft.Text("Editar viaje", size=20, weight=ft.FontWeight.BOLD),
                        self.modal_nombre,
                        self.modal_estado,
                        ft.Row(
                            controls=[
                                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                                ft.TextButton("Actualizar", on_click=self.actualizar_viaje),
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
        
        self.modal_nombre.value = viaje.nombre_viaje
        self.modal_estado.value = viaje.estado_viaje
        self.page.overlay.append(self.modal_edit)
        self.modal_open = True
        self.page.update()
        
    def cerrar_modal(self, e=None):
        """Cerrar el modal de edición"""
        self.modal_open = False

        # Cerrar y remover el modal del overlay
        if self.modal_edit and self.modal_edit in self.page.overlay:
            self.page.overlay.remove(self.modal_edit)
            self.modal_edit = None  # Limpiar la referencia

        self.page.update()
        
    def actualizar_viaje(self, e):
        """Actualizar una viaje existente"""
        if not self.modal_nombre.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        # Preparar datos actualizados
        datos_actualizados = {
            "nombre_viaje": self.modal_nombre.value.upper(),
            "estado_viaje": self.modal_estado.value
        }

        try:
            # Usar el controlador para actualizar la viaje
            viaje_actualizada = self.controlador.actualizar_viaje(self.viaje_seleccionada.id_viaje, datos_actualizados)
            
            if viaje_actualizada:
                # Recargar la tabla de viajes
                self.cargar_viajes()
                
                # Cerrar el modal
                self.cerrar_modal()
                
                # Mostrar mensaje de éxito
                self.mostrar_mensaje("viaje actualizada exitosamente")
            
        except ValueError as error:
            # Manejar errores de validación
            self.mostrar_mensaje(str(error), es_error=True)