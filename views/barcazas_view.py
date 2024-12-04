import flet as ft
from controllers.control_barcazas import ControlBarcaza

class BarcazaView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlBarcaza()
        page.title = "Barcazas"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.barcaza_seleccionada = None
        
        # New barcaza input fields
        self.nombre_barcaza = ft.TextField(label="Nombre de Barcaza", expand=True)
        self.estado_barcaza = ft.Checkbox(label="Activo", value=True)
        
        # Modal edit barcaza fields
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        
        # Save button
        self.button_save = ft.ElevatedButton(
            text="Guardar Barcaza",
            on_click=self.guardar_barcaza
        )
        
        # Data table for barcazas
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
                ft.Text("Nueva Barcaza", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_barcaza,
                self.estado_barcaza,
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
        
        # Load existing barcazas
        self.cargar_barcazas()
    
    def cargar_barcazas(self):
        """Cargar la lista de barcazas en la tabla"""
        self.data_table.rows = []
        for index, barcaza in enumerate(self.controlador.obtener_barcazas()):
            estado_text = "ACTIVO" if barcaza.estado_barcaza else "INACTIVO"
            estado_text_color = None if barcaza.estado_barcaza else ft.colors.WHITE
            estado_bgcolor = None if barcaza.estado_barcaza else ft.colors.RED_400
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(barcaza.nombre_barcaza)),
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
                                ft.TextButton("Editar", on_click=lambda e, barcaza=barcaza: self.abrir_modal_editar(e, barcaza)),
                            ])
                        )
                    ]
                )
            )
    
    def guardar_barcaza(self, _):
        """Guardar una nueva barcaza"""
        if not self.nombre_barcaza.value:
            self.mostrar_mensaje("El nombre de la barcaza es requerido.", es_error=True)
            return
        
        
        datos_barcaza = {
            "nombre_barcaza": self.nombre_barcaza.value.upper(),

            "estado_barcaza": self.estado_barcaza.value
        }
        
        try:
            self.controlador.crear_barcaza(datos_barcaza)
            self.cargar_barcazas()
            self.nombre_barcaza.value = ""
            self.estado_barcaza.value = True
            
            self.mostrar_mensaje("Barcaza guardada correctamente.")
        
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar la barcaza: {str(e)}", es_error=True)
    
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
        
    def abrir_modal_editar(self, e, barcaza):
        """Abrir modal para editar una barcaza"""
        self.barcaza_seleccionada = barcaza
        
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
                        ft.Text("Editar Barcaza", size=20, weight=ft.FontWeight.BOLD),
                        self.modal_nombre,
                        self.modal_estado,
                        ft.Row(
                            controls=[
                                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                                ft.TextButton("Actualizar", on_click=self.actualizar_barcaza),
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
        
        self.modal_nombre.value = barcaza.nombre_barcaza
        self.modal_estado.value = barcaza.estado_barcaza
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
        
    def actualizar_barcaza(self, e):
        """Actualizar una barcaza existente"""
        if not self.modal_nombre.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        # Preparar datos actualizados
        datos_actualizados = {
            "nombre_barcaza": self.modal_nombre.value.upper(),
            "estado_barcaza": self.modal_estado.value
        }

        try:
            # Usar el controlador para actualizar la barcaza
            barcaza_actualizada = self.controlador.actualizar_barcaza(self.barcaza_seleccionada.id_barcaza, datos_actualizados)
            
            if barcaza_actualizada:
                # Recargar la tabla de barcazas
                self.cargar_barcazas()
                
                # Cerrar el modal
                self.cerrar_modal()
                
                # Mostrar mensaje de éxito
                self.mostrar_mensaje("Barcaza actualizada exitosamente")
            
        except ValueError as error:
            # Manejar errores de validación
            self.mostrar_mensaje(str(error), es_error=True)