import flet as ft


class Datos(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Datos"
        self.page = page
        self.width = "100%"
        self.height = "100%"
        self.bgcolor = "#f0f123"
        self.alignment = ft.alignment.center
        self.go_home = ft.TextButton(text="Inicio", on_click=lambda _:self.page.go("/"))
        
        self.content = ft.Column([
                ft.Row([
                    ft.Container(
                    content=self.go_home)
                ]),
                ft.Row([
                    ft.Container(
                        content=ft.TextButton("Clientes", on_click=lambda _:self.page.go("/clientes")),
                        width=200,
                        height=200,
                        bgcolor="red"
                    ),
                    ft.Container(
                        content=ft.TextButton("Minas", on_click=lambda _:self.page.go("/minas")),
                        width=200,
                        height=200,
                        bgcolor="pink"
                    ),
                    ft.Container(
                        content=ft.TextButton("Lotes", on_click=lambda _:self.page.go("/lotes")),
                        width=200,
                        height=200,
                        bgcolor="grey"
                    ),
                    ft.Container(
                        content=ft.Text("Productos"),
                        width=200,
                        height=200,
                        bgcolor="blue"
                    ),
                    ft.Container(
                        content=ft.Text("Barcazas", text_align="center"),
                        width=200,
                        height=200,
                        bgcolor="white",
                        alignment=ft.alignment.center
                    ),
                ],
                       alignment=ft.alignment.center)
                
        ], )