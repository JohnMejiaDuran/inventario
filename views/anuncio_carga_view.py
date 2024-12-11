import flet as ft
from controllers.control_anuncio_carga import ControlAnuncioCarga
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from components.go_home import create_home_button
from controllers.control_transportadores import ControlTransportador
from controllers.control_productos import ControlProducto
from controllers.control_tipo_producto import  ControlTipoProducto
import pandas as pd

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

        self.go_home = create_home_button(page, lambda _: page.go("/"))
        self.cargar_excel = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            tooltip="Cargar archivo excel",
            on_click=self.abrir_modal_cargar_excel
        )
        
        self.data_table = ft.DataTable(
            
            columns=[
                ft.DataColumn(ft.Text("#", text_align="center")),
                ft.DataColumn(ft.Text("PLACA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PLACA DE\nREMOLQUE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NOMBRE DE\nCONDUCTOR",text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NÚMERO DE\nCÉDULA",text_align="center" ), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NÚMERO DE\nCONTACTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("EMPRESA\nTRANSPORTADORA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NIT", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO DE\nVEHÍCULO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CLIENTE/\nCONSIGNATARIO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BL", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PRODUCTO/REFERENCIA \n /PEDIDO O NÚMERO DE \n CONTENEDOR", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("SELLOS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BULTOS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PESO KGS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA DE\nPROGRAMACIÓN DE\n CARGA / DESCARGUE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
        )
        
        self.data_table_modal = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("INGRESO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PLACA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PLACA\nREMOLQUE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NOMBRE DE\nCONDUCTOR", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NÚMERO\nDE CÉDULA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NÚMERO\nDE CONTACTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("EMPRESA\nTRANSPORTADORA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NIT", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO DE\nVEHÍCULO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CLIENTE/\nCONSIGNATARIO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BL", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PRODUCTO/REFERENCIA\n/PEDIDO O NÚMERO\nDE CONTENEDOR", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("SELLOS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("BULTOS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PESO KGS", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA DE\nPROGRAMACIÓN DE\nCARGA/DESCARGUE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
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
                        ft.Row([
                            self.data_table
                        ],
                               scroll=ft.ScrollMode.ALWAYS),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                    scroll=ft.ScrollMode.ALWAYS
                ),
                
            ],
            
        )
    def ir_atras(self, _):
        self.page.go("/datos")
        
    def abrir_modal_cargar_excel(self, e):
        # Create a file picker
        self.file_picker = ft.FilePicker(on_result=self.upload_excel)
        self.page.overlay.append(self.file_picker)
        self.page.update()

        # Create the modal dialog
        self.modal = ft.AlertDialog(
            title=ft.Text("Anunciar cargas", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.UPLOAD_FILE_ROUNDED,
                        tooltip="Cargar archivo Excel",
                        on_click=lambda _: self.file_picker.pick_files(
                            allowed_extensions=["xlsx", "xls"],
                            dialog_title="Seleccionar archivo Excel"
                        )
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                [
                                    self.data_table_modal
                                ],
                                scroll=ft.ScrollMode.ALWAYS
                            )
                        ],
                        height=400,
                    )
                ],
                height=1000,
                width=1200,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_modal),
                ft.ElevatedButton("Guardar")
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = self.modal
        self.modal.open = True
        self.page.update()
        
    def cerrar_modal(self, e):
        self.page.dialog.open = False
        self.page.update()
        
    def upload_excel(self, e: ft.FilePickerResultEvent):
        """
        Upload an Excel file and populate both the modal's and main data tables
        
        :param e: Flet FilePickerResultEvent containing the uploaded file
        """
        if not e.files:
            print("no files uploaded")
            return

        try:
            # Read the Excel file starting from row 5 (index 4) to get headers
            df = pd.read_excel(e.files[0].path, header=3)
            print("Original columns:", list(df.columns))
            
            # Define a mapping of desired display columns to potential Excel headers
            column_mapping = {
                'PLACA': ['PLACA', 'Placa', 'placa'],
                'PLACA DE REMOLQUE': ['PLACA DE REMOLQUE', 'Placa de Remolque', 'placa de remolque'],
                'NOMBRE DE CONDUCTOR': ['NOMBRE DE CONDUCTOR', 'Nombre de Conductor', 'nombre de conductor'],
                'NÚMERO DE CÉDULA': ['NÚMERO DE CÉDULA', 'Número de Cédula', 'número de cédula'],
                'NÚMERO DE CONTACTO': ['NÚMERO DE CONTACTO', 'Número de Contacto', 'número de contacto'],
                'EMPRESA TRANSPORTADORA': ['EMPRESA TRANSPORTADORA', 'Empresa Transportadora', 'empresa transportadora'],
                'NIT': ['NIT', 'Nit', 'nit'],
                'TIPO DE VEHÍCULO': ['TIPO DE VEHÍCULO', 'Tipo de Vehículo', 'tipo de vehículo'],
                'CLIENTE/CONSIGNATARIO': ['CLIENTE/CONSIGNATARIO', 'Cliente/Consignatario', 'cliente/consignatario'],
                'BL': ['BL', 'Bl', 'bl'],
                'PRODUCTO/REFERENCIA /PEDIDO O NUMERO DE CONTENEDOR': [
                    'PRODUCTO/REFERENCIA /PEDIDO O NUMERO DE CONTENEDOR', 
                    'Producto/Referencia/ Pedido o Numero de Contenedor',
                    'producto/referencia/ pedido o numero de contenedor'
                ],
                'SELLOS': ['SELLOS', 'Sellos', 'sellos'],
                'BULTOS': ['BULTOS', 'Bultos', 'bultos'],
                'PESO KGS': ['PESO KGS', 'Peso Kgs', 'peso kgs'],
                'FECHA DE PROGRAMACIÓN DE CARGUE / DESCARGUE': [
                    'FECHA DE PROGRAMACIÓN DE CARGUE / DESCARGUE', 
                    'Fecha de Programación de cargue / Descargue',
                    'fecha de programación de cargue / descargue'
                ]
            }
            
            # Find the actual column names in the Excel file
            display_columns = {}
            for display_col, possible_headers in column_mapping.items():
                # Find the first matching header
                matching_header = next((col for col in df.columns if col in possible_headers), None)
                
                if matching_header:
                    display_columns[display_col] = matching_header
                else:
                    print(f"Warning: No match found for {display_col}")
                    display_columns[display_col] = ''
            
            # Ensure all columns are strings and handle NaN values
            df = df.fillna('')
            df = df.astype(str)
            
            # Clear existing rows in both tables
            self.data_table_modal.rows.clear()
            
            # Populate both the modal and main data tables
            for index, row in df.iterrows():
                # Create a row for the modal DataTable
                modal_row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1), text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Checkbox(value=True))]+
                    [
                        ft.DataCell(ft.Text(
                            row.get(display_columns.get(col, ''), ''),
                            text_align=ft.TextAlign.CENTER
                        )) 
                        for col in column_mapping.keys()
                    ]
                )
                self.data_table_modal.rows.append(modal_row)
                
                # Create a row for the main DataTable with an index column
                main_row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index + 1), text_align=ft.TextAlign.CENTER)),  # Index column
                    ] + [
                        ft.DataCell(ft.Text(
                            row.get(display_columns.get(col, ''), ''), 
                            text_align=ft.TextAlign.CENTER
                        )) 
                        for col in column_mapping.keys()
                    ]
                )

            
            # Force the modal to update and show the data
            self.page.dialog.content.controls[1].controls[0].content = self.data_table_modal
            self.page.dialog.open = True
            self.page.update()
        
        except Exception as ex:
            # Handle any errors during file upload or data processing
            print(f"Error uploading Excel file: {ex}")
            # Show an error dialog to the user
            error_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"No se pudo cargar el archivo Excel: {ex}")
            )
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()