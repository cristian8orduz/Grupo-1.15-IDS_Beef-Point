# src/views/pedido_domicilio.py
import tkinter as tk
from controllers.pedido_controller import create_pedido
from views.producto_seleccion import ProductoSeleccionView
import os

class PedidoDomicilioView(tk.Toplevel):
    def __init__(self, parent, trabajador):
        super().__init__(parent)
        self.title("Nuevo Pedido a Domicilio")
        self.geometry("400x300")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        self.label_direccion = tk.Label(self, text="Dirección:")
        self.label_direccion.pack(pady=5)
        self.entry_direccion = tk.Entry(self)
        self.entry_direccion.pack(pady=5)

        self.label_contacto = tk.Label(self, text="Número de Contacto:")
        self.label_contacto.pack(pady=5)
        self.entry_contacto = tk.Entry(self)
        self.entry_contacto.pack(pady=5)

        self.button_crear_pedido = tk.Button(self, text="Crear Pedido", command=self.crear_pedido)
        self.button_crear_pedido.pack(pady=20)

    def crear_pedido(self):
        direccion = self.entry_direccion.get()
        numero_contacto = self.entry_contacto.get()

        if direccion and numero_contacto:
            pedido_id = create_pedido(None, self.trabajador.id, "Pendiente", direccion, numero_contacto)
            self.destroy()
            ProductoSeleccionView(self.master, pedido_id)
        else:
            tk.messagebox.showerror("Error", "Debe ingresar todos los datos de domicilio.")
