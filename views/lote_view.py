# minas_view.py
import flet as ft
from controllers.control_cliente import ControlCliente
from controllers.control_lote import ControlLote
from controllers.control_minas import ControlMina

class LoteView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador_lote = ControlLote()
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        
        self.filtro_lotes = ft.TextField(
            label="Filtrar lotes",
            expand=True, 
            on_change=self.filtrar_lotes
        )
        
        self.lote_seleccionado = None
        page.title = "Lotes"
        # Navigation button
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.modal_open = False
        self.modal_edit = None
        
        # Input fields
        self.insert_lote = ft.TextField(label="Lote", expand=True, bgcolor="white")
        self.insert_cliente = ft.Dropdown(
            label="Cliente", 
            options=[
                ft.dropdown.Option(key=cliente.id_cliente, text=cliente.nombre_cliente) 
                for cliente in self.controlador_cliente.obtener_clientes()
                if cliente.estado
            ],
            on_change=self.actualizar_minas
        )
        self.insert_mina = ft.Dropdown(label="Mina")
        self.insert_contrato = ft.TextField(label="No. Contrato", expand=True)
        self.insert_booking = ft.TextField(label="Booking", expand=True)
        # Active status checkbox
        # self.estado_lote = ft.Checkbox(label="Activo", value=True)
        # Edit lote
        self.lote_seleccionado = None
        self.modal_lote = ft.TextField(label="Lote")
        self.modal_cliente = ft.TextField(label="Cliente")
        self.modal_mina = ft.TextField(label="Mina")
        # self.modal_estado = ft.Checkbox(label="Activo", value=True)
        self.modal_contrato = ft.TextField(label="No. Contrato")
        self.modal_booking = ft.TextField(label="Booking")
        # Save button with custom click handler
        self.button_save = ft.ElevatedButton(
            text="Guardar lote",
            on_click=self.guardar_lote
        )
        self.data_table = ft.DataTable(
            width=float('inf'),
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("Lote"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Cliente"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Mina"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("No. Contrato"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Booking"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Acciones"), heading_row_alignment=ft.MainAxisAlignment.CENTER)
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
            
        )
        
        self.tabla_scrollable = ft.Container(
            content=ft.Column(
                controls=[self.data_table],
                scroll=ft.ScrollMode.AUTO,
            ),
            height=500,

        )
        # Main content layout
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo lote", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.insert_lote,
                    self.insert_cliente,
                    self.insert_mina
                    ]),
                ft.Row([
                    self.insert_contrato,
                    self.insert_booking
                ]),
                self.button_save,
                ft.Row([
                   self.filtro_lotes 
                ],
                    width=300,
                    spacing=10),
                ft.Column(
                    controls=[
                        self.tabla_scrollable
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,

                )
            ],
        )
        self.cargar_lotes()
    
    def filtrar_lotes(self, e):
        """Filtra los lotes basado en el texto de búsqueda"""
        filtro = self.filtro_lotes.value.lower()
        lotes = self.controlador_lote.obtener_lotes()
        
        # Filter lotes based on multiple fields
        lotes_filtrados = [
            lote for lote in lotes 
            if (filtro in str(lote.id_lote).lower() or 
                filtro in lote.nombre_lote.lower() or 
                filtro in str(lote.id_cliente).lower() or 
                filtro in str(lote.id_mina).lower() or 
                filtro in str(lote.no_contrato or '').lower() or 
                filtro in str(lote.booking or '').lower())
        ]
        
        # Rebuild table with filtered results
        self.data_table.rows = []
        
        for lote in lotes_filtrados:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(lote.id_lote))),
                        ft.DataCell(ft.Text(lote.nombre_lote)),
                        ft.DataCell(ft.Text(lote.id_cliente)),
                        ft.DataCell(ft.Text(lote.id_mina or '')),
                        ft.DataCell(ft.Text(lote.no_contrato or '')),
                        ft.DataCell(ft.Text(lote.booking or '')),
                        ft.DataCell(
                            ft.Row([
                                ft.TextButton("Editar", on_click=lambda e, current_lote=lote: self.abrir_modal_editar(e, current_lote)),
                            ],
                            )
                        )
                    ]
                )
            )
        self.page.update()
        
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

    def actualizar_minas(self, e):
        """Al seleccionar un cliente me trae sus minas """
        cliente_seleccionado = self.insert_cliente.value
        self.insert_mina.options = []
        
        # Obtain all minas and clients
        minas = self.controlador_mina.obtener_minas()
        clientes = self.controlador_cliente.obtener_clientes()
        
        # Find the selected client by ID or name
        cliente_actual = None
        for cliente in clientes:
            if str(cliente.id_cliente) == cliente_seleccionado or cliente.nombre_cliente == cliente_seleccionado:
                cliente_actual = cliente
                break
        
        if cliente_actual:
            # Filter minas for this specific client
            minas_cliente = [mina for mina in minas if mina.id_cliente == cliente_actual.id_cliente]
            
            if minas_cliente: 
                self.insert_mina.options = [
                    ft.dropdown.Option(key=mina.id_mina, text=mina.nombre_mina) for mina in minas_cliente
                    if mina.estado 
                ]
            else:
                print(f"No minas found for client name: {cliente_actual.nombre_cliente}")
        else:
            print(f"Client not found: {cliente_seleccionado}")
        
        self.page.update()
        
    
    def guardar_lote(self, _):
        """Guardar lote"""
        if not self.insert_lote.value or not self.insert_cliente.value or not self.insert_mina.value:
            self.mostrar_mensaje("Por favor, complete todos los campos", es_error=True)
            return
        datos_lote = {
            'nombre_lote': self.insert_lote.value.upper(),
            'id_cliente': self.insert_cliente.value,
            'id_mina': self.insert_mina.value if self.insert_mina.value else None,
            'no_contrato': self.insert_contrato.value if self.insert_contrato.value else None,
            'booking': self.insert_booking.value if self.insert_booking.value else None
        }

        try:
            self.controlador_lote.crear_lote(datos_lote)
            self.mostrar_mensaje("Lote creado exitosamente")
            
            self.insert_lote.value = ""
            self.insert_cliente.value = ""
            self.insert_mina.value = ""
            self.insert_contrato.value = ""
            self.insert_booking.value = ""
            self.cargar_lotes()
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)
    
    def cargar_prefijo(self):
        clientes = self.controlador_cliente.obtener_clientes()
        prefijo = [cliente.prefijo_cliente for cliente in clientes if cliente.nombre_cliente == self.insert_cliente.value]
        print(prefijo[0])   
    
    
    def cargar_lotes(self):
        """Carga los lotes en la tabla."""
        lotes = self.controlador_lote.obtener_lotes()

        # Limpiar filas existentes
        self.data_table.rows.clear()

        # Poblar la tabla con datos de los lotes
        for lote in lotes:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(lote.id_lote))),
                        ft.DataCell(ft.Text(lote.nombre_lote)),
                        ft.DataCell(ft.Text(lote.id_cliente)),
                        ft.DataCell(ft.Text(lote.id_mina or '')),
                        ft.DataCell(ft.Text(lote.no_contrato or '')),
                        ft.DataCell(ft.Text(lote.booking or '')),
                        ft.DataCell(
                            ft.Row([
                                ft.TextButton("Editar", on_click=lambda e, current_lote=lote: self.abrir_modal_editar(e, current_lote)),
                            ])
                        )
                    ]
                )
            )
        self.page.update()
        
    def abrir_modal_editar(self, e, lote):
        """Open modal to edit a specific lote"""
        self.lote_seleccionado = lote
        
        # Prepare client dropdown options
        cliente_options = [
            ft.dropdown.Option(key=str(cliente.nombre_cliente), text=cliente.nombre_cliente) 
            for cliente in self.controlador_cliente.obtener_clientes()
            if cliente.estado
        ]
        
        # Create modal content with editable fields
        self.modal_edit = ft.AlertDialog(
            title=ft.Text("Editar Lote", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label="Lote",
                        value=lote.nombre_lote,
                        expand=True
                    ),
                    ft.Dropdown(
                        label="Cliente", 
                        options=cliente_options,
                        value=lote.id_cliente,
                        on_change=self.actualizar_minas_modal
                    ),
                    ft.Dropdown(
                        label="Mina",
                        options=[],  # Will be populated dynamically
                        value=lote.id_mina
                    ),
                    ft.TextField(
                        label="No. Contrato",
                        value=lote.no_contrato or "",
                        expand=True
                    ),
                    ft.TextField(
                        label="Booking",
                        value=lote.booking or "",
                        expand=True
                    )
                ],
                width=500,
                spacing=10,
                height=300
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                ft.ElevatedButton("Actualizar", on_click=self.actualizar_lote_seleccionado)
            ]
        )
        
        # Populate minas dropdown based on selected client
        self.actualizar_minas_modal(None)
        
        # Open the modal
        self.page.dialog = self.modal_edit
        self.modal_edit.open = True
        self.page.update()
        
    def actualizar_minas_modal(self, e):
        """Update minas dropdown in edit modal based on selected client"""
        # Get the currently selected client in the modal
        cliente_seleccionado = self.modal_edit.content.controls[1].value
        
        # Find minas for the selected client
        minas = self.controlador_mina.obtener_minas()
        minas_cliente = [
            ft.dropdown.Option(key=mina.nombre_mina, text=mina.nombre_mina) 
            for mina in minas 
            if mina.id_cliente == cliente_seleccionado and mina.estado
        ]
        
        # Update the minas dropdown
        self.modal_edit.content.controls[2].options = minas_cliente
        self.page.update()

    def actualizar_lote_seleccionado(self, e):
        """Update the selected lote with new information"""
        # Get values from modal fields
        campos_modal = self.modal_edit.content.controls
        
        datos_actualizados = {
            'nombre_lote': campos_modal[0].value.upper(),
            'id_cliente': campos_modal[1].value,
            'id_mina': campos_modal[2].value,
            'no_contrato': campos_modal[3].value or None,
            'booking': campos_modal[4].value or None
        }

        try:
            # Update the lote using the controller
            self.controlador_lote.actualizar_lote(self.lote_seleccionado.id_lote, datos_actualizados)
            
            # Show success message
            self.mostrar_mensaje("Lote actualizado exitosamente")
            
            # Close modal and refresh lotes
            self.cerrar_modal(e)
            self.cargar_lotes()
        except Exception as e:
            # Show error message if update fails
            self.mostrar_mensaje(f"Error al actualizar lote: {str(e)}", es_error=True)

    def cerrar_modal(self, e=None):
        """Close the edit modal"""
        if self.modal_edit:
            self.modal_edit.open = False
            self.page.update()