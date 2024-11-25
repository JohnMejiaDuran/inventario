import flet as ft


class HomeView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.title = "Inicio"
        self.page = page
        self.go_datos = ft.TextButton(text="Datos", on_click=lambda _:self.page.go("/datos"))
        
        self.content = self.go_datos
