import flet as ft
from components.go_home import create_home_button

class Datos(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Datos"
        self.page = page
        self.width = "100%"
        self.height = "100%"
        
        self.alignment = ft.alignment.center
        self.go_home = create_home_button(page, lambda _: page.go("/"))
        
        self.content = ft.Column([
                ft.Row([
                    ft.Container(
                    content=self.go_home)
                ]),
                ft.Row([
                    ft.Container(
                        content=ft.TextButton("CLIENTES", on_click=lambda _:self.page.go("/clientes")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("MINAS", on_click=lambda _:self.page.go("/minas")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("LOTES", on_click=lambda _:self.page.go("/lotes")),
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
                        content=ft.TextButton("TRANSPORTADORES", on_click=lambda _:self.page.go("/transportadores")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("PRODUCTOS", on_click=lambda _:self.page.go("/productos")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("TIPO DE PRODUCTOS", on_click=lambda _:self.page.go("/tipo_productos")),
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
                        content=ft.TextButton("BODEGAS", on_click=lambda _:self.page.go("/bodegas")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("VIAJES", on_click=lambda _:self.page.go("/viajes")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                    ft.Container(
                        content=ft.TextButton("BARCAZAS", on_click=lambda _:self.page.go("/barcazas")),
                        width=200,
                        height=200,
                        border_radius=20,
                        bgcolor="white"
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ])
            