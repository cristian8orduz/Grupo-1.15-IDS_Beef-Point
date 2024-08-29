import tkinter as tk
from controllers.pedido_controller import get_detalle_by_pedido, confirmar_pedido, cancelar_pedido, get_pedido, update_pedido_info
import os

class ResumenPedidoView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Resumen del Pedido - Beef Point")
        self.geometry("500x500")
        self.configure(bg="#F0F0F0")  # Fondo suave

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id

        # Cargar información del pedido
        self.pedido = get_pedido(self.pedido_id)

        label_style = {"font": ("Arial", 14, "bold"), "bg": "#F0F0F0"}
        entry_style = {"font": ("Arial", 12), "bd": 2}
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
        self.resumen_frame.pack(pady=10)

        # Campos para editar información del cliente
        self.label_nombre_cliente = tk.Label(self, text="Nombre del Cliente:", **label_style)
        self.label_nombre_cliente.pack(pady=5)
        self.entry_nombre_cliente = tk.Entry(self, **entry_style)
        self.entry_nombre_cliente.insert(0, self.pedido.nombre_cliente)
        self.entry_nombre_cliente.pack(pady=5, fill=tk.X, padx=20)

        self.label_direccion = tk.Label(self, text="Dirección:", **label_style)
        self.label_direccion.pack(pady=5)
        self.entry_direccion = tk.Entry(self, **entry_style)
        self.entry_direccion.insert(0, self.pedido.direccion)
        self.entry_direccion.pack(pady=5, fill=tk.X, padx=20)

        self.label_contacto = tk.Label(self, text="Número de Contacto:", **label_style)
        self.label_contacto.pack(pady=5)
        self.entry_contacto = tk.Entry(self, **entry_style)
        self.entry_contacto.insert(0, self.pedido.numero_contacto)
        self.entry_contacto.pack(pady=5, fill=tk.X, padx=20)

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
        # Actualizar la información del pedido con los datos editados
        nombre_cliente = self.entry_nombre_cliente.get()
        direccion = self.entry_direccion.get()
        numero_contacto = self.entry_contacto.get()

        update_pedido_info(self.pedido_id, nombre_cliente, direccion, numero_contacto)

        confirmar_pedido(self.pedido_id)
        tk.messagebox.showinfo("Éxito", "Pedido confirmado.")
        self.destroy()

    def cancelar_pedido(self):
        cancelar_pedido(self.pedido_id)
        tk.messagebox.showinfo("Información", "Pedido cancelado.")
        self.destroy()
