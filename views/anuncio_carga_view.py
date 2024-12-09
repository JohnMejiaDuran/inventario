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
            
            columns=[
                ft.DataColumn(ft.Text("#", text_align="center")),
                ft.DataColumn(ft.Text("PLACA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PLACA\nREMOLQUE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NOMBRE\nCONDUCTOR",text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NÚMERO DE\nCÉDULA",text_align="center" ), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NÚMERO DE\nCONTACTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("EMPRESA\nTRANSPORTADORA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NIT", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO DE\nVEHÍCULO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CLIENTE /\n CONSIGNATARIO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BL", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PRODUCTO/REFERENCIA \n /VPEDIDO O NÚMERO DE \n CONTENEDOR", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("SELLOS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BULTOS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PESO KGS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA DE \n PROGRAMACIÓN DE \n CARGA/DESCARGUE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
        )
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Cargas Anunciadas", size=20, weight=ft.FontWeight.BOLD),
                ft.Column(
                    controls=[
                        ft.Row([
                            self.data_table
                        ],
                               scroll=ft.ScrollMode.ALWAYS),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                    scroll=ft.ScrollMode.ALWAYS
                ),
                
            ],
            
        )
    def ir_atras(self, _):
        self.page.go("/datos")
        
    