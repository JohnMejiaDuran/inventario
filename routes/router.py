import flet as ft
from views.home_view import HomeView
from views.datos import Datos
from views.clientes_view import ClientesView

def init_router(page: ft.Page):
    def route_change(_):
        page.views.clear()
        
        if page.route == "/" or page.route == "":
            page.views.append(
                ft.View(
                    "/",
                    [

                        HomeView(page)
                    ]
                )
            )
        elif page.route == "/datos":
            page.views.append(
                ft.View(
                    "/datos",
                    [
                        Datos(page)
                    ]
                )
            )
        elif page.route == "/clientes":
            page.views.append(
                ft.View(
                    "/clientes",
                    [
                        ClientesView(page)
                    ]
                )
            )
        
        page.update()

    def view_pop(_):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop