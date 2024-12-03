import flet as ft
from controllers.control_tipo_producto import ControlTipoProducto

class TipoProductoView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlTipoProducto()
        page.title = "Tipo de productos"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.producto_seleccionado = None
        
        # New product input fields
        self.nombre_tipo_producto = ft.TextField(label="Producto", expand=True)
        self.estado_tipo_producto = ft.Checkbox(label="Activo", value=True)
        
        # Modal edit product fields
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        
        # Save button
        self.button_save = ft.ElevatedButton(
            text="Guardar tipo producto",
            on_click=self.guardar_tipo_producto
        )
        
        # Data table for products
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
                ft.Text("Nuevo producto", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_tipo_producto,
                self.estado_tipo_producto,
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
        
        # Load existing products
        self.cargar_tipo_productos()
    
    def cargar_tipo_productos(self):
        """Cargar la lista de productos en la tabla"""
        self.data_table.rows = []
        for index, tipo_producto in enumerate(self.controlador.obtener_tipo_productos()):
            estado_text = "ACTIVO" if tipo_producto.estado_tipo_producto else "INACTIVO"
            estado_text_color = None if tipo_producto.estado_tipo_producto else ft.colors.WHITE
            estado_bgcolor = None if tipo_producto.estado_tipo_producto else ft.colors.RED_400
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(tipo_producto.nombre_tipo_producto)),
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
                                ft.TextButton("Editar", on_click=lambda e, producto=tipo_producto: self.abrir_modal_editar(e, producto)),
                            ])
                        )
                    ]
                )
            )
    
    def guardar_tipo_producto(self, _):
        """Guardar un nuevo producto"""
        if not self.nombre_tipo_producto.value:
            self.mostrar_mensaje("El nombre del tipo producto es requerido.", es_error=True)
            return
        
        datos_producto = {
            "nombre_tipo_producto": self.nombre_tipo_producto.value.upper(),
            "estado_tipo_producto": self.estado_tipo_producto.value
        }
        
        try:
            self.controlador.crear_producto(datos_producto)
            self.cargar_tipo_productos()
            self.nombre_tipo_producto.value = ""
            self.estado_tipo_producto.value = True
            
            self.mostrar_mensaje("Tipo producto guardado correctamente.")
        
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar el tipo producto: {str(e)}", es_error=True)
    
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
        
    def abrir_modal_editar(self, e, tipo_producto):
        """Abrir modal para editar un producto"""
        self.tipo_producto_seleccionado = tipo_producto
        
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
                        ft.Text("Editar tipo producto", size=20, weight=ft.FontWeight.BOLD),
                        self.modal_nombre,
                        self.modal_estado,
                        ft.Row(
                            controls=[
                                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                                ft.TextButton("Actualizar", on_click=self.actualizar_tipo_producto),
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
        
        self.modal_nombre.value = tipo_producto.nombre_tipo_producto
        self.modal_estado.value = tipo_producto.estado_tipo_producto
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
        
    def actualizar_tipo_producto(self, e):
        """Actualizar un producto existente"""
        if not self.modal_nombre.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        # Preparar datos actualizados
        datos_actualizados = {
            "nombre_tipo_producto": self.modal_nombre.value.upper(),
            "estado_tipo_producto": self.modal_estado.value
        }

        try:
            # Usar el controlador para actualizar el producto
            producto_actualizado = self.controlador.actualizar_tipo_producto(self.tipo_producto_seleccionado.id_tipo_producto, datos_actualizados)
            
            if producto_actualizado:
                # Recargar la tabla de productos
                self.cargar_tipo_productos()
                
                # Cerrar el modal
                self.cerrar_modal()
                
                # Mostrar mensaje de éxito
                self.mostrar_mensaje("Tipo producto actualizado exitosamente")
            
        except ValueError as error:
            # Manejar errores de validación
            self.mostrar_mensaje(str(error), es_error=True)