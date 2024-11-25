import flet as ft
from sqlalchemy.orm import sessionmaker
from database.db import engine, Base
from database.models.clientes import Cliente

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

class ClientesView(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        page.title = "Clientes"
        self.page = page
        self.go_home = ft.TextButton(text="Atrás", on_click=lambda _: self.page.go("/datos"))
        self.nombre_input = ft.TextField(label="Nombre")
        self.nit_input = ft.TextField(label="Nit")
        self.estado_input = ft.Checkbox(label="Activo", value=True)
        self.message = ft.Text()
        self.save_button = ft.ElevatedButton(text="Guardar Cliente", on_click=self.save_user)

        self.content = ft.Column(
            controls=[
                self.go_home,
                self.nombre_input,
                self.nit_input,
                self.estado_input,
                self.save_button,
                self.message
            ]
        )
        self.controls.append(self.content)

    def save_user(self, e):
        nombre = self.nombre_input.value
        nit = self.nit_input.value
        estado = self.estado_input.value
        
        if nombre and nit:
            new_user = Cliente(nombre=nombre, nit=nit, estado=estado)
            session.add(new_user)
            session.commit()
            self.message.value = "Cliente guardado"
            self.nombre_input.value = ""
            self.nit_input.value = ""
            self.estado_input.value = True
        else:
            self.message.value = "Por favor, ingrese tanto el nombre como el NIT."
        self.update()

