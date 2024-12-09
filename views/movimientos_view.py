import flet as ft
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from controllers.control_transportadores import ControlTransportador
from controllers.control_productos import ControlProducto
from controllers.control_tipo_producto import  ControlTipoProducto
from controllers.control_bodegas import ControlBodega
from controllers.control_tipo_unidad import ControlTipoUnidad
import datetime
from controllers.control_movimiento import ControlMovimientos

class MovimientoView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        self.controlador_lotes = ControlLote()
        self.controlador_transportador = ControlTransportador()
        self.controlador_producto = ControlProducto()
        self.controlador_tipo_producto = ControlTipoProducto()
        self.controlador_bodegas = ControlBodega()
        self.controlador_movimientos = ControlMovimientos()
        self.controlador_tipo_unidad = ControlTipoUnidad()
        self.nombre_movimiento = ft.Text("Nuevo Movimiento")
        self.insert_cliente = ft.Dropdown(
            label="Selecciona un cliente",
            options=[
                ft.dropdown.Option(key=cliente.id_cliente, text=cliente.nombre_cliente)
                for cliente in self.controlador_cliente.obtener_clientes()
                if cliente.estado
            ],
                on_change=self.actualizar_minas,
                expand=True
            )
        
        self.insert_mina = ft.Dropdown(
            label="Selecciona una mina",
            on_change=self.actualizar_lotes,
            expand=True
            )
        
        self.insert_lote = ft.Dropdown(label="Selecciona un lote",expand=True)
        self.insert_placa_contenedor = ft.TextField(label="Placa o contenedor",expand=True, on_change=self.convertir_mayuscula)
        self.insert_tipo_vehiculo = ft.Dropdown(
            label="Selecciona tipo de vehiculo",
            options=[
                ft.dropdown.Option("PLANCHA"),
                ft.dropdown.Option("VOLCO"),
                ft.dropdown.Option("MULA")
            ]
            ,expand=True)
        self.insert_transportador = ft.Dropdown(
            label="Selecciona un transportador",
            max_menu_height=200,
            options=[
                ft.dropdown.Option(transportador.nombre_transportador)
                for transportador in self.controlador_transportador.obtener_transportadores()
                if transportador.estado_transportador
            ],
            expand=True)
        
        self.insert_producto = ft.Dropdown(
            label="Selecciona un producto",
            options=[
                ft.dropdown.Option(producto.nombre_producto)
                for producto in self.controlador_producto.obtener_productos()
                if producto.estado_producto
            ],
            expand=True)
        self.insert_tipo_producto = ft.Dropdown(
            label="Selecciona tipo de producto",
            options=[
                ft.dropdown.Option(tipo_producto.nombre_tipo_producto)
                for tipo_producto in self.controlador_tipo_producto.obtener_tipo_productos()
                if tipo_producto.estado_tipo_producto
                ],
            expand=True)
        self.insert_imo = ft.Dropdown(
            label="Seleccione IMO",
            options=[
                ft.dropdown.Option("3"),
                ft.dropdown.Option("9"),
            ],
            expand=True
        )
        
        self.insert_tipo_unidad = ft.Dropdown(
            label="Seleccione tipo de unidad",
            options=[
                ft.dropdown.Option(key=tipo_unidad.nombre_tipo_unidad, text=tipo_unidad.nombre_tipo_unidad)
                for tipo_unidad in self.controlador_tipo_unidad.obtener_tipo_unidades()
                if tipo_unidad.estado_tipo_unidad
            ],
            expand=True
        )
        self.insert_unidades_anuncio = ft.TextField(label="Unidades anunciadas", expand=True)
        self.insert_peso_anuncio = ft.TextField(label="Peso anunciado", expand=True)
        self.insert_categoria = ft.Dropdown(label="Seleccione categoría", options=[
            ft.dropdown.Option("EXPORTACIÓN"),
            ft.dropdown.Option("NACIONAL"),
            ft.dropdown.Option("NACIONALIZADA"),
            ft.dropdown.Option("SIN NACIONALIZAR"),
        ],
            expand=True
                                            )
        self.insert_ubicacion = ft.Dropdown(
            label="Seleccione ubicación",
            options=[
                ft.dropdown.Option(bodega.nombre_bodega)
                for bodega in self.controlador_bodegas.obtener_bodegas()
                if bodega.estado_bodega
            ],
            expand=True
        )
        self.insert_unidades = ft.TextField(label="Ingresa unidades", expand=True)
        self.insert_neto_bascula = ft.TextField(label="Ingrese Neto Báscula", expand=True)
        
        self.insert_para = ft.TextField(label="Ingrese Para", value=0, expand=True)
        self.insert_observaciones = ft.TextField(label="Observaciones", expand=True)
        # Button to open modal
        self.nuevo_movimiento_btn = ft.ElevatedButton(
            text="Nuevo Movimiento",
            on_click=self.abrir_modal_movimiento
        )
        
        # Dropdown para tipo de movimiento
        self.tipo_movimiento = ft.Dropdown(
            label="Tipo de Movimiento",
            options=[
                ft.dropdown.Option("INGRESO TERRESTRE"),
                ft.dropdown.Option("INGRESO FLUVIAL"),
                ft.dropdown.Option("INGRESO VACIADO"),
                ft.dropdown.Option("SALIDA LLENADO"),
                ft.dropdown.Option("SALIDA TERRESTRE"),
                ft.dropdown.Option("SALIDA FLUVIAL")
            ],
            on_change=self.cambiar_tipo_movimiento,
            expand=True
        )
        self.insert_fecha = ft.DatePicker(
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31),
            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR,
            on_change=self.on_fecha_change
        )
        self.page.overlay.append(self.insert_fecha)
        
        self.fecha_display = ft.TextField(
            label="Fecha",
            read_only=True,
            expand=True
        )
        
        self.insert_hora = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=self.on_hora_change
        )
        self.insert_hora_fin = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=self.on_hora_fin_change
        )
        self.page.overlay.append(self.insert_hora)
        self.page.overlay.append(self.insert_hora_fin)
        self.hora_inicio = ft.TextField(
            label="Hora inicio",
            read_only=True,
            expand=True)
        self.hora_fin = ft.TextField(
            label="Hora fin",
            read_only=True,
            expand=True)
        
        self.hora_button = ft.IconButton(
            icon=ft.Icons.ACCESS_TIME,
            on_click=lambda _: self.insert_hora.pick_time()
        )
        self.hora_fin_button = ft.IconButton(
            icon=ft.Icons.ACCESS_TIME,
            on_click=lambda _: self.insert_hora_fin.pick_time()
        )
        self.stack_hora = ft.Stack([
            
            self.hora_inicio,
            ft.Container(
            content=self.hora_button,
            alignment=ft.alignment.center_right,
            padding=ft.padding.only(right=3, top=5)
            )
        ], expand=True)
        self.stack_hora_fin = ft.Stack([
            self.hora_fin,
            ft.Container(
            content=self.hora_fin_button,
            alignment=ft.alignment.center_right,
            padding=ft.padding.only(right=3, top=5)
            )
        ], expand=True)
        self.fecha_button = ft.IconButton(
            icon=ft.Icons.EVENT,
            on_click=lambda _: self.insert_fecha.pick_date()
        )
        self.stack_fecha = ft.Stack([
            self.fecha_display,
            ft.Container(
            content=self.fecha_button,
            alignment=ft.alignment.center_right,
            padding=ft.padding.only(right=3, top=5)
        )
        ],expand=True)
        # Form containers
        self.container_ingreso_terrestre = ft.Container(
            visible=False,
            
            content=ft.Column([
                ft.Text("Información cliente"),
                ft.Row([
                        self.insert_cliente,
                        self.insert_mina,
                        self.insert_lote
                    ]),
                ft.Text("Anuncio de carga"),
                ft.Row([
                    self.insert_placa_contenedor,
                    self.insert_tipo_vehiculo,
                    self.insert_transportador
                ]),
                ft.Row([
                    self.insert_producto,
                    self.insert_tipo_producto,
                    self.insert_imo
                ]),
                ft.Row([
                    self.insert_tipo_unidad,
                    self.insert_unidades_anuncio,
                    self.insert_peso_anuncio
                ]),
                ft.Text("Movimiento"),
                ft.Row([
                    self.insert_categoria,
                    self.insert_ubicacion,
                    self.insert_unidades,
                    self.insert_neto_bascula
                ]),
                ft.Row([
                    self.stack_fecha,
                    self.stack_hora,
                    self.stack_hora_fin,
                    self.insert_para
                ]),
                ft.Row([
                    self.insert_observaciones
                ])
            ]))
        
        
        # DATA TABLE MOVIMIENTOS
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("No. SERVICIO",text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO \n MOVIMIENTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CATEGORÍA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("UBICACIÓN", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("UNIDADES", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NETO \n BÁSCULA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("HORA \n INICIO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("HORA \n FIN", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("ACCIONES", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
            column_spacing=20
            
        )
        # Main content layout
        self.content = ft.Column(
            controls=[
                ft.Row([
                    ft.TextButton("Inicio", on_click=lambda e: page.go("/")),
                ]),
                self.nuevo_movimiento_btn,
                ft.Column([
                    self.data_table
                ])
            ]
        )
        
        self.cargar_movimientos()
    
    def on_fecha_change(self, e):
        """Handle date selection"""
        selected_date = e.control.value
        if selected_date:
            # Format date as string for display
            formatted_date = selected_date.strftime("%d/%m/%Y")
            self.fecha_display.value = formatted_date
            self.page.update()
            
    def on_hora_change(self, e):
        """Handle time selection"""
        selected_time = e.control.value
        if selected_time:
            # Format time as string for display
            formatted_time = selected_time.strftime("%H:%M")
            self.hora_inicio.value = formatted_time
            self.page.update()
    
    def on_hora_fin_change(self, e):
        """Handle time selection"""
        selected_time = e.control.value
        if selected_time:
            # Format time as string for display
            formatted_time = selected_time.strftime("%H:%M")
            self.hora_fin.value = formatted_time
            self.page.update()
            
    def convertir_mayuscula(self, e):
        """Convert text to uppercase as user types"""
        if e.data:  # Check if there's input data
            self.insert_placa_contenedor.value = e.data.upper()
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

        
    def actualizar_lotes(self, e):
        """Al seleccionar la mina del cliente me trae sus lotes"""
        mina_seleccionada = self.insert_mina.value
        self.insert_lote.options = []
        
        # Obtain lotes for the selected mine
        lotes = self.controlador_lotes.obtener_lotes()
        clientes = self.controlador_cliente.obtener_clientes
        # Find the selected mine
        minas = self.controlador_mina.obtener_minas()
        mina_actual = next((mina for mina in minas if str(mina.id_mina) == mina_seleccionada or mina.nombre_mina == mina_seleccionada), None)
        cliente_actual = next((lote for lote in lotes if str(lote.id_cliente) == mina_seleccionada or lote.nombre_cliente == mina_seleccionada), None)
        if mina_actual:
            # Filter lotes for this specific mine
            lotes_mina = [lote for lote in lotes if lote.id_mina == mina_actual.id_mina]
            lotes_cliente = [lote for lote in lotes if lote.id_cliente == cliente_actual.id_cliente]
            if lotes_mina:
                self.insert_lote.options = [
                    ft.dropdown.Option(key=lote.id_lote, text=lote.nombre_lote) 
                    for lote in lotes_mina
                ]
            else:
                self.insert_lote.options = [
                    ft.dropdown.Option(key=lote.id_lote, text=lote.nombre_lote) 
                    for lote in lotes_cliente
                ]
        else:
            print(f"Mine not found: {mina_seleccionada}")
        
        self.page.update()
        
            
    
    def abrir_modal_movimiento(self, e ):
        modal = ft.AlertDialog(
            title=self.nombre_movimiento,
            content=ft.Column(
                controls=[
                    self.tipo_movimiento,
                    self.container_ingreso_terrestre,
                    # Add other containers here
                ],
                height=600,
                width=800,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                ft.ElevatedButton("Guardar", on_click=self.guardar_movimiento_in_terrestre)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = modal
        modal.open = True
        self.page.update()
    
    def cerrar_modal(self, e):
        self.page.dialog.open = False
        self.page.update()
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet."""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.RED if es_error else ft.colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
    
    def guardar_movimiento_in_terrestre(self, e):
        # Ensure fecha_obj is a datetime.date object
        fecha_obj = self.insert_fecha.value  # Assuming this is already a date object
        lote_seleccionado = next(
            (lote.nombre_lote for lote in self.controlador_lotes.obtener_lotes() 
            if str(lote.id_lote) == self.insert_lote.value),
            self.insert_lote.value  # fallback to the value itself if not found
        )
        # Combine date and time to create datetime.datetime objects
        hora_inicio = datetime.datetime.combine(fecha_obj, self.insert_hora.value)
        hora_fin = datetime.datetime.combine(fecha_obj, self.insert_hora_fin.value)

        # Calculate tiempo_op
        tiempo_operativo = (hora_fin - hora_inicio).total_seconds() / 3600 - float(self.insert_para.value)

        tiempo_operativo_rounded = round(tiempo_operativo, 2)
        
        prefijo = self.controlador_cliente.obtener_prefijo_cliente(self.insert_cliente.value)
        no_servicio = f"{prefijo}-{self.insert_producto.value}-{lote_seleccionado}"
        # Create a dictionary with the data
        datos = {
            "tipo_movimiento": self.tipo_movimiento.value,
            "unidades": self.insert_unidades.value,
            "neto_bascula": self.insert_neto_bascula.value,
            "fecha": fecha_obj,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "para": self.insert_para.value,
            "tiempo_op": tiempo_operativo_rounded,
            "observaciones": self.insert_observaciones.value,
            "ubicacion": self.insert_ubicacion.value,
            "categoria": self.insert_categoria.value,
            "id_lote": self.insert_lote.value,
            "no_servicio": no_servicio
        }
        print(tiempo_operativo_rounded)
        try:
            self.controlador_movimientos.crear_movimiento(datos)
            self.mostrar_mensaje("Movimiento guardado correctamente")
            self.cargar_movimientos()
            self.cerrar_modal(e)
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)
            print(e)
    
    def cambiar_tipo_movimiento(self, e):
        # Your existing change handler code
        if e.data == "INGRESO TERRESTRE":
            self.container_ingreso_terrestre.visible = True
            self.nombre_movimiento.value = "Nuevo Movimiento Terrestre"
        self.page.update()
    
    
    def cargar_movimientos(self):
        movimientos = self.controlador_movimientos.obtener_movimientos()
        
        self.data_table.rows.clear()
        
        for movimiento in movimientos:
            # cliente_nombre = next((cliente.nombre_cliente for cliente in self.controlador_cliente.obtener_clientes() if cliente.id_cliente == movimiento.id_cliente), "CLIENTE INACTIVO")

            edit_button = ft.TextButton(
                text="Editar",
                on_click=lambda _, movimiento=movimiento: self.abrir_modal_editar(_, movimiento)
            )
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(movimiento.id_movimiento)),
                    ft.DataCell(ft.Text(movimiento.no_servicio)),
                    ft.DataCell(ft.Text(movimiento.tipo_movimiento)),
                    ft.DataCell(ft.Text(movimiento.categoria)),
                    ft.DataCell(ft.Text(movimiento.ubicacion, text_align="center")),
                    ft.DataCell(ft.Text(round(movimiento.unidades))),
                    ft.DataCell(ft.Text(round(movimiento.neto_bascula))),
                    ft.DataCell(ft.Text(movimiento.fecha.strftime("%d/%m/%Y"))),
                    ft.DataCell(ft.Text(movimiento.hora_inicio.strftime("%H:%M"))),
                    ft.DataCell(ft.Text(movimiento.hora_fin.strftime("%H:%M"))),
                    ft.DataCell(edit_button)
                ]
            )
            self.data_table.rows.append(row)
            
        self.page.update()