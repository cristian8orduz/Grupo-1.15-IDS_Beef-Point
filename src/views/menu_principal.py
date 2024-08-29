import tkinter as tk
from views.pedido import PedidoView
from views.resumen_pedido import ResumenPedidoView
from controllers.pedido_controller import get_pedidos_pendientes
from views.historial_pedidos import HistorialPedidosView
from views.login import LoginView 
from views.pedido_domicilio import PedidoDomicilioView
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
            "font": ("Helvetica", 14, "bold"),
            "bg": "#1ABC9C",  # Color verde agua moderno
            "fg": "white",  # Color de texto blanco
            "activebackground": "#16A085",
            "bd": 0,
            "relief": "flat",
            "width": 25,
            "height": 2,
            "cursor": "hand2"
        }

        self.button_nuevo_pedido = tk.Button(button_frame, text="Nuevo Pedido", command=self.nuevo_pedido, **button_style)
        self.button_nuevo_pedido.pack(pady=10)

        self.button_pedido_domicilio = tk.Button(button_frame, text="Nuevo Pedido a Domicilio", command=self.pedido_domicilio, **button_style)
        self.button_pedido_domicilio.pack(pady=10)

        self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
        self.button_historial_pedidos.pack(pady=10)

        self.button_cerrar_sesion = tk.Button(button_frame, text="Cerrar Sesión", command=self.cerrar_sesion, **button_style)
        self.button_cerrar_sesion.pack(pady=10)

        # Barra inferior con la información del usuario
        footer_frame = tk.Frame(self, bg="#34495E")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.label_usuario = tk.Label(footer_frame, text=f"Usuario: {self.trabajador.nombre}", font=("Helvetica", 10), bg="#34495E", fg="white")
        self.label_usuario.pack(pady=5, padx=10, anchor="w")

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

    def cerrar_sesion(self):
        self.destroy()  # Cierra la ventana del menú principal
        LoginView(self.master)  # Abre la ventana de inicio de sesión nuevamente
