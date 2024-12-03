# go_home.py
import flet as ft

def create_home_button(page, on_click):
    return ft.TextButton(
        text="Inicio",
        on_click=on_click
    )
    
