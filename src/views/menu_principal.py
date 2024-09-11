import tkinter as tk
from views.pedido import PedidoView
from views.resumen_pedido import ResumenPedidoView
from controllers.pedido_controller import get_pedidos_pendientes
from views.historial_pedidos import HistorialPedidosView
from views.login import LoginView 
from views.pedido_domicilio import PedidoDomicilioView
from views.admin_productos import AdminProductosView
from views.admin_trabajadores import AdminTrabajadoresView
import os

class MenuPrincipalView(tk.Toplevel):
    def __init__(self, parent, trabajador):
        super().__init__(parent)
        self.title("Menú Principal - Beef Point")
        self.geometry("500x400")
        self.configure(bg="#2C3E50")  # Fondo oscuro profesional

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        # Crear un marco superior para el título y logo
        header_frame = tk.Frame(self, bg="#34495E")
        header_frame.pack(fill=tk.X)

        self.label_logo = tk.Label(header_frame, text="Beef Point", font=("Helvetica", 20, "bold"), bg="#34495E", fg="white")
        self.label_logo.pack(pady=10)

        # Crear un marco para organizar los botones
        button_frame = tk.Frame(self, bg="#2C3E50")
        button_frame.pack(expand=True)

        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#218ff9",  # Color verde agua moderno
            "fg": "white",  # Color de texto blanco
            "activebackground": "#1b6dbc",
            "bd": 0,
            "relief": "flat",
            "width": 25,
            "height": 1,
            "cursor": "hand2"
        }

        # Mostrar botones según el rol del trabajador
        if self.trabajador.rol == 'Mesero':
            self.button_nuevo_pedido = tk.Button(button_frame, text="Nuevo Pedido", command=self.nuevo_pedido, **button_style)
            self.button_nuevo_pedido.pack(pady=10)

            self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
            self.button_historial_pedidos.pack(pady=10)

        elif self.trabajador.rol == 'Auxiliar Cocina':
            self.button_pedido_domicilio = tk.Button(button_frame, text="Nuevo Pedido a Domicilio", command=self.pedido_domicilio, **button_style)
            self.button_pedido_domicilio.pack(pady=10)

            self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
            self.button_historial_pedidos.pack(pady=10)

        elif self.trabajador.rol == 'Administrador':
            self.button_nuevo_pedido = tk.Button(button_frame, text="Nuevo Pedido", command=self.nuevo_pedido, **button_style)
            self.button_nuevo_pedido.pack(pady=10)

            self.button_pedido_domicilio = tk.Button(button_frame, text="Nuevo Pedido a Domicilio", command=self.pedido_domicilio, **button_style)
            self.button_pedido_domicilio.pack(pady=10)

            self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
            self.button_historial_pedidos.pack(pady=10)

            self.button_admin_productos = tk.Button(button_frame, text="Administrar Productos", command=self.admin_productos, **button_style)
            self.button_admin_productos.pack(pady=10)

            self.button_admin_trabajadores = tk.Button(button_frame, text="Administrar Trabajadores", command=self.admin_trabajadores, **button_style)
            self.button_admin_trabajadores.pack(pady=10)

        elif self.trabajador.rol in ['Chef', 'Domiciliario']:
            self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
            self.button_historial_pedidos.pack(pady=10)

        elif self.trabajador.rol == 'Co-propietario':
            self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
            self.button_historial_pedidos.pack(pady=10)

            self.button_admin_productos = tk.Button(button_frame, text="Administrar Productos", command=self.admin_productos, **button_style)
            self.button_admin_productos.pack(pady=10)

            self.button_admin_trabajadores = tk.Button(button_frame, text="Administrar Trabajadores", command=self.admin_trabajadores, **button_style)
            self.button_admin_trabajadores.pack(pady=10)
            
        # Barra inferior con la información del usuario y su rol
        footer_frame = tk.Frame(self, bg="#34495E")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Mostrar el nombre y rol del trabajador logeado
        self.label_usuario = tk.Label(footer_frame, text=f"Usuario: {self.trabajador.nombre} | Rol: {self.trabajador.rol}", font=("Helvetica", 10), bg="#34495E", fg="white")
        self.label_usuario.pack(side=tk.LEFT, pady=5, padx=10)

        self.button_cerrar_sesion = tk.Button(footer_frame, text="Cerrar Sesión", command=self.cerrar_sesion, font=("Helvetica", 10, "bold"), bg="#E74C3C", fg="white", relief="flat", cursor="hand2")
        self.button_cerrar_sesion.pack(side=tk.RIGHT, pady=5, padx=10)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def nuevo_pedido(self):
        PedidoView(self, self.trabajador)

    def pedido_domicilio(self):
        PedidoDomicilioView(self, self.trabajador)

    def ver_historial(self):
        HistorialPedidosView(self)

    def admin_productos(self):
        AdminProductosView(self)

    def admin_trabajadores(self):
        AdminTrabajadoresView(self)

    def cerrar_sesion(self):
        self.destroy()  # Cierra la ventana del menú principal
        LoginView(self.master)  # Abre la ventana de inicio de sesión nuevamente
