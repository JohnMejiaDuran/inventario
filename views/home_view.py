import flet as ft


class HomeView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.title = "Inicio"
        page.title = "Inventario general Carga Seca"
        self.page = page
        self.go_datos = ft.TextButton(text="Datos", on_click=lambda _:self.page.go("/datos"))
        self.anunciar_carga = ft.TextButton(text="Anunciar carga", on_click=lambda _:self.page.go("/anunciar_carga"))
        
        self.content = ft.Row([
            ft.Container(
                content=self.go_datos
            ),
            ft.Container(
                content=self.anunciar_carga
            )
        ])
