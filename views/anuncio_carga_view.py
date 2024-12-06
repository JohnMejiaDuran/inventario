import flet as ft
from controllers.control_anuncio_carga import ControlAnuncioCarga
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from components.go_home import create_home_button
from controllers.control_transportadores import ControlTransportador
from controllers.control_productos import ControlProducto
from controllers.control_tipo_producto import  ControlTipoProducto

class AnuncioCargaView(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Anunciar carga"
        self.page = page
        self.control_anuncio_carga = ControlAnuncioCarga()
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        self.controlador_lotes = ControlLote()
        self.controlador_transportador = ControlTransportador()
        self.controlador_producto = ControlProducto()
        self.controlador_tipo_producto = ControlTipoProducto()

        self.go_home = create_home_button(page, lambda _: page.go("/"))
        
        self.data_table = ft.DataTable(
            width=float('inf'),
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("No. Servicio"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Mina"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Transportador"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Producto", ), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Tipo Producto"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Tipo unidad"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Unidades \n anunciadas", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Peso \n anunciado", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
        )
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Cargas Anunciadas", size=20, weight=ft.FontWeight.BOLD),
                ft.Column([
                    self.data_table
                ])
            ],
        )
    def ir_atras(self, _):
        self.page.go("/datos")
        
    