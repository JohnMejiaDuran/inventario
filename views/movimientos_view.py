import flet as ft
from controllers.control_movimiento import ControlMovimientos
from components.go_home import create_home_button
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote

class MovimientoView(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Movimientos"
        self.page = page
        self.control_movimiento = ControlMovimientos()
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        self.controlador_lotes = ControlLote()
        self.go_home =  create_home_button(page, lambda _: page.go("/"))
        
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
        self.insert_tipo_movimiento = ft.Dropdown(
            label="Selecciona un tipo de movimiento",
            options=[
                ft.dropdown.Option("Ajuste Inventario"),
                ft.dropdown.Option("Homogenizado"),
                ft.dropdown.Option("Ingreso Fluvial"),
                ft.dropdown.Option("Ingreso Terrestre"),
                ft.dropdown.Option("Ingreso Vaciado"),
                ft.dropdown.Option("Salida Fluvial"),
                ft.dropdown.Option("Salida Terrestre"),
                ft.dropdown.Option("Salida Vaciado"),
            ],
            expand=True
        )
        
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Nuevo Movimiento", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.insert_cliente,
                    self.insert_mina,
                    self.insert_lote,
                    
                ]),
                ft.Row([
                    self.insert_tipo_movimiento
                ])
            ]
        )
        
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