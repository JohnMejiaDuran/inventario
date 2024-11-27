# BaseView.py

import flet as ft
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import threading
import time

from database.db import engine

Session = sessionmaker(bind=engine)
session = Session()


class BaseView(ft.Container):
    def __init__(
        self,
        page,
        entity_name,
        model,
        campos_formulario,
        columnas_tabla,
        dropdown_fields=None,
    ):
        """
        Clase base para vistas de entidades.

        :param page: Página de Flet.
        :param entity_name: Nombre de la entidad (por ejemplo, "Mina" o "Cliente").
        :param model: Modelo de SQLAlchemy correspondiente.
        :param campos_formulario: Lista de tuplas con (nombre_campo, tipo_control, label).
        :param columnas_tabla: Lista de columnas para la DataTable.
        :param dropdown_fields: Diccionario donde la clave es el nombre del campo y el valor es una función que retorna las opciones.
        """
        super().__init__()
        self.page = page
        self.entity_name = entity_name
        self.model = model
        self.campos_formulario = campos_formulario
        self.columnas_tabla = columnas_tabla
        self.dropdown_fields = dropdown_fields or {}
        self.entidad_seleccionada = None
        self.modal_open = False
        self.print_thread = None
        self.modal_container = None  # Referencia al contenedor del modal

        # Inicializar controles principales
        self.go_home = ft.TextButton(text="Atrás", on_click=self.ir_atras)
        self.form_inputs = {}
        for campo, tipo, label in self.campos_formulario:
            if tipo == "TextField":
                self.form_inputs[campo] = ft.TextField(label=label)
            elif tipo == "Checkbox":
                self.form_inputs[campo] = ft.Checkbox(label=label, value=True)
            elif tipo == "Dropdown":
                self.form_inputs[campo] = ft.Dropdown(
                    label=label, width=400, options=[]
                )
            # Agrega más tipos según tus necesidades

        self.message = ft.Text()
        self.save_button = ft.ElevatedButton(
            text=f"Guardar {self.entity_name}", on_click=self.guardar_entidad
        )

        # Tabla de datos
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("#")),  # Índice
                *[
                    ft.DataColumn(label=ft.Text(label))
                    for campo, label in self.columnas_tabla
                ],
                ft.DataColumn(label=ft.Text("Acciones")),  # Acciones
            ],
            rows=[],
        )

        # Diseño principal
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text(
                    f"Crear Nuevo {self.entity_name}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                *self.form_inputs.values(),
                self.save_button,
                self.message,
                self.data_table,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=20,
        )

        # Añadir el contenido principal a la página
        self.page.add(self.content)

        # Llamar a did_mount para cargar entidades y dropdowns
        self.did_mount()

    def ir_atras(self, e):
        """Maneja el evento de clic en el botón 'Atrás'."""
        if self.modal_open:
            self.cerrar_modal()
        self.page.go("/datos")  # Ajusta la ruta según tu routing

    def did_mount(self):
        """Método llamado una vez que el control ha sido montado en la página."""
        print("Mounting BaseView: Cargando entidades y dropdowns.")
        self.cargar_entidades()
        self.cargar_opciones_dropdown()

    def cargar_opciones_dropdown(self):
        """Carga las opciones para los dropdowns basados en dropdown_fields."""
        for campo, funcion in self.dropdown_fields.items():
            dropdown = self.form_inputs.get(campo)
            if dropdown:
                try:
                    opciones = funcion()
                    print(f"Opciones obtenidas para '{campo}': {opciones}")  # Debug
                    dropdown.options.clear()
                    for opcion in opciones:
                        dropdown_option = ft.dropdown.Option(
                            key=str(opcion["key"]), text=opcion["text"]
                        )
                        dropdown.options.append(dropdown_option)
                    print(f"Dropdown '{campo}' actualizado con opciones.")  # Debug
                except Exception as ex:
                    print(f"Error al cargar opciones para {campo}: {ex}")
        self.page.update()

    def cargar_entidades(self):
        """Load and display entities in the data table."""
        try:
            entidades = session.query(self.model).all()
            print(f"Entidades cargadas para '{self.entity_name}': {entidades}")  # Debug
            self.data_table.rows.clear()

            for index, entidad in enumerate(entidades, 1):
                edit_button = ft.IconButton(
                    ft.icons.EDIT,
                    on_click=lambda e, c=entidad: self.abrir_modal_edicion(c),
                )

                # Obtener el estado y definir estilos
                estado = getattr(entidad, 'estado', True)
                estado_text = "Activo" if estado else "Inactivo"
                estado_text_color = ft.colors.BLACK if estado else ft.colors.WHITE
                estado_bgcolor = None if estado else ft.colors.RED_400

                # Crear un Container para la celda de estado
                estado_cell = ft.DataCell(
                    ft.Container(
                        content=ft.Text(
                            estado_text,
                            color=estado_text_color,
                            weight=ft.FontWeight.BOLD,
                        ),
                        bgcolor=estado_bgcolor,
                        padding=ft.padding.all(5),  # Opcional: agrega un padding si lo deseas
                    )
                )

                # Construir las celdas de la fila
                row_cells = [
                    ft.DataCell(ft.Text(str(index))),  # Índice
                ]

                for campo, _ in self.columnas_tabla:
                    if campo == "cliente_nombre":
                        cliente_nombre = entidad.cliente.nombre_cliente if entidad.cliente else "Sin Cliente"
                        row_cells.append(ft.DataCell(ft.Text(cliente_nombre)))
                    elif campo == "estado":
                        # Código para manejar el estado (como en tu implementación actual)
                        row_cells.append(estado_cell)
                    else:
                        valor = getattr(entidad, campo, "")
                        row_cells.append(ft.DataCell(ft.Text(str(valor))))

                row_cells.append(ft.DataCell(edit_button))  # Acciones

                row = ft.DataRow(cells=row_cells)
                self.data_table.rows.append(row)
            self.page.update()
            print("Entidades y filas de la tabla actualizadas correctamente.")  # Debug
        except Exception as ex:
            print(f"Error al cargar {self.entity_name.lower()}s: {ex}")
            self.message.value = f"Error al cargar {self.entity_name.lower()}s: {ex}"
            self.page.update()


    def guardar_entidad(self, e):
        """Guarda una nueva entidad."""
        datos = {}
        for campo, control in self.form_inputs.items():
            if isinstance(control, ft.TextField):
                datos[campo] = control.value.strip()
            elif isinstance(control, ft.Checkbox):
                datos[campo] = control.value
            elif isinstance(control, ft.Dropdown):
                datos[campo] = int(control.value) if control.value else None
            # Agrega más tipos según tus necesidades

        # Validaciones básicas
        required_fields = [
            campo for campo, tipo, label in self.campos_formulario if tipo != "Checkbox"
        ]
        if all([datos.get(campo) for campo in required_fields]):
            try:
                nueva_entidad = self.model(**datos)
                session.add(nueva_entidad)
                session.commit()
                self.message.value = f"{self.entity_name} guardado exitosamente."
                # Limpiar los campos
                for control in self.form_inputs.values():
                    if isinstance(control, ft.TextField):
                        control.value = ""
                    elif isinstance(control, ft.Checkbox):
                        control.value = True
                    elif isinstance(control, ft.Dropdown):
                        control.value = None
                self.cargar_entidades()
            except IntegrityError as ex:
                session.rollback()
                if 'UNIQUE constraint failed' in str(ex.orig):
                    self.message.value = f"Error: Ya existe un {self.entity_name.lower()} con ese nombre."
                else:
                    self.message.value = f"Error al guardar {self.entity_name.lower()}: {ex}"
                print(f"Error al guardar {self.entity_name.lower()}: {ex}")  # Debug
            except Exception as ex:
                session.rollback()
                self.message.value = f"Error al guardar {self.entity_name.lower()}: {ex}"
                print(f"Error al guardar {self.entity_name.lower()}: {ex}")  # Debug
        else:
            self.message.value = "Por favor ingresa todos los campos obligatorios."
        self.page.update()

    def abrir_modal_edicion(self, entidad):
        """Open the edit modal for the selected entity."""
        self.entidad_seleccionada = entidad

        # Crear controles para el modal
        modal_controles = {}
        for campo, tipo, label in self.campos_formulario:
            valor = getattr(entidad, campo, "")
            if tipo == "TextField":
                modal_controles[campo] = ft.TextField(label=label, value=str(valor))
            elif tipo == "Checkbox":
                modal_controles[campo] = ft.Checkbox(label=label, value=bool(valor))
            elif tipo == "Dropdown":
                modal_controles[campo] = ft.Dropdown(label=label, width=400, options=[])
                # Cargar opciones para el dropdown específico en el modal
                if campo in self.dropdown_fields:
                    try:
                        opciones = self.dropdown_fields[campo]()
                        print(
                            f"Opciones obtenidas para '{campo}' en el modal: {opciones}"
                        )  # Debug
                        modal_controles[campo].options.clear()
                        for opcion in opciones:
                            dropdown_option = ft.dropdown.Option(
                                key=str(opcion["key"]), text=opcion["text"]
                            )
                            modal_controles[campo].options.append(dropdown_option)
                        # Establecer el valor actual del dropdown en el modal
                        modal_controles[campo].value = str(valor) if valor else None
                        print(
                            f"Dropdown '{campo}' en el modal actualizado con opciones."
                        )  # Debug
                    except Exception as ex:
                        print(
                            f"Error al cargar opciones para {campo} en el modal: {ex}"
                        )
                    except Exception as ex:
                        print(
                            f"Error al cargar opciones para {campo} en el modal: {ex}"
                        )
            # Agrega más tipos según tus necesidades

        modal_text = ft.Text("")

        # Definir el contenido del modal
        self.modal_container = ft.Container(
            expand=True,
            bgcolor=ft.colors.BLACK45,  # Fondo semi-transparente
            content=ft.Container(
                width=500,
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Editar {self.entity_name}",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        *modal_controles.values(),
                        modal_text,
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    text="Cancelar", on_click=self.cerrar_modal
                                ),
                                ft.TextButton(
                                    text="Guardar",
                                    on_click=lambda e: self.actualizar_entidad(
                                        modal_controles, modal_text
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=10,  # Espacio entre controles
                ),
            ),
            alignment=ft.alignment.center,  # Centrar el modal
        )

        # Añadir el modal al overlay
        self.page.overlay.append(self.modal_container)
        self.modal_open = True
        self.start_print_thread()
        self.page.update()
        print(f"Modal de edición abierto para {self.entity_name}: {entidad}")  # Debug

    def actualizar_entidad(self, modal_controles, modal_text):
        """Actualiza la entidad seleccionada con los datos editados."""
        if self.entidad_seleccionada:
            datos = {}
            for campo, control in modal_controles.items():
                if isinstance(control, ft.TextField):
                    datos[campo] = control.value.strip()
                elif isinstance(control, ft.Checkbox):
                    datos[campo] = control.value
                elif isinstance(control, ft.Dropdown):
                    datos[campo] = int(control.value) if control.value else None
                # Agrega más tipos según tus necesidades

            # Validaciones y guardado...
            required_fields = [
                campo
                for campo, tipo, label in self.campos_formulario
                if tipo != "Checkbox"
            ]
            if all([datos.get(campo) for campo in required_fields]):
                try:
                    for campo, valor in datos.items():
                        setattr(self.entidad_seleccionada, campo, valor)
                    session.commit()
                    self.cerrar_modal()
                    self.cargar_entidades()
                    self.message.value = f"{self.entity_name} actualizado exitosamente."
                except IntegrityError as ex:
                    session.rollback()
                    if 'UNIQUE constraint failed' in str(ex.orig):
                        modal_text.value = f"Error: Ya existe un {self.entity_name.lower()} con ese nombre."
                    else:
                        modal_text.value = f"Error al actualizar {self.entity_name.lower()}: {ex}"
                    print(f"Error al actualizar {self.entity_name.lower()}: {ex}")  # Debug
                except Exception as ex:
                    session.rollback()
                    modal_text.value = f"Error al actualizar {self.entity_name.lower()}: {ex}"
                    print(f"Error al actualizar {self.entity_name.lower()}: {ex}")  # Debug
            else:
                modal_text.value = "Por favor ingresa todos los campos obligatorios."
        self.page.update()

    def cerrar_modal(self, e=None):
        """Close the edit modal."""
        self.modal_open = False

        # Cerrar y remover el modal del overlay
        if self.modal_container and self.modal_container in self.page.overlay:
            self.page.overlay.remove(self.modal_container)
            self.modal_container = None  # Limpiar la referencia

        self.page.update()
        print("Modal de edición cerrado.")  # Debug

    def start_print_thread(self):
        """Start a thread to print while the modal is open."""
        if self.print_thread is None or not self.print_thread.is_alive():
            self.print_thread = threading.Thread(target=self.print_loop, daemon=True)
            self.print_thread.start()

    def print_loop(self):
        """Print 'Modal is open' every second while the modal is open."""
        while self.modal_open:
            print("Modal is open")
            time.sleep(1)
