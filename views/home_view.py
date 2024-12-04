import flet as ft


class HomeView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.title = "Inicio"
        page.title = "Inventario general Carga Seca"
        self.page = page
        self.go_datos = ft.TextButton(text="Datos", on_click=lambda _:self.page.go("/datos"))
        self.anunciar_carga = ft.TextButton(text="Cargas anunciadas", on_click=lambda _:self.page.go("/anunciar_carga"))
        self.nuevo_servicio = ft.TextButton(text="Movimientos", on_click=lambda _:self.page.go("/nuevo_servicio"))
        self.data_table = ft.DataTable(
            width=float('inf'),
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("No. Servicio"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ]
        )
        
        self.content = ft.Column([
            ft.Row([
                ft.Container(
                    content=self.go_datos
                ),
                ft.Container(
                    content=self.nuevo_servicio
                ),
                ft.Container(
                    content=self.anunciar_carga
                ),
                
            ]),
            ft.Column([
                
            ])
        ])
