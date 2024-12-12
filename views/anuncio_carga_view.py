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

        self.content = ft.Column(
            controls=[
                self.go_home,
                self.cargar_excel,
                ft.Text("Cargas Anunciadas", size=20, weight=ft.FontWeight.BOLD),
                ft.Column(
                    controls=[
                        ft.Row([self.data_table], scroll=ft.ScrollMode.ADAPTIVE),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
            ],
        )
        
    @staticmethod
    def generate_anuncio_carga_id():
        # Two random uppercase letters
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        
        # Five random non-repeating digits
        digits = ''.join(random.sample(string.digits, 5))
        
        return letters + digits

    def ir_atras(self, _):
        self.page.go("/datos")

    def abrir_modal_cargar_excel(self, e):
        # Create a file picker
        self.file_picker = ft.FilePicker(on_result=self.upload_excel)
        self.page.overlay.append(self.file_picker)
        self.page.update()
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
                ft.ElevatedButton("ANUNCIAR", on_click=self.guardar_anuncio_carga),
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

            # Close the modal after processing
            self.cerrar_modal(e)
            self.page.update()

        except Exception as ex:
            # Handle any unexpected errors
            error_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"Error al guardar los registros: {ex}"),
                actions=[
                    ft.TextButton("Cerrar", on_click=self.cerrar_dialog)
                ]
            )
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()
        
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
        self.page.dialog.open = False
        self.page.update()


    def upload_excel(self, e: ft.FilePickerResultEvent):
        if not e.files:
            print("no files uploaded")
            return

        try:
            # Read the Excel file starting from row 5 (index 4) to get headers
            self.df = pd.read_excel(e.files[0].path, header=3)

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
            # Handle any errors during file upload or data processing
            print(f"Error uploading Excel file: {ex}")
            import traceback

            traceback.print_exc()  # This will print the full stack trace

            # Show an error dialog to the user
            error_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"No se pudo cargar el archivo Excel: {ex}"),
            )
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()

    # def cargar_anuncios_carga(self):
    #     anuncios_carga = self.control_anuncio_carga.obtener_anuncios_carga()
    #     rows = []
    #     for index, anuncio in enumerate(anuncios_carga):
    #         rows.append(
    #             ft.DataRow(
    #                 cells=[
    #                     ft.DataCell(ft.Text(str(index + 1), text_align=ft.TextAlign.CENTER)),
    #                     ft.DataCell(ft.Text(anuncio.fecha_anuncio, text_align=ft.TextAlign.CENTER)),
    #                     ft.DataCell(ft.Text(anuncio.cabezote, text_align=ft.TextAlign.CENTER)),
    #                     ft.DataCell(ft.Text