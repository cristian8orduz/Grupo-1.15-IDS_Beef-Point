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
        self.geometry("600x400")
        self.configure(bg="#F0F0F0")  # Color de fondo suave

        # Centrar la ventana
        self.center_window()
        
        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        # Crear un frame para organizar los botones
        button_frame = tk.Frame(self, bg="#F0F0F0")
        button_frame.pack(expand=True)

        button_style = {
            "font": ("Arial", 14, "bold"),
            "bg": "#4CAF50",  # Color verde suave
            "fg": "white",  # Color de texto blanco
            "activebackground": "#45A049",
            "bd": 0,
            "relief": "flat",
            "width": 25,
            "height": 2
        }

        self.button_nuevo_pedido = tk.Button(button_frame, text="Nuevo Pedido", command=self.nuevo_pedido, **button_style)
        self.button_nuevo_pedido.pack(pady=10)

        self.button_pedido_domicilio = tk.Button(button_frame, text="Nuevo Pedido a Domicilio", command=self.pedido_domicilio, **button_style)
        self.button_pedido_domicilio.pack(pady=10)

        self.button_historial_pedidos = tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, **button_style)
        self.button_historial_pedidos.pack(pady=10)

        self.button_cerrar_sesion = tk.Button(button_frame, text="Cerrar Sesión", command=self.cerrar_sesion, **button_style)
        self.button_cerrar_sesion.pack(pady=10)

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
