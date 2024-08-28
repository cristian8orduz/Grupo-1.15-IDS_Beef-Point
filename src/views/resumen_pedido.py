# src/views/resumen_pedido.py
import tkinter as tk
from controllers.pedido_controller import get_detalle_by_pedido, confirmar_pedido, cancelar_pedido
import os

class ResumenPedidoView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Resumen del Pedido")
        self.geometry("400x400")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id

        self.label_resumen = tk.Label(self, text="Resumen del Pedido")
        self.label_resumen.pack(pady=10)

        self.resumen_frame = tk.Frame(self)
        self.resumen_frame.pack(pady=20)

        self.mostrar_resumen()

        self.button_confirmar = tk.Button(self, text="Confirmar Pedido", command=self.confirmar_pedido)
        self.button_confirmar.pack(pady=10)

        self.button_cancelar = tk.Button(self, text="Cancelar Pedido", command=self.cancelar_pedido)
        self.button_cancelar.pack(pady=10)

    def mostrar_resumen(self):
        detalles = get_detalle_by_pedido(self.pedido_id)

        for widget in self.resumen_frame.winfo_children():
            widget.destroy()

        for detalle in detalles:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            label = tk.Label(self.resumen_frame, text=f"{categoria_nombre} - {producto_nombre} (ID: {producto_id}) x {cantidad}")
            label.pack()

    def confirmar_pedido(self):
        confirmar_pedido(self.pedido_id)  # Actualiza el estado del pedido en la base de datos
        tk.messagebox.showinfo("Éxito", "Pedido confirmado.")
        self.destroy()

    def cancelar_pedido(self):
        cancelar_pedido(self.pedido_id)  # Actualiza el estado del pedido a 'Cancelado'
        tk.messagebox.showinfo("Información", "Pedido cancelado.")
        self.destroy()
