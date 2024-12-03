import flet as ft
from controllers.control_anuncio_carga import ControlAnuncioCarga
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from components.go_home import create_home_button

class AnuncioCargaView(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Anunciar carga"
        self.page = page
        self.control_anuncio_carga = ControlAnuncioCarga()
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        self.controlador_lotes = ControlLote()
        self.go_home = create_home_button(page, lambda _: page.go("/"))
        self.insert_cliente = ft.Dropdown(
            label="Selecciona un cliente",
            options=[
                ft.dropdown.Option(cliente.nombre_cliente)
                for cliente in self.controlador_cliente.obtener_clientes()
                if cliente.estado
            ],
                on_change=self.actualizar_minas
            )
        self.insert_mina = ft.Dropdown(
            label="Selecciona una mina",
            on_change=self.actualizar_lotes
            )
        self.insert_lote = ft.Dropdown(label="Selecciona un lote")
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Anunciar carga", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=
                        ft.Row([
                            self.insert_cliente,
                            self.insert_mina,
                            self.insert_lote
                            ],
                            alignment=ft.MainAxisAlignment.CENTER 
                        ),
                    ),
                ft.ElevatedButton("Anunciar carga")
            ],
        )
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