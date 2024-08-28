import tkinter as tk
from controllers.pedido_controller import get_detalle_by_pedido, confirmar_pedido, cancelar_pedido
import os

class ResumenPedidoView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Resumen del Pedido - Beef Point")
        self.geometry("500x400")
        self.configure(bg="#F0F0F0")  # Fondo suave

        # Centrar la ventana
        self.center_window()
        
        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id

        label_style = {"font": ("Arial", 14, "bold"), "bg": "#F0F0F0"}
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#45A049",
            "bd": 0,
            "relief": "flat",
            "width": 20,
            "height": 2
        }

        self.label_resumen = tk.Label(self, text="Resumen del Pedido", **label_style)
        self.label_resumen.pack(pady=10)

        self.resumen_frame = tk.Frame(self, bg="#F0F0F0")
        self.resumen_frame.pack(pady=20)

        self.mostrar_resumen()

        self.button_confirmar = tk.Button(self, text="Confirmar Pedido", command=self.confirmar_pedido, **button_style)
        self.button_confirmar.pack(pady=10)

        self.button_cancelar = tk.Button(self, text="Cancelar Pedido", command=self.cancelar_pedido, **button_style)
        self.button_cancelar.pack(pady=10)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_resumen(self):
        detalles = get_detalle_by_pedido(self.pedido_id)

        for widget in self.resumen_frame.winfo_children():
            widget.destroy()

        for detalle in detalles:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            label = tk.Label(self.resumen_frame, text=f"{categoria_nombre} - {producto_nombre} x {cantidad}", font=("Arial", 12), bg="#F0F0F0")
            label.pack(anchor="w")

    def confirmar_pedido(self):
        confirmar_pedido(self.pedido_id)
        tk.messagebox.showinfo("Éxito", "Pedido confirmado.")
        self.destroy()

    def cancelar_pedido(self):
        cancelar_pedido(self.pedido_id)
        tk.messagebox.showinfo("Información", "Pedido cancelado.")
        self.destroy()
