import tkinter as tk
from tkinter import ttk
from controllers.mesa_controller import get_all_mesas
from controllers.pedido_controller import create_pedido
from views.producto_seleccion import ProductoSeleccionView
import os

class PedidoView(tk.Toplevel):
    def __init__(self, parent, trabajador):
        super().__init__(parent)
        self.title("Nuevo Pedido - Beef Point")
        self.geometry("400x300")
        self.configure(bg="#2C3E50")  # Fondo oscuro y profesional

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        # Estilo para etiquetas y entradas
        label_style = {"font": ("Helvetica", 12, "bold"), "bg": "#2C3E50", "fg": "white"}
        combobox_style = {"font": ("Helvetica", 12)}  # Sin opciones de color que no soporta ttk.Combobox

        # Estilo del botón
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#218ff9",
            "fg": "white",
            "activebackground": "#1c67b0",
            "bd": 0,
            "relief": "flat",
            "width": 20,
            "height": 2,
            "cursor": "hand2"
        }

        # Label para seleccionar mesa
        self.label_mesa = tk.Label(self, text="Seleccione la Mesa:", **label_style)
        self.label_mesa.pack(pady=20)

        self.mesas = get_all_mesas()  # Cargar todas las mesas disponibles
        self.mesa_var = tk.StringVar(self)
        self.mesa_var.set("Seleccionar Mesa")

        # Dropdown personalizado (sin bg y fg, ya que ttk.Combobox no las soporta)
        self.mesa_dropdown = ttk.Combobox(self, textvariable=self.mesa_var, values=[mesa.numero for mesa in self.mesas], **combobox_style)
        self.mesa_dropdown.pack(pady=10)

        # Botón para crear el pedido
        self.button_crear_pedido = tk.Button(self, text="Crear Pedido", command=self.crear_pedido, **button_style)
        self.button_crear_pedido.pack(pady=30)

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
