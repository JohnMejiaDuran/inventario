import flet as ft
from controllers.control_tipo_unidad import ControlTipoUnidad

class UnidadesView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlTipoUnidad()
        page.title = "Tipo de Unidades"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.tipo_unidad_seleccionada = None
        self.insert_nombre_tipo_unidad = ft.TextField(label="Tipo de Unidad", expand=True)
        self.estado_tipo_unidad = ft.Checkbox(label="Activo", value=True)
        self.button_save = ft.ElevatedButton(
            text="Guardar tipo de unidad",
            on_click=self.guardar_tipo_unidad
            
        )
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("Tipo de Unidad")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"), heading_row_alignment=ft.MainAxisAlignment.CENTER)
            ],
            rows=[]
        )
        
        self.modal_estado_unidad = None
        self.modal_nombre_unidad = None
        
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo tipo de unidad", size=20, weight=ft.FontWeight.BOLD),
                self.insert_nombre_tipo_unidad,
                self.estado_tipo_unidad,
                self.button_save,
                ft.Column(
                    controls=[
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                )
            ]
        )
        self.cargar_datos()
    
    def ir_atras(self, _):
        self.page.go("/datos")
    
    def cargar_datos(self):
        self.data_table.rows = []
        tipo_unidades = self.controlador.obtener_tipo_unidades()
        
            
        for index, tipo_unidad in enumerate(tipo_unidades):
            estado_text = "ACTIVO" if tipo_unidad.estado_tipo_unidad else "INACTIVO"
            estado_text_color = None if tipo_unidad.estado_tipo_unidad else ft.Colors.WHITE
            estado_bgcolor = None if tipo_unidad.estado_tipo_unidad else ft.Colors.RED_400
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(tipo_unidad.nombre_tipo_unidad)),
                        ft.DataCell(ft.Container(
                            content=ft.Text(
                                estado_text,
                                color=estado_text_color          
                            ),
                            bgcolor=estado_bgcolor,
                            padding=ft.padding.all(5)
                        )),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.TextButton("Editar", on_click=lambda e, tipo_unidad=tipo_unidad: self.abrir_modal_editar(e, tipo_unidad)),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    ]
                )
            )
            self.page.update()
            
    def guardar_tipo_unidad(self, e):
        """ Guardar un nuevo tipo de unidad"""
        if not self.insert_nombre_tipo_unidad.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        datos_tipo_unidades = {
            "nombre_tipo_unidad": self.insert_nombre_tipo_unidad.value.upper(),
            "estado_tipo_unidad": self.estado_tipo_unidad.value
        }
        try:
            self.controlador.guardar_tipo_unidad(datos_tipo_unidades)
            self.cargar_datos()
            self.insert_nombre_tipo_unidad.value = ""
            self.estado_tipo_unidad.value = True
            self.mostrar_mensaje("Tipo de unidad guardado correctamente")
           
        except Exception as e:
            # Handle any errors 
            self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)
            
    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet."""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.Colors.RED if es_error else ft.Colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
    
    def abrir_modal_editar(self, e, tipo_unidad):
        """Abrir modal para editar el tipo de unidad"""
        self.tipo_unidad_seleccionada = tipo_unidad
        
        
        self.modal_nombre_unidad = ft.TextField(
            label="Tipo de unidad",
            value=tipo_unidad.nombre_tipo_unidad  # Pre-select current type
        )
        self.modal_estado_unidad = ft.Checkbox(
            label="Activo",
            value=tipo_unidad.estado_tipo_unidad  # Set current state
        )
        self.modal_edit = ft.AlertDialog(
            title = ft.Text("Editar tipo unidad", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=[
                    self.modal_nombre_unidad,
                    self.modal_estado_unidad
                ],
                width=300,
                spacing=10,
                height=200
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                ft.ElevatedButton("Actualizar", on_click=self.actualizar_tipo_unidad)
            ]
        )
        
        self.page.overlay.append(self.modal_edit)
        self.modal_edit.open = True
        self.page.update()
        
    def cerrar_modal(self, e=None):
        """Close the edit modal"""
        if self.modal_edit:
            self.modal_edit.open = False
            self.page.update()
    
    def actualizar_tipo_unidad(self, e):
        datos_actualizados = {
            "nombre_tipo_unidad" : self.modal_nombre_unidad.value.upper(),
            "estado_tipo_unidad" : self.modal_estado_unidad.value
        }
        
        try:
            tipo_unidad_actualizada = self.controlador.actualizar_tipo_unidad(self.tipo_unidad_seleccionada.id_tipo_unidad, datos_actualizados)

            if tipo_unidad_actualizada:
                self.cargar_datos()
                self.cerrar_modal()
                self.mostrar_mensaje("Tipo unidad actualizada correctamente")
                
        except ValueError as error:
            # Handle validation errors
            self.mostrar_mensaje(str(error), es_error=True)