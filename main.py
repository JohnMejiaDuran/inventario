import flet as ft
from routes.router import init_router
from database.db import Base, engine
from database.models.clientes import Cliente
from database.models.minas import Mina
from database.models.transportadores import Transportador
from database.models.productos import Producto
from database.models.tipos_productos import TipoProducto
from database.models.anuncio_carga import AnuncioCarga
from database.models.movimientos import Movimiento
from database.models.bodegas import Bodega
from database.models.viajes import Viaje
from database.models.barcazas import Barcaza

def main(page: ft.Page):
    page.title = "Inventario"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.maximized = True

    # Crear las tablas en la base de datos
    Base.metadata.create_all(engine)

    # Initialize the router
    init_router(page)
    
    # Set the initial route to "/"
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)