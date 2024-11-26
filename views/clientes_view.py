import flet as ft
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database.db import engine, Base
from database.models.clientes import Cliente

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()


class ClientesView(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Clientes"
        # Navigation
        self.go_home = ft.TextButton(text="Atrás", on_click=self.go_to_datos)
        # Modal for editing
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_nit = ft.TextField(label="Nit")
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        self.modal_text = ft.Text("")
        # Edit Modal
        self.edit_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Cliente"),
            content=ft.Column(
                [self.modal_nombre, self.modal_nit, self.modal_estado, self.modal_text]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                ft.TextButton("Guardar", on_click=self.actualizar_cliente),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        # Form inputs for new client
        self.nombre_input = ft.TextField(label="Nombre")
        self.nit_input = ft.TextField(label="Nit")
        self.estado_input = ft.Checkbox(label="Activo", value=True)
        # Message display
        self.message = ft.Text()
        # Buttons
        self.save_button = ft.ElevatedButton(
            text="Guardar Cliente", on_click=self.guardar_cliente
        )
        # Selected client tracking
        self.cliente_seleccionado = None
        # Data table
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("NIT")),
                ft.DataColumn(label=ft.Text("Estado")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[],
        )

    def build(self):
        # Load clients when building the view

        self.cargar_clientes()

        return ft.Column(
            controls=[
                self.go_home,
                ft.Text("Crear Nuevo Cliente", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_input,
                self.nit_input,
                self.estado_input,
                self.save_button,
                self.message,
                ft.Text("Lista de Clientes", size=20, weight=ft.FontWeight.BOLD),
                self.data_table,
            ]
        )
        
        
        

    def go_to_datos(self, e):
        self.page.go("/datos")

    def abrir_modal_edicion(self, cliente):
        # Store the selected client
        self.cliente_seleccionado = cliente
        
        # Reset modal text
        self.modal_text.value = ""
        
        # Populate modal fields
        self.modal_nombre.value = cliente.nombre
        self.modal_nit.value = cliente.nit
        self.modal_estado.value = cliente.estado

        # Open the modal
        self.page.dialog = self.edit_modal
        self.edit_modal.open = True
        self.page.update()

    def cerrar_modal(self, e):
        # Close the modal
        self.edit_modal.open = False
        self.page.update()

    def actualizar_cliente(self, e):
        if self.cliente_seleccionado:
            try:
                # Check for existing clients with same name or NIT (excluding current client)
                nombre = self.modal_nombre.value
                nit = self.modal_nit.value
                
                existe_nombre = (
                    session.query(Cliente)
                    .filter(Cliente.nombre == nombre)
                    .filter(Cliente.id != self.cliente_seleccionado.id)
                    .first()
                )
                
                existe_nit = (
                    session.query(Cliente)
                    .filter(Cliente.nit == nit)
                    .filter(Cliente.id != self.cliente_seleccionado.id)
                    .first()
                )

                if existe_nombre and existe_nit:
                    self.modal_text.value = "El nombre y NIT ya están en uso por otro cliente."
                    self.page.update()
                    return
                elif existe_nombre:
                    self.modal_text.value = "El nombre ya está en uso por otro cliente."
                    self.page.update()
                    return
                elif existe_nit:
                    self.modal_text.value = "El NIT ya está en uso por otro cliente."
                    self.page.update()
                    return

                # Update the selected client
                self.cliente_seleccionado.nombre = nombre
                self.cliente_seleccionado.nit = nit
                self.cliente_seleccionado.estado = self.modal_estado.value
                
                session.commit()
                
                # Close modal
                self.edit_modal.open = False
                
                # Reload clients and show success message
                self.cargar_clientes()
                self.message.value = "Cliente actualizado exitosamente"
                self.page.update()
            except IntegrityError:
                session.rollback()
                self.message.value = "Error: No se pudo actualizar el cliente debido a una restricción única."
                self.page.update()
            except Exception as ex:
                session.rollback()
                self.message.value = f"Error al actualizar: {str(ex)}"
                self.page.update()

    def guardar_cliente(self, e):
        nombre = self.nombre_input.value
        nit = self.nit_input.value
        estado = self.estado_input.value

        if nombre and nit:
            try:
                existe_nombre = session.query(Cliente).filter_by(nombre=nombre).first()
                existe_nit = session.query(Cliente).filter_by(nit=nit).first()

                if existe_nombre and existe_nit:
                    self.message.value = "El nombre y el NIT ya existen"
                elif existe_nombre:
                    self.message.value = "El nombre ya existe"
                elif existe_nit:
                    self.message.value = "El NIT ya existe"
                else:
                    nuevo_cliente = Cliente(nombre=nombre, nit=nit, estado=estado)
                    session.add(nuevo_cliente)
                    session.commit()

                    # Clear inputs and show success message
                    self.nombre_input.value = ""
                    self.nit_input.value = ""
                    self.estado_input.value = True
                    self.message.value = "Cliente guardado"

                    # Reload the clients table
                    self.cargar_clientes()
            except IntegrityError:
                # Rollback the session in case of any integrity error
                session.rollback()
                self.message.value = "Error: No se pudo guardar el cliente debido a una restricción única."
            except Exception as ex:
                self.message.value = f"Error al guardar: {str(ex)}"
                session.rollback()
        else:
            self.message.value = "Por favor, ingrese tanto el nombre como el NIT."

        # Update the view
        self.update()

    def cargar_clientes(self):
        try:
            clientes = session.query(Cliente).all()

            # Clear existing rows and repopulate
            self.data_table.rows.clear()
            for cliente in clientes:
                # Create edit button for each row
                edit_button = ft.TextButton(
                    text="Editar",
                    on_click=lambda e, c=cliente: self.abrir_modal_edicion(c),
                )

                self.data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cliente.nombre)),
                            ft.DataCell(ft.Text(cliente.nit)),
                            ft.DataCell(
                                ft.Text("Activo" if cliente.estado else "Inactivo")
                            ),
                            ft.DataCell(edit_button),
                        ]
                    )
                )

            # Mark the table as needing an update
            self.data_table.update()
        except Exception as ex:
            print(f"Error al cargar clientes: {ex}")
