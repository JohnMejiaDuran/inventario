import flet as ft
from sqlalchemy.orm import sessionmaker
from database.db import engine
from database.models.minas import Mina
from database.models.clientes import Cliente

Session = sessionmaker(bind=engine)
session = Session()

class MinasView(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.mina_seleccionada = None
        
        # Recreate controls in __init__ instead of init_controls
        self.go_home = ft.TextButton(text="Atrás", on_click=lambda _: self.page.go("/datos"))
        self.nombre_input = ft.TextField(label="Nombre")
        self.cliente_dropdown = ft.Dropdown(
            label="Cliente",
            width=400,
        )
        self.estado_input = ft.Checkbox(label="Activo", value=True)
        self.message = ft.Text()
        self.save_button = ft.ElevatedButton(text="Guardar Mina", on_click=self.guardar_mina)
        
        # Modal controls
        self.modal_nombre = ft.TextField(label="Nombre")
        self.modal_cliente_dropdown = ft.Dropdown(
            label="Cliente",
            width=400,
        )
        self.modal_estado = ft.Checkbox(label="Activo", value=True)
        self.modal_text = ft.Text("")
        
        # Edit Modal
        self.edit_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Mina"),
            content=ft.Column([
                self.modal_nombre, 
                self.modal_cliente_dropdown,
                self.modal_estado, 
                self.modal_text
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                ft.TextButton("Guardar", on_click=self.actualizar_mina),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("#")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Cliente")),
                ft.DataColumn(label=ft.Text("Estado")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )

    def build(self):
        return ft.Column(
            controls=[
                self.go_home,
                ft.Text("Crear Nueva Mina", size=20, weight=ft.FontWeight.BOLD),
                self.nombre_input,
                self.cliente_dropdown,
                self.estado_input,
                self.save_button,
                self.message,
                self.data_table
            ]
        )

    def cargar_clientes_dropdown(self):
        """Populate the client dropdown with clients from the database"""
        try:
            clientes = session.query(Cliente).all()
            
            # Clear existing items
            self.cliente_dropdown.options.clear()
            self.modal_cliente_dropdown.options.clear()
            
            # Add clients to dropdown
            for cliente in clientes:
                dropdown_option = ft.dropdown.Option(
                    key=cliente.id,  # Use client ID as key
                    text=cliente.nombre  # Display client name
                )
                self.cliente_dropdown.options.append(dropdown_option)
                
                # Also add to modal dropdown
                modal_dropdown_option = ft.dropdown.Option(
                    key=cliente.id,
                    text=cliente.nombre
                )
                self.modal_cliente_dropdown.options.append(modal_dropdown_option)
        except Exception as ex:
            print(f"Error al cargar clientes: {ex}")
            self.message.value = f"Error al cargar clientes: {ex}"

    def did_mount(self):
        self.cargar_clientes_dropdown()
        self.cargar_minas()

    def guardar_mina(self, e):
        nombre = self.nombre_input.value
        cliente = self.cliente_dropdown.value
        # Use the key directly from the dropdown
        id_cliente = int(cliente) if cliente else None
        estado = self.estado_input.value
        
        if nombre and id_cliente:
            try:
                nueva_mina = Mina(nombre=nombre, id_cliente=id_cliente, estado=estado)
                session.add(nueva_mina)
                session.commit()
                self.message.value = "Mina guardada exitosamente"
                self.nombre_input.value = ""
                self.cliente_dropdown.value = None
                self.estado_input.value = True
                self.cargar_minas()
            except Exception as ex:
                session.rollback()
                self.message.value = f"Error al guardar: {str(ex)}"
        else:
            self.message.value = "Por favor ingrese el nombre de la mina y seleccione un cliente"
        self.update()

    def actualizar_mina(self, e):
        if self.mina_seleccionada:
            try:
                # Check for existing mines with same name (excluding current mine)
                nombre = self.modal_nombre.value
                id_cliente = int(self.modal_cliente_dropdown.value) if self.modal_cliente_dropdown.value else None
                
                existe_nombre = (
                    session.query(Mina)
                    .filter(Mina.nombre == nombre)
                    .filter(Mina.id != self.mina_seleccionada.id)
                    .first()
                )
                
                if existe_nombre:
                    self.modal_text.value = "El nombre ya está en uso por otra mina."
                    self.page.update()
                    return

                # Update the selected mine
                self.mina_seleccionada.nombre = nombre
                self.mina_seleccionada.id_cliente = id_cliente
                self.mina_seleccionada.estado = self.modal_estado.value
                
                session.commit()
                
                # Close modal
                self.edit_modal.open = False
                
                # Reload mines and show success message
                self.cargar_minas()
                self.message.value = "Mina actualizada exitosamente"
                self.page.update()
            except Exception as ex:
                session.rollback()
                self.message.value = f"Error al actualizar: {str(ex)}"
                self.page.update()

    def cargar_minas(self):
        try:
            minas = session.query(Mina).all()
            self.data_table.rows.clear()
            
            for index, mina in enumerate(minas, 1):
                edit_button = ft.IconButton(
                    ft.icons.EDIT,
                    on_click=lambda e, m=mina: self.abrir_modal_edicion(m),
                )
                
                cliente_nombre = mina.cliente.nombre if mina.cliente else "Sin Cliente"
                
                self.data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(index))),
                            ft.DataCell(ft.Text(mina.nombre)),
                            ft.DataCell(ft.Text(cliente_nombre)),
                            ft.DataCell(ft.Text("Activo" if mina.estado else "Inactivo")),
                            ft.DataCell(edit_button),
                        ]
                    )
                )
            self.update()
        except Exception as ex:
            print(f"Error al cargar minas: {ex}")

    def abrir_modal_edicion(self, mina):
        # Store the selected mine
        self.mina_seleccionada = mina
        
        # Reset modal text
        self.modal_text.value = ""
        
        # Populate modal fields
        self.modal_nombre.value = mina.nombre
        self.modal_estado.value = mina.estado

        # Set the current client in the dropdown
        self.modal_cliente_dropdown.value = str(mina.id_cliente) if mina.id_cliente else None
        
        # Open the modal
        self.page.dialog = self.edit_modal
        self.edit_modal.open = True
        self.page.update()

    def cerrar_modal(self, e):
        # Close the modal
        self.edit_modal.open = False
        self.page.update()