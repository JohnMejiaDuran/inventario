import flet as ft
from routes.router import init_router

async def main(page: ft.Page):
    page.title = "Inventario"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True

    # Initialize the router
    init_router(page)
    
    # Set the initial route to "/"
    await page.go_async("/")

if __name__ == "__main__":
    ft.app(target=main)