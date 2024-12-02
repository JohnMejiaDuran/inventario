import flet as ft
from views.home_view import HomeView
from views.datos import Datos
from views.clientes_view import ClientesView
from views.minas_view import MinasView  
from views.lote_view import LoteView  
from views.transportadores_view import TransportadoresView

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
        elif page.route == "/minas":
            page.views.append(
                ft.View(
                    "/minas",
                    [
                        MinasView(page)
                    ]
                )
            )
        elif page.route == "/lotes":
            page.views.append(
                ft.View(
                    "/lotes",
                    [
                        LoteView(page)
                    ]
                )
            )
        elif page.route == "/transportadores":
            page.views.append(
                ft.View(
                    "/transportadoes",
                    [
                        TransportadoresView(page)
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