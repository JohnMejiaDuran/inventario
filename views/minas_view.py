import flet as ft
from controllers.control_minas import ControlMina
from controllers.control_cliente import ControlCliente

class MinasView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador_mina = ControlMina()
        self.controlador_cliente = ControlCliente()
        page.title = "Minas"
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        self.mina_seleccionada = None
        self.insert_mina = ft.TextField(label="Mina", expand=True)
        self.cliente = ft.Dropdown(
            label="Cliente",
            options=[
                ft.dropdown.Option(cliente.nombre_cliente)
                for cliente in self.controlador_cliente.obtener_clientes()
                if cliente.estado
            ],
            expand=True
        )
        self.estado_mina = ft.Checkbox(label="Activo", value=True)
        self.lote_seleccionado = None
        
        #Modal edit mina
        self.modal_mina = ft.TextField(label="Mina")
        self.modal_cliente = ft.Dropdown(
            label="Cliente",
            options=[
                ft.dropdown.Option(cliente.nombre_cliente)
                for cliente in self.controlador_cliente.obtener_clientes()
            ],
            ),
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        self.button_save = ft.ElevatedButton(
            text="Guardar mina",
            on_click=self.guardar_mina
        )
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Mina")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nueva mina", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.insert_mina, self.cliente]),
                self.estado_mina,
                self.button_save,
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Minas", size=20, weight=ft.FontWeight.BOLD)
                            ]
                        ),
                        self.data_table
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                )
            ]
        )
        self.cargar_minas()
        
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
    
    def cargar_minas(self):
        minas = self.controlador_mina.obtener_minas()
        
        self.data_table.rows.clear()
        
        for mina in minas:
            estado_text = "ACTIVO" if mina.estado else "INACTIVO"
            estado_text_color = None if mina.estado else ft.colors.WHITE
            estado_bgcolor = None if mina.estado else ft.colors.RED_400
            edit_button = ft.TextButton(
                text="Editar",
                on_click=lambda _, mina=mina: self.abrir_modal_editar(_, mina)
            )
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(mina.id_mina))),
                    ft.DataCell(ft.Text(mina.nombre_mina)),
                    ft.DataCell(ft.Text(mina.id_cliente)),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                estado_text,
                                color=estado_text_color
                            ),
                            bgcolor=estado_bgcolor,
                            padding=ft.padding.all(5)
                        )),
                        ft.DataCell(edit_button)
                        ]
                    )
            self.data_table.rows.append(row)
            
        self.page.update()
        
    def guardar_mina(self, e):
        if not self.insert_mina.value or not self.cliente.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        
        datos_mina = {
            "nombre_mina" : self.insert_mina.value.upper(),
            "id_cliente" : self.cliente.value,
            "estado" : self.estado_mina.value
        }
        
        try: 
            self.controlador_mina.crear_mina(datos_mina)
            self.mostrar_mensaje("Mina creada exitosamente")
            self.cargar_minas()
            
            self.insert_mina.value = ""
            self.cliente.value = ""
            self.estado_mina.value = True
            
            self.mostrar_mensaje("Mina guardada exitosamente")
            
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)
    
    def abrir_modal_editar(self, e, mina):
        self.mina_seleccionada = mina
        
        # Preparar las opciones del dropdown de clientes
        cliente_options = [
            ft.dropdown.Option(key=str(cliente.nombre_cliente))
            for cliente in self.controlador_cliente.obtener_clientes()
            if cliente.estado
        ]
        
        # Actualizar el dropdown de clientes para reflejar las opciones
        self.modal_cliente = ft.Dropdown(
            label="Cliente",
            options=cliente_options,
            value=str(mina.id_cliente) if mina.id_cliente else "Cliente inactivo"  # Establecer el cliente actual como valor seleccionado
        )
        
        self.modal_edit = ft.Container(
            expand=True,
            bgcolor=ft.colors.BLACK45,
            content=ft.Container(
                width=500,
                height=300,
                bgcolor=ft.colors.WHITE,
                content=ft.Column(
                    controls=[
                        ft.Text("Editar mina", size=20, weight=ft.FontWeight.BOLD),
                        self.modal_mina,
                        self.modal_cliente,
                        self.modal_estado,
                        ft.Row([
                            ft.TextButton("Actualizar", on_click=self.actualizar_mina_seleccionada),
                            ft.TextButton("Cancelar", on_click=self.cerrar_modal)
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                )
            ),
            alignment=ft.alignment.center
        )
        
        self.modal_mina.value = mina.nombre_mina
        self.modal_estado.value = mina.estado
        self.page.overlay.append(self.modal_edit)
        self.modal_edit.open = True
        self.page.update()

    def actualizar_mina_seleccionada(self, e):
        # Get updated values from inputs
        nombre_mina = self.modal_mina.value
        estado = self.modal_estado.value
        id_cliente = self.modal_cliente.value

        if not nombre_mina or not id_cliente:
            self.mostrar_mensaje("Por favor, complete todos los campos.", es_error=True)
            return
        datos_actualizados = {
            "nombre_mina": nombre_mina.upper(),
            "estado": estado,
            "id_cliente": id_cliente
        }

        try:
            # Update the mine record using your controller
            self.controlador_mina.actualizar_mina(self.mina_seleccionada.id_mina, datos_actualizados)
            self.mostrar_mensaje("Mina actualizada exitosamente.")
            self.modal_edit.open = False
            self.cerrar_modal()
            self.cargar_minas()
            self.page.update()
        except Exception as e:
            self.mostrar_mensaje(f"Error al actualizar la mina: {e}", es_error=True)
   
        
    def cerrar_modal (self, e=None):
        """Close the edit modal."""
        self.modal_open = False

        # Cerrar y remover el modal del overlay
        if self.modal_edit and self.modal_edit in self.page.overlay:
            self.page.overlay.remove(self.modal_edit)
            self.modal_edit = None  # Limpiar la referencia

        self.page.update()
        print("Modal de edición cerrado.")  # Debug