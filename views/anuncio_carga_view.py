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
                ft.DataColumn(ft.Text("FECHA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CABEZOTE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("EMPRESA DE TRANSPORTE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NIT:",text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("REMOLQUE:",text_align="center" ), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NOMBRE DEL CONDUCTOR ", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NUMERO CEDULA DE CIUDADANÍA:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("DOCUMENTO O GUÍA TRANSPORTE", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PRODUCTO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CANTIDAD A CARGAR (GLS)", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("ORIGEN / DESTINO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("ENTURNADOR", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CANT", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("ORDEN DE SERVICIO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("INGRESO:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("RETIRO:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NAL", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CONTROL ADUANERO:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CLIENTE:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NIT:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("EMPRESA AUTORIZADA (SIA):", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NIT:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NOMBRE BARCAZA:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NOMBRE DEL REMOLCADOR:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NUMERO DE VIAJE:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA DE LLEGADA:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("MANIFIESTO:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("DEC. DE IMPORTACIÓN:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("LEVANTE:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("FECHA:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("NUMERO CONTENEDOR", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("LONGITUD", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TIPO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("TARA", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PESO DECLARADO KG", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("CANTIDAD A CARGAR (UN)", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("IMO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("PRECINTOS DE SEGURIDAD", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("OBSERVACIONES:", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER)
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
                               scroll=ft.ScrollMode.ADAPTIVE),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                    scroll=ft.ScrollMode.ADAPTIVE
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

        # Create the modal dialog without a predefined data table
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
                    # Placeholder for dynamically created data table
                    ft.Container(
                        content=ft.Text("No se ha cargado ningún archivo"),
                        padding=20
                    )
                ],
                height=1000,
                width=1200,
                scroll=ft.ScrollMode.ALWAYS
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
        Upload an Excel file and create a dynamic data table in the modal
        
        :param e: Flet FilePickerResultEvent containing the uploaded file
        """
        if not e.files:
            print("no files uploaded")
            return

        try:
            # Read the Excel file starting from row 5 (index 4) to get headers
            df = pd.read_excel(e.files[0].path, header=3)
            
            # Ensure all columns are strings and handle NaN values
            df = df.fillna('')
            df = df.astype(str)
            
            def format_date(date_value):
                try:
                    # Convert to datetime if it's not already
                    if pd.notna(date_value):
                        # Convert to datetime and format as dd/mm/yyyy
                        return pd.to_datetime(date_value).strftime('%d/%m/%Y')
                    return ''
                except Exception:
                    return str(date_value)

            # Dynamically create column list from the DataFrame
            display_columns = list(df.columns)

            # Dynamically create the data table for the modal
            data_table_modal = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Índice", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                    ft.DataColumn(ft.Text("INGRESO/RETIRO", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER)
                ] + [
                    ft.DataColumn(
                        ft.Text(col, text_align="center"), 
                        heading_row_alignment=ft.MainAxisAlignment.CENTER
                    ) for col in display_columns
                ],
                rows=[],
                vertical_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300),
                horizontal_lines=ft.BorderSide(width=1, color=ft.Colors.GREY_300)
            )

            # Populate the dynamic data table
            for index, row in df.iterrows():
                # Checkbox for ingreso/retiro
                ingreso_checkbox = ft.Checkbox(
                    label="INGRESO",
                    value=True,
                    on_change=lambda e, checkbox=None: self.toggle_ingreso_type(e, checkbox)
                )

                # Create a row for the modal DataTable
                row_cells = [
                    ft.DataCell(ft.Text(str(index + 1), text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ingreso_checkbox)
                ] + [
                    ft.DataCell(ft.Text(
                        format_date(row[col]) if 'fecha' in col.lower() else row[col], 
                        text_align=ft.TextAlign.CENTER
                    )) 
                    for col in display_columns
                ]

                modal_row = ft.DataRow(cells=row_cells)
                data_table_modal.rows.append(modal_row)
                
                # Link the checkbox to the row
                ingreso_checkbox.data = {'row': modal_row}

            # Update the modal content with the dynamically created table
            self.modal.content.controls[1] = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [data_table_modal],
                            scroll=ft.ScrollMode.ALWAYS
                        )
                    ]
                )
            )
            
            # Force the modal to update and show the data
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
        
    
    def toggle_ingreso_type(self, e, checkbox=None):
        """
        Toggle between INGRESO and RETIRO when checkbox is checked/unchecked
        
        :param e: Flet event
        :param checkbox: Optional checkbox to toggle (used if not passed via event)
        """
        # Use the event's control if no checkbox is provided
        target_checkbox = checkbox or e.control
        
        # Update checkbox label based on state
        if target_checkbox.value:
            target_checkbox.label = "INGRESO"
        else:
            target_checkbox.label = "RETIRO"
        
        # Update the page to reflect changes
        self.page.update()