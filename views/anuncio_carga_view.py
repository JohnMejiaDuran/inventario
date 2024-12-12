import flet as ft
from controllers.control_anuncio_carga import ControlAnuncioCarga
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from components.go_home import create_home_button
from controllers.control_transportadores import ControlTransportador
from controllers.control_productos import ControlProducto
from controllers.control_tipo_producto import ControlTipoProducto
import pandas as pd
from datetime import datetime
import random
import string
from sqlalchemy import exists
from database.models.anuncio_carga import AnuncioCarga
from database.db import session

class AnuncioCargaView(ft.Container):
    def __init__(self, page):
        super().__init__()
        page.title = "Anunciar carga"
        self.page = page
        self.control_anuncio_carga = ControlAnuncioCarga()
        self.controlador_cliente = ControlCliente()
        self.controlador_mina = ControlMina()
        self.controlador_lotes = ControlLote()
        self.controlador_transportador = ControlTransportador()
        self.controlador_producto = ControlProducto()
        self.controlador_tipo_producto = ControlTipoProducto()
        self.df = None
        self.page_size = 50
        self.current_page = 0
        self.is_loading = False
        self.all_loaded = False
        
        # Add loading indicator
        self.loading_indicator = ft.ProgressBar(visible=False)
        self.go_home = create_home_button(page, lambda _: page.go("/"))
        self.cargar_excel = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            tooltip="Cargar archivo excel",
            on_click=self.abrir_modal_cargar_excel,
        )

        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", text_align="center")),
                ft.DataColumn(ft.Text("ID_CARGA", text_align="center")),
                ft.DataColumn(
                    ft.Text("FECHA", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("CABEZOTE", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("EMPRESA DE TRANSPORTE", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NIT:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("REMOLQUE:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("TIPO", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NOMBRE DEL CONDUCTOR ", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NUMERO CEDULA DE CIUDADANÍA:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("DOCUMENTO O GUÍA TRANSPORTE", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("PRODUCTO", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("CANTIDAD A CARGAR (GLS)", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("ORIGEN / DESTINO", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("ENTURNADOR", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("CANT", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("ORDEN DE SERVICIO", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("INGRESO:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("RETIRO:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NAL", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("CONTROL ADUANERO:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("CLIENTE:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NIT:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("EMPRESA AUTORIZADA (SIA):", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NIT:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NOMBRE BARCAZA:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NOMBRE DEL REMOLCADOR:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NUMERO DE VIAJE:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("FECHA DE LLEGADA:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("MANIFIESTO:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("FECHA:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("DEC. DE IMPORTACIÓN:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("FECHA:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("LEVANTE:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("FECHA:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("NUMERO CONTENEDOR", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("LONGITUD", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("TIPO", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("TARA", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("PESO DECLARADO KG", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("CANTIDAD A CARGAR (UN)", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("IMO", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("PRECINTOS DE SEGURIDAD", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.DataColumn(
                    ft.Text("OBSERVACIONES:", text_align="center"),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
        )
        
        self.data_table_column = ft.Row([
            ft.Column([
                self.data_table,
                self.loading_indicator
            ], scroll=ft.ScrollMode.ALWAYS, on_scroll=self.handle_scroll)
        ],
        height=400,
        width='100%',
        scroll=ft.ScrollMode.ALWAYS)
                            

        self.content = ft.Column([
            self.go_home,
            self.cargar_excel,
            self.data_table_column
        ])
        
        self.cargar_anuncios_carga()
        
    @staticmethod
    def generate_anuncio_carga_id():
        # Two random uppercase letters
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        
        # Five random non-repeating digits
        digits = ''.join(random.sample(string.digits, 5))
        
        return letters + digits

    def handle_scroll(self, e):
        # Check if we've scrolled near the bottom
        if (not self.is_loading and 
            not self.all_loaded and 
            e.pixels >= e.max_scroll_extent * 0.8):
            self.load_more_data()
    
    def load_more_data(self):
        self.is_loading = True
        self.loading_indicator.visible = True
        self.page.update()
        
        # Calculate offset
        offset = self.current_page * self.page_size
        
        # Get next batch of records
        new_anuncios = self.control_anuncio_carga.obtener_anuncios_carga_paginados(
            limit=self.page_size, 
            offset=offset
        )
        
        if len(new_anuncios) < self.page_size:
            self.all_loaded = True
            
        if new_anuncios:
            self.current_page += 1
            self.add_rows_to_table(new_anuncios)
        
        self.is_loading = False
        self.loading_indicator.visible = False
        self.page.update()
        
    def ir_atras(self, _):
        self.page.go("/datos")

    def abrir_modal_cargar_excel(self, e):
        # Create a file picker
        self.file_picker = ft.FilePicker(on_result=self.upload_excel)
        self.page.overlay.append(self.file_picker)
        self.anunciar_button = ft.ElevatedButton("ANUNCIAR", 
            on_click=self.guardar_anuncio_carga,
            disabled=True  # Start as disabled
        )
        # Create the modal dialog without a predefined data table
        self.modal = ft.AlertDialog(
            title=ft.Text("Anunciar cargas", size=20, weight=ft.FontWeight.BOLD),
            icon=ft.IconButton(
                icon=ft.Icons.UPLOAD_FILE_ROUNDED,
                tooltip="Cargar archivo Excel",
                on_click=lambda _: self.file_picker.pick_files(
                    allowed_extensions=["xlsx", "xls"],
                    dialog_title="Seleccionar archivo Excel",
                ),
            ),
            content=ft.Row(
                controls=[
                    # Placeholder for dynamically created data table
                    ft.Container(
                        content=ft.Text("No se ha cargado ningún archivo"),
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                self.anunciar_button,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = self.modal
        self.modal.open = True
        self.page.update()

    def guardar_anuncio_carga(self, e):
        try:
            if not hasattr(self, 'df'):
                raise ValueError("No se ha cargado un archivo Excel")

            successful_records = []
            failed_records = []

            for _, row in self.df.iterrows():
                try:
                    # Convert date strings to datetime.date objects
                    fecha_anuncio = pd.Timestamp.now().date() 
                    fecha_programacion = pd.to_datetime(row.get('FECHA DE PROGRAMACIÓN DE CARGUE / DESCARGUE', pd.Timestamp.now())).date() if row.get('FECHA DE PROGRAMACIÓN DE CARGUE / DESCARGUE') else None

                    datos_anuncio = {
                        'id_anuncio_carga': self.generate_anuncio_carga_id(),
                        'fecha_anuncio': fecha_anuncio,
                        'cabezote': row.get('PLACA', ''),
                        'remolque': row.get('PLACA DE REMOLQUE', ''),
                        'nombre_conductor': row.get('NOMBRE DE CONDUCTOR', ''),
                        'numero_cedula': row.get('NÚMERO DE CÉDULA', ''),
                        'numero_contacto_conductor': row.get('NÚMERO DE CONTACTO', ''),
                        'empresa_de_transporte': row.get('EMPRESA TRANSPORTADORA', ''),
                        'nit_empresa': row.get('NIT', ''),
                        'tipo_vehiculo': row.get('TIPO DE VEHÍCULO', ''),
                        'cliente': row.get('CLIENTE/CONSIGNATARIO', ''),
                        'observaciones': row.get('PRODUCTO/REFERENCIA /PEDIDO O NUMERO DE CONTENEDOR', ''),
                        'precintos_de_seguridad': row.get('SELLOS', ''),
                        'cantidad_a_cargar': float(row.get('BULTOS', 0)),
                        'peso_declarado': float(row.get('PESO KGS', 0)),
                        'BL': row.get('BL', ''),
                        'fecha_programacion_cargue_descargue': fecha_programacion
                    }

                    nuevo_anuncio = self.control_anuncio_carga.crear_anuncio_carga(datos_anuncio)
                    successful_records.append(nuevo_anuncio)

                except Exception as record_error:
                    self.mostrar_mensaje(f"ERROR AL GUARDAR: {record_error}", es_error=True)
                    failed_records.append({
                        'row_data': row.to_dict(),
                        'error': str(record_error)
                    })
            # Provide feedback to the user
            if successful_records:
                self.mostrar_mensaje(f"Se guardaron {len(successful_records)} registros exitosamente."),
                self.cerrar_modal(e)

            if failed_records:
                self.mostrar_mensaje(f"Error al guardar: {str(e)}", es_error=True)

            if hasattr(self, 'df'):
                del self.df

            # Close the modal after processing
            self.cerrar_modal(e)
            self.cargar_anuncios_carga()
            self.page.update()

        except Exception:
            self.mostrar_mensaje("Selecciona un archivo Excel", es_error=True)
        
    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet."""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.Colors.RED if es_error else ft.Colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def cerrar_modal(self, e):
        # Clear the DataFrame
        if hasattr(self, 'df'):
            del self.df

        # Reset the modal content to its initial state
        self.modal.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("No se ha cargado ningún archivo"),
                )
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

        # Disable the anunciar button
        self.anunciar_button.disabled = True

        # Close the dialog
        self.page.dialog.open = False
        self.page.update()

    def upload_excel(self, e: ft.FilePickerResultEvent):
        if not e.files:
            print("no files uploaded")
            return

        try:
            # Read the Excel file starting from row 5 (index 4) to get headers
            self.df = pd.read_excel(e.files[0].path, header=3)
            self.anunciar_button.disabled = False
            # Print diagnostic information
            print("DataFrame Columns:", list(self.df.columns))
            print("DataFrame Shape:", self.df.shape)

            # Ensure all columns are strings and handle NaN values
            self.df = self.df.fillna("")
            self.df = self.df.astype(str)

            def format_date(date_value):
                try:
                    if pd.notna(date_value):
                        return pd.to_datetime(date_value).strftime("%d/%m/%Y")
                    return ""
                except Exception:
                    return str(date_value)

            # Dynamically create column list from the DataFrame
            display_columns = list(self.df.columns)

            # Dynamically create the data table for the modal
            data_table_modal = ft.DataTable(
                columns=[
                    ft.DataColumn(
                        ft.Text("ÍNDICE", text_align="center"),
                        heading_row_alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
                + [
                    ft.DataColumn(
                        ft.Text(col, text_align="center"),
                        heading_row_alignment=ft.MainAxisAlignment.CENTER,
                    )
                    for col in display_columns
                ],
                rows=[],
                vertical_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
                horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
            )

            # Populate the dynamic data table
            for index, row in self.df.iterrows():

                # Create a row for the modal DataTable
                # Use .get() method to safely handle missing columns
                row_cells = [
                    ft.DataCell(
                        ft.Text(str(index + 1), text_align=ft.TextAlign.CENTER)
                    ),
                ] + [
                    ft.DataCell(
                        ft.Text(
                            (
                                format_date(row.get(col, ""))
                                if "fecha" in col.lower()
                                else row.get(col, "")
                            ),
                            text_align=ft.TextAlign.CENTER,
                        )
                    )
                    for col in display_columns
                ]

                modal_row = ft.DataRow(cells=row_cells)
                data_table_modal.rows.append(modal_row)

                # Link the checkbox to the row

            # Update the modal content with the dynamically created table
            self.modal.content.controls[0] = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [data_table_modal],
                        )
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )

            # Force the modal to update and show the data
            self.page.dialog.open = True
            self.page.update()

        except Exception as ex:
            self.mostrar_mensaje("No se pudo cargar el excel", es_error=True)

    def add_rows_to_table(self, anuncios):
        start_index = len(self.data_table.rows)
        new_rows = []
        
        for index, anuncio in enumerate(anuncios, start=start_index):
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(anuncio.id_anuncio_carga, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.fecha_anuncio, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.cabezote, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.empresa_de_transporte, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nit_empresa, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.remolque, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.tipo_vehiculo, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nombre_conductor, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.numero_cedula, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.documento_guia_transporte, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.producto, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.cantidad_a_cargar_gls, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.origen_destino, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.enturnador, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.cant, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.orden_de_servicio, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.ingreso, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.retiro, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nal, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.control_aduanero, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.cliente, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nit_cliente, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.empresa_autorizada, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nit_empresa_autorizada, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nombre_barcaza, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.nombre_remolcador, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.numero_de_viaje, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.fecha_de_llegada, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.manifiesto, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.fecha_llegada, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.declaracion_importacion, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.fecha_declaracion, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.levante, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.fecha_levante, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.numero_contenedor, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.longitud, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.tipo_contenedor, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.tara, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.peso_declarado, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.cantidad_a_cargar, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.imo, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.precintos_de_seguridad, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(anuncio.observaciones, text_align=ft.TextAlign.CENTER)),
                    ]
                )
            )
        
        self.data_table.rows.extend(new_rows)
        
    def cargar_anuncios_carga(self):
        # Reset pagination
        self.current_page = 0
        self.all_loaded = False
        self.data_table.rows = []
        
        # Load initial data
        self.load_more_data()
        
                        