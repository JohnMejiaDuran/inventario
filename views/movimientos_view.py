import flet as ft
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from controllers.control_transportadores import ControlTransportador
from controllers.control_productos import ControlProducto
from controllers.control_tipo_producto import  ControlTipoProducto
from controllers.control_bodegas import ControlBodega
import datetime

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
        self.insert_cliente = ft.Dropdown(
            label="Selecciona un cliente",
            options=[
                ft.dropdown.Option(cliente.nombre_cliente)
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
            label="Selecciona un tipo de vehiculo",
            options=[
                ft.dropdown.Option("PLANCHA"),
                ft.dropdown.Option("VOLCO"),
                ft.dropdown.Option("MULA")
            ]
            ,expand=True)
        self.insert_transportador = ft.Dropdown(
            label="Selecciona un transportador",
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
            label="Selecciona un tipo de producto",
            options=[
                ft.dropdown.Option(tipo_producto.nombre_tipo_producto)
                for tipo_producto in self.controlador_tipo_producto.obtener_tipo_productos()
                if tipo_producto.estado_tipo_producto
                ],
            expand=True)
        self.insert_imo = ft.Dropdown(
            label="Seleccione IMO",
            options=[
                ft.dropdown.Option("IMO 3"),
                ft.dropdown.Option("IMO 9"),
            ],
            expand=True
        )
        
        self.insert_tipo_unidad = ft.Dropdown(
            label="Seleccione tipo de unidad",
            options=[
                ft.dropdown.Option("BIG BAG"),
                ft.dropdown.Option("CARGA GENERAL"),
                ft.dropdown.Option("CONTENEDORES"),
                ft.dropdown.Option("ISOTANQUES"),
                ft.dropdown.Option("PALLET"),
                
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
        
        self.insert_fecha = ft.TextField(label="Ingrese fecha", expand=True)
        self.insert_hora_inicio = ft.TextField(label="Ingrese hora inicio", expand=True)
        self.insert_hora_fin = ft.TextField(label="Ingrese hora fin", expand=True)
        self.insert_para = ft.TextField(label="Ingrese Para", expand=True)
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
        self.fecha_button = ft.IconButton(
            icon=ft.icons.EVENT,
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
                    self.insert_hora_inicio,
                    self.insert_hora_fin,
                    self.insert_para
                ]),
                ft.Row([
                    self.insert_observaciones
                ])
            ]))
        
        # Main content layout
        self.content = ft.Column(
            controls=[
                ft.Row([
                    ft.TextButton("Inicio", on_click=lambda e: page.go("/")),
                ]),
                self.nuevo_movimiento_btn,
                # Other controls...
            ]
        )
    def on_fecha_change(self, e):
        """Handle date selection"""
        selected_date = e.control.value
        if selected_date:
            # Format date as string for display
            formatted_date = selected_date.strftime("%d/%m/%Y")
            self.fecha_display.value = formatted_date
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
        # obtener la mina del cliente seleccionado
        minas = self.controlador_mina.obtener_minas()
        minas = [mina for mina in minas if mina.id_cliente == cliente_seleccionado]
        if minas: 
            self.insert_mina.options = [
                ft.dropdown.Option(mina.nombre_mina) for mina in minas
                if mina.estado 
            ]
        self.page.update()
        
    def actualizar_lotes(self, e):
        """Al seleccionar la mina del cliente me trae sus lotes"""
        mina_seleccionada = self.insert_mina.value
        self.insert_lote.options = []
        # obtener la mina del cliente seleccionado
        lotes = self.controlador_lotes.obtener_lotes()
        lotes = [lote for lote in lotes if lote.id_mina == mina_seleccionada]
        if lotes:
            self.insert_lote.options = [
                ft.dropdown.Option(lote.nombre_lote) for lote in lotes
            ]
        self.page.update()
    
    def abrir_modal_movimiento(self, e):
        modal = ft.AlertDialog(
            title=ft.Text("Nuevo Movimiento"),
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
                ft.ElevatedButton("Guardar", on_click=self.guardar_movimiento)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = modal
        modal.open = True
        self.page.update()
    
    def cerrar_modal(self, e):
        self.page.dialog.open = False
        self.page.update()
    
    def guardar_movimiento(self, e):
        # Add save logic here
        self.cerrar_modal(e)
    
    def cambiar_tipo_movimiento(self, e):
        # Your existing change handler code
        self.container_ingreso_terrestre.visible = e.data == "INGRESO TERRESTRE"
        self.page.update()