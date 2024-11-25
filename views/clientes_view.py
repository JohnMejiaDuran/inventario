import flet as ft


class ClientesView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.title = "Clientes"
        self.page = page
        self.go_home = ft.TextButton(text="Atrás", on_click=lambda _:self.page.go("/datos"))
        
        self.content = self.go_home