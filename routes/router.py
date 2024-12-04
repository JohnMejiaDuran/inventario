import flet as ft
from views.home_view import HomeView
from views.datos import Datos
from views.clientes_view import ClientesView
from views.minas_view import MinasView  
from views.lote_view import LoteView  
from views.transportadores_view import TransportadoresView
from views.productos_view import ProductosView
from views.tipo_producto_view import TipoProductoView
from views.anuncio_carga_view import AnuncioCargaView
from views.barcazas_view import BarcazaView
from views.bodegas_view import BodegaView
from views.viajes_view import ViajeView
from views.movimientos_view import MovimientoView

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
        elif page.route == "/productos":
            page.views.append(
                ft.View(
                    "/productos",
                    [
                        ProductosView(page)
                    ]
                )
            )
        elif page.route == "/tipo_productos":
            page.views.append(
                ft.View(
                    "/tipo_productos",
                    [
                        TipoProductoView(page)
                    ]
                )
            )
        elif page.route == "/anunciar_carga":
            page.views.append(
                ft.View(
                    "/anunciar_carga",
                    [
                        AnuncioCargaView(page)
                    ]
                )
            )
        elif page.route == "/barcazas":
            page.views.append(
                ft.View(
                    "/barcazas",
                    [
                        BarcazaView(page)
                    ]
                )
            )
        elif page.route == "/bodegas":
            page.views.append(
                ft.View(
                    "/bodegas",
                    [
                        BodegaView(page)
                    ]
                )
            )
        elif page.route == "/viajes":
            page.views.append(
                ft.View(
                    "/viajes",
                    [
                        ViajeView(page)
                    ]
                )
            )
        elif page.route == "/movimientos":
            page.views.append(
                ft.View(
                    "/movimientos",
                    [
                        MovimientoView(page)
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