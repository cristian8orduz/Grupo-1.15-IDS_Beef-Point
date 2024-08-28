import tkinter as tk
from controllers.mesa_controller import get_all_mesas
from controllers.pedido_controller import create_pedido
from views.producto_seleccion import ProductoSeleccionView
import os

class PedidoView(tk.Toplevel):
    def __init__(self, parent, trabajador):
        super().__init__(parent)
        self.title("Nuevo Pedido - Beef Point")
        self.geometry("400x300")
        self.configure(bg="#F0F0F0")  # Fondo suave

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        # Estilo para etiquetas y entradas
        label_style = {"font": ("Arial", 12), "bg": "#F0F0F0"}
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

        # Label para seleccionar mesa
        self.label_mesa = tk.Label(self, text="Seleccione la Mesa:", **label_style)
        self.label_mesa.pack(pady=10)

        self.mesas = get_all_mesas()  # Cargar todas las mesas disponibles
        self.mesa_var = tk.StringVar(self)
        self.mesa_var.set("Seleccionar Mesa")

        self.mesa_dropdown = tk.OptionMenu(self, self.mesa_var, *[mesa.numero for mesa in self.mesas])
        self.mesa_dropdown.configure(font=("Arial", 12))
        self.mesa_dropdown.pack(pady=10)

        self.button_crear_pedido = tk.Button(self, text="Crear Pedido", command=self.crear_pedido, **button_style)
        self.button_crear_pedido.pack(pady=20)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def crear_pedido(self):
        mesa_numero = self.mesa_var.get()
        mesa = next((m for m in self.mesas if str(m.numero) == mesa_numero), None)

        if mesa:
            pedido_id = create_pedido(mesa.id, self.trabajador.id, "Pendiente")
            self.destroy()
            ProductoSeleccionView(self.master, pedido_id)
        else:
            tk.messagebox.showerror("Error", "Debe seleccionar una mesa válida.")
