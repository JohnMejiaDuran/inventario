import flet as ft
from controllers.control_anuncio_carga import ControlAnuncioCarga
from controllers.control_cliente import ControlCliente
from controllers.control_minas import ControlMina
from controllers.control_lote import ControlLote
from components.go_home import create_home_button
from controllers.control_transportadores import ControlTransportador
from controllers.control_productos import ControlProducto
from controllers.control_tipo_producto import  ControlTipoProducto

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
        self.insert_cliente = ft.Dropdown(
            label="Selecciona un cliente",
            options=[
                ft.dropdown.Option(cliente.nombre_cliente)
                for cliente in self.controlador_cliente.obtener_clientes()
                if cliente.estado
            ],
                on_change=self.actualizar_minas,
                expand=True
            )
        self.insert_mina = ft.Dropdown(
            label="Selecciona una mina",
            on_change=self.actualizar_lotes,
            expand=True
            )
        self.insert_lote = ft.Dropdown(label="Selecciona un lote",expand=True)
        self.insert_placa_contenedor = ft.TextField(label="Placa o contenedor",expand=True)
        self.transportador = ft.Dropdown(
            label="Selecciona un transportador",
            options=[
                ft.dropdown.Option(transportador.nombre_transportador)
                for transportador in self.controlador_transportador.obtener_transportadores()
                if transportador.estado_transportador
            ],
            expand=True
        )
        self.insert_producto = ft.Dropdown(
            label="Selecciona un producto",
            options=[
                ft.dropdown.Option(producto.nombre_producto)
                for producto in self.controlador_producto.obtener_productos()
                if producto.estado_producto
            ],
            expand=True)
        self.insert_tipo_producto = ft.Dropdown(
            label="Selecciona un tipo de producto",
            options=[
                ft.dropdown.Option(tipo_producto.nombre_tipo_producto)
                for tipo_producto in self.controlador_tipo_producto.obtener_tipo_productos()
                if tipo_producto.estado_tipo_producto
                ],
            expand=True)
        self.insert_tipo_unidad = ft.Dropdown(
            label="Selecciona un tipo de unidad",
            options=[
                ft.dropdown.Option("BIG BAG"),
                ft.dropdown.Option("CONTENEDORES"),
                ft.dropdown.Option("CARGA GENERAL"),
                ft.dropdown.Option("PALLETS")
            ],
            expand=True)
        self.insert_unidades_anunciadas = ft.TextField(label="Unidades anunciadas",expand=True)
        self.insert_peso_anunciado = ft.TextField(label="Peso anunciado",expand=True)
        self.data_table = ft.DataTable(
            width=float('inf'),
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("No. Servicio"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Mina"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Transportador"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Producto", ), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Tipo Producto"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Tipo unidad"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Unidades \n anunciadas", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Peso \n anunciado", text_align="center"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
            ],
            rows=[],
            vertical_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
            horizontal_lines=ft.BorderSide(width=1, color=ft.colors.GREY_300),
        )
        self.content = ft.Column(
            controls=[
                self.go_home,
                ft.Text("Anunciar carga", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=
                        ft.Row([
                            self.insert_cliente,
                            self.insert_mina,
                            self.insert_lote
                            ],
                            alignment=ft.MainAxisAlignment.CENTER 
                        ),
                    ),
                ft.Container(
                    content=
                        ft.Row([
                            self.insert_placa_contenedor,
                            self.transportador
                            ],
                            alignment=ft.MainAxisAlignment.CENTER 
                        ),
                    ),
                ft.Container(
                    content=
                        ft.Row([
                            self.insert_producto,
                            self.insert_tipo_producto
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ),
                ft.Container(
                    content=
                        ft.Row([
                            self.insert_tipo_unidad,
                            self.insert_unidades_anunciadas,
                            self.insert_peso_anunciado
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ),
                ft.ElevatedButton("Anunciar carga"),
                ft.Column([
                    self.data_table
                ])
            ],
        )
    def ir_atras(self, _):
        self.page.go("/datos")
        
    def mostrar_mensaje(self, mensaje, es_error=False):
        """Muestra un mensaje utilizando el método de overlay de Flet."""
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.RED if es_error else ft.colors.GREEN
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
        
    def actualizar_minas(self, e):
        """Al seleccionar un cliente me trae sus minas """
        cliente_seleccionado = self.insert_cliente.value
        self.insert_mina.options = []
        # obtener la mina del cliente seleccionado
        minas = self.controlador_mina.obtener_minas()
        minas = [mina for mina in minas if mina.id_cliente == cliente_seleccionado]
        if minas: 
            self.insert_mina.options = [
                ft.dropdown.Option(mina.nombre_mina) for mina in minas
                if mina.estado 
            ]
        self.page.update()
        
    def actualizar_lotes(self, e):
        """Al seleccionar la mina del cliente me trae sus lotes"""
        mina_seleccionada = self.insert_mina.value
        self.insert_lote.options = []
        # obtener la mina del cliente seleccionado
        lotes = self.controlador_lotes.obtener_lotes()
        lotes = [lote for lote in lotes if lote.id_mina == mina_seleccionada]
        if lotes: 
            self.insert_lote.options = [
                ft.dropdown.Option(lote.nombre_lote) for lote in lotes
            ]
        self.page.update()
        
    def guardar_anuncio(self, _):
        """Guardar anuncio de carga"""
        datos = {
            "id_cliente": self.insert_cliente.value,
            "id_mina": self.insert_mina.value,
            "id_lote": self.insert_lote.value,
            "placa_contenedor": self.insert_placa_contenedor.value,
            "id_transportador": self.transportador.value,
            "id_producto": self.insert_producto.value,
            "id_tipo_producto": self.insert_tipo_producto.value,
            "tipo_unidad": self.insert_tipo_unidad.value,
            "unidades_anunciadas": self.insert_unidades_anunciadas.value,
            "peso_anunciado": self.insert_peso_anunciado.value,
        }
        try:
            self.control_anuncio_carga.crear_anuncio_carga(datos)
            self.mostrar_mensaje("Anuncio de carga guardado correctamente")
            self.insert_placa_contenedor.value = ""
            self.insert_unidades_anunciadas.value = ""
            self.insert_peso_anunciado.value = ""
            self.page.update()
        except ValueError as e:
            self.mostrar_mensaje(str(e), es_error=True)
            self.page.update()