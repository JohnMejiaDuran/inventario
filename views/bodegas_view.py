import flet as ft
from controllers.control_bodegas import ControlBodega

class BodegaView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlBodega()
        page.title = "Bodegas"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.bodega_seleccionada = None
        
        # New barcaza input fields
        self.nombre_bodega = ft.TextField(label="Nombre de la Bodega", expand=True)
        self.estado_bodega = ft.Checkbox(label="Activo", value=True)
        
        # Modal edit bodega fields
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        
        # Save button
        self.button_save = ft.ElevatedButton(
            text="Guardar Bodega",
            on_click=self.guardar_bodega
        )
        
        # Data table for bodegas
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
                ft.Text("Nueva bodega", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_bodega,
                self.estado_bodega,
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
        
        # Load existing bodegas
        self.cargar_bodegas()
    
    def cargar_bodegas(self):
        """Cargar la lista de bodegas en la tabla"""
        self.data_table.rows = []
        for index, bodega in enumerate(self.controlador.obtener_bodegas()):
            estado_text = "ACTIVO" if bodega.estado_bodega else "INACTIVO"
            estado_text_color = None if bodega.estado_bodega else ft.colors.WHITE
            estado_bgcolor = None if bodega.estado_bodega else ft.colors.RED_400
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(bodega.nombre_bodega)),
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
                                ft.TextButton("Editar", on_click=lambda e, bodega=bodega: self.abrir_modal_editar(e, bodega)),
                            ])
                        )
                    ]
                )
            )
    
    def guardar_bodega(self, _):
        """Guardar una nueva bodega"""
        if not self.nombre_bodega.value:
            self.mostrar_mensaje("El nombre de la bodega es requerido.", es_error=True)
            return
        
        
        datos_bodega = {
            "nombre_bodega": self.nombre_bodega.value.upper(),
            "estado_bodega": self.estado_bodega.value
        }
        
        try:
            self.controlador.crear_bodega(datos_bodega)
            self.cargar_bodegas()
            self.nombre_bodega.value = ""
            self.estado_bodega.value = True
            
            self.mostrar_mensaje("bodega guardada correctamente.")
        
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar la bodega: {str(e)}", es_error=True)
    
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
        
    def abrir_modal_editar(self, e, bodega):
        """Abrir modal para editar una bodega"""
        self.bodega_seleccionada = bodega
        
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
                        ft.Text("Editar bodega", size=20, weight=ft.FontWeight.BOLD),
                        self.modal_nombre,
                        self.modal_estado,
                        ft.Row(
                            controls=[
                                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                                ft.TextButton("Actualizar", on_click=self.actualizar_bodega),
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
        
        self.modal_nombre.value = bodega.nombre_bodega
        self.modal_estado.value = bodega.estado_bodega
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
        
    def actualizar_bodega(self, e):
        """Actualizar una bodega existente"""
        if not self.modal_nombre.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        # Preparar datos actualizados
        datos_actualizados = {
            "nombre_bodega": self.modal_nombre.value.upper(),
            "estado_bodega": self.modal_estado.value
        }

        try:
            # Usar el controlador para actualizar la bodega
            bodega_actualizada = self.controlador.actualizar_bodega(self.bodega_seleccionada.id_bodega, datos_actualizados)
            
            if bodega_actualizada:
                # Recargar la tabla de bodegas
                self.cargar_bodegas()
                
                # Cerrar el modal
                self.cerrar_modal()
                
                # Mostrar mensaje de éxito
                self.mostrar_mensaje("bodega actualizada exitosamente")
            
        except ValueError as error:
            # Manejar errores de validación
            self.mostrar_mensaje(str(error), es_error=True)