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
        self.title("Menú Principal")
        self.geometry("600x400")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        self.button_nuevo_pedido = tk.Button(self, text="Nuevo Pedido", command=self.nuevo_pedido)
        self.button_nuevo_pedido.pack(pady=10)

        self.button_pedido_domicilio = tk.Button(self, text="Nuevo Pedido a Domicilio", command=self.pedido_domicilio)
        self.button_pedido_domicilio.pack(pady=10)

        self.button_historial_pedidos = tk.Button(self, text="Ver Historial", command=self.ver_historial)
        self.button_historial_pedidos.pack(pady=10)

        self.button_cerrar_sesion = tk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion)
        self.button_cerrar_sesion.pack(pady=10)

    def nuevo_pedido(self):
        PedidoView(self, self.trabajador)

    def pedido_domicilio(self):
        PedidoDomicilioView(self, self.trabajador)

    def ver_historial(self):
            HistorialPedidosView(self)

    def cerrar_sesion(self):
        self.destroy()  # Cierra la ventana del menú principal
        LoginView(self.master)  # Abre la ventana de inicio de sesión nuevamente

    def ver_pedidos(self):
        pedidos_pendientes = get_pedidos_pendientes()
        if pedidos_pendientes:
            PedidoView(self, pedidos_pendientes)
        else:
            tk.messagebox.showinfo("Información", "No hay pedidos pendientes.")
