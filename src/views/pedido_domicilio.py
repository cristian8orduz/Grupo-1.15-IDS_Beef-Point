import tkinter as tk
from tkinter import ttk
from controllers.pedido_controller import create_pedido
from views.producto_seleccion import ProductoSeleccionView
import os

class PedidoDomicilioView(tk.Toplevel):
    def __init__(self, parent, trabajador):
        super().__init__(parent)
        self.title("Nuevo Pedido a Domicilio - Beef Point")
        self.geometry("500x400")
        self.configure(bg="#2C3E50")  # Fondo oscuro para un look profesional

        # Centrar la ventana
        self.center_window()
        
        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        # Estilo para etiquetas y entradas
        label_style = {"font": ("Helvetica", 12, "bold"), "bg": "#2C3E50", "fg": "white"}
        entry_style = {"font": ("Helvetica", 12), "bg": "#ECF0F1", "fg": "#34495E", "bd": 2, "relief": "groove"}

        # Estilo del botón
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#218ff9",
            "fg": "white",
            "activebackground": "#1c68b1",
            "bd": 0,
            "relief": "flat",
            "width": 20,
            "height": 2,
            "cursor": "hand2"
        }

        # Título de la sección
        title_label = tk.Label(self, text="Información del Cliente", font=("Helvetica", 16, "bold"), bg="#2C3E50", fg="white")
        title_label.pack(pady=20)

        # Nombre del Cliente
        self.label_nombre_cliente = tk.Label(self, text="Nombre del Cliente:", **label_style)
        self.label_nombre_cliente.pack(pady=5)
        self.entry_nombre_cliente = tk.Entry(self, **entry_style)
        self.entry_nombre_cliente.pack(pady=5, fill=tk.X, padx=20)

        # Dirección
        self.label_direccion = tk.Label(self, text="Dirección:", **label_style)
        self.label_direccion.pack(pady=5)
        self.entry_direccion = tk.Entry(self, **entry_style)
        self.entry_direccion.pack(pady=5, fill=tk.X, padx=20)

        # Número de Contacto
        self.label_contacto = tk.Label(self, text="Número de Contacto:", **label_style)
        self.label_contacto.pack(pady=5)
        self.entry_contacto = tk.Entry(self, **entry_style)
        self.entry_contacto.pack(pady=5, fill=tk.X, padx=20)

        # Botón para Crear Pedido
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
        nombre_cliente = self.entry_nombre_cliente.get()
        direccion = self.entry_direccion.get()
        numero_contacto = self.entry_contacto.get()

        if nombre_cliente and direccion and numero_contacto:
            pedido_id = create_pedido(None, self.trabajador.id, "Pendiente", direccion=direccion, numero_contacto=numero_contacto, nombre_cliente=nombre_cliente)
            self.destroy()
            ProductoSeleccionView(self.master, pedido_id)
        else:
            tk.messagebox.showerror("Error", "Debe ingresar todos los datos del domicilio.")

