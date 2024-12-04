import flet as ft


class HomeView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.title = "Inicio"
        page.title = "Inventario general Carga Seca"
        self.page = page
        self.go_datos = ft.TextButton(text="Datos", on_click=lambda _:self.page.go("/datos"))
        self.anunciar_carga = ft.TextButton(text="Cargas anunciadas", on_click=lambda _:self.page.go("/anunciar_carga"))
        self.movimientos = ft.TextButton(text="Movimientos", on_click=lambda _:self.page.go("/movimientos"))
        self.data_table = ft.DataTable(
            width=float('inf'),
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("No. \n SERVICIO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO \n MOVIMIENTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PRODUCTO"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO \n PRODUCTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("UNIDAD"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CATEGORIA"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NETO \n BASCULA(tm)", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("VIAJE"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BARCAZA"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ]
            ,rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300)
        )
        
        self.nuevo_servicio = ft.TextButton(text="Nuevo servicio")
        self.content = ft.Column([
            ft.Row([
                ft.Container(
                    content=self.go_datos,
                ),
                ft.Container(
                    content=self.movimientos
                ),
                ft.Container(
                    content=self.anunciar_carga
                ),
                
            ]),
            ft.Row([
                self.nuevo_servicio
            ])
            ,
            ft.Column([
                self.data_table
            ])
        ])
