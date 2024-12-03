import flet as ft
from components.go_home import create_home_button

class Datos(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Datos"
        self.page = page
        self.width = "100%"
        self.height = "100%"
        self.bgcolor = "#f5f5f5"
        self.alignment = ft.alignment.center
        self.go_home = create_home_button(page, lambda _: page.go("/"))
        
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
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("Minas", on_click=lambda _:self.page.go("/minas")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("Lotes", on_click=lambda _:self.page.go("/lotes")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white",
                        border = ft.border_radius.all(20)
                    ),
                    
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([
                    ft.Container(
                        content=ft.TextButton("Transportadores", on_click=lambda _:self.page.go("/transportadores")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("Productos", on_click=lambda _:self.page.go("/productos")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("Tipo de productos", on_click=lambda _:self.page.go("/tipo_productos")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([
                    ft.Container(
                        content=ft.TextButton("Bodegas", on_click=lambda _:self.page.go("/")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("Viajes", on_click=lambda _:self.page.go("/")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("Barcazas", on_click=lambda _:self.page.go("/")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ])
            