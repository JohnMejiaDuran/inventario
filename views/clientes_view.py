import flet as ft
from controllers.control_cliente import ControlCliente

class ClientesView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador = ControlCliente()
        
        # Navigation button
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        
        # Input fields
        self.insert_cliente = ft.TextField(label="Cliente", expand=True)
        self.insert_nit = ft.TextField(label="Nit", expand=True)
        
        # Active status checkbox
        self.estado_cliente = ft.Checkbox(label="Activo", value=True)
        
        #edit button
        self.edit_button = ft.IconButton(
            ft.icons.EDIT_OUTLINED,
            
        )
        
        
        # Save button with custom click handler
        self.button_save = ft.ElevatedButton(
            text="Guardar cliente",
            on_click=self.guardar_cliente
        )
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Nit")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )
        # Main content layout
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo cliente", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.insert_cliente, self.insert_nit]),
                self.estado_cliente,
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
        self.cargar_clientes()
    
    def ir_atras(self, e):
        """Maneja el evento de clic en el botón 'Atrás'."""
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
    
    
    def cargar_clientes(self):
        """Carga los clientes en la tabla."""
        clientes = self.controlador.obtener_clientes()
        
        # Clear existing rows
        self.data_table.rows.clear()
        
        # Populate table with client data
        for cliente in clientes:
            estado_text = "Activo" if cliente.estado else "Inactivo"
            estado_text_color = None if cliente.estado else ft.colors.WHITE
            estado_bgcolor = None if cliente.estado else ft.colors.RED_400
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente.id))),
                    ft.DataCell(ft.Text(cliente.nombre_cliente)),
                    ft.DataCell(ft.Text(cliente.nit)),
                    ft.DataCell(ft.Container(
                        content=ft.Text(
                            estado_text,
                            color=estado_text_color          
                        ),
                        bgcolor=estado_bgcolor,
                        padding=ft.padding.all(5)
                    )),
                    ft.DataCell(self.edit_button)
                ]
            )
            self.data_table.rows.append(row)
        
        # Update the page to reflect changes
        self.page.update()
    
    def guardar_cliente(self, e):
        """Guarda un nuevo cliente con los datos ingresados."""
        # Validate inputs
        if not self.insert_cliente.value or not self.insert_nit.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        # Prepare client data
        datos_cliente = {
            "nombre_cliente": self.insert_cliente.value,
            "nit": self.insert_nit.value,
            "estado": self.estado_cliente.value
        }
        
        try:
            # Attempt to create the client
            self.controlador.crear_cliente(datos_cliente)
            self.cargar_clientes()
            # Clear input fields after successful save
            self.insert_cliente.value = ""
            self.insert_nit.value = ""
            self.estado_cliente.value = True
            
            # Show success message
            self.mostrar_mensaje("Cliente guardado exitosamente")

        except Exception as e:
            # Handle any errors 
            self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)

