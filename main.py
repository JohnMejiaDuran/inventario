import flet as ft
from routes.router import init_router
from database.db import Base, engine
from database.models.clientes import Cliente

async def main(page: ft.Page):
    page.title = "Inventario"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True

    # Crear las tablas en la base de datos
    Base.metadata.create_all(engine)

    # Initialize the router
    init_router(page)
    
    # Set the initial route to "/"
    await page.go_async("/")

if __name__ == "__main__":
    ft.app(target=main)