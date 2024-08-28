import tkinter as tk
from tkinter import ttk
from controllers.categoria_controller import get_all_categorias
from controllers.producto_controller import get_productos_by_categoria
from controllers.pedido_controller import add_producto_to_pedido
from views.resumen_pedido import ResumenPedidoView
import os

class ProductoSeleccionView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Seleccionar Productos - Beef Point")
        self.geometry("550x650")
        self.configure(bg="#EAECEE")  # Fondo suave más claro

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id
        self.categorias = get_all_categorias()

        # Estilo para etiquetas y botones
        label_style = {"font": ("Verdana", 13, "bold"), "bg": "#EAECEE"}
        button_style = {
            "font": ("Verdana", 12, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#16A085",
            "bd": 0,
            "relief": "flat"
        }

        self.label_categoria = tk.Label(self, text="Seleccione la Categoría:", **label_style)
        self.label_categoria.pack(pady=10)

        self.categoria_var = tk.StringVar(self)
        self.categoria_var.set("Seleccionar Categoría")

        self.categoria_dropdown = ttk.Combobox(self, textvariable=self.categoria_var, values=[cat.nombre for cat in self.categorias], font=("Verdana", 12))
        self.categoria_dropdown.pack(pady=10)
        
        # Asociar el cambio en la selección de categoría al método para mostrar productos
        self.categoria_dropdown.bind("<<ComboboxSelected>>", lambda event: self.mostrar_productos())

        # Frame para productos con scrollbar
        self.producto_frame = tk.Frame(self, bg="#EAECEE")
        self.producto_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.producto_frame, bg="#EAECEE")
        self.scrollbar = tk.Scrollbar(self.producto_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#EAECEE")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.button_terminar = tk.Button(self, text="Terminar Pedido", command=self.terminar_pedido, **button_style)
        self.button_terminar.pack(pady=20)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_productos(self):
        categoria_nombre = self.categoria_var.get()
        categoria = next((c for c in self.categorias if c.nombre == categoria_nombre), None)

        if categoria:
            productos = get_productos_by_categoria(categoria.id)
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            for producto in productos:
                self.crear_producto_widget(producto)

    def crear_producto_widget(self, producto):
        frame = tk.Frame(self.scrollable_frame, bg="#EAECEE")
        frame.pack(pady=8, fill=tk.X)

        label = tk.Label(frame, text=producto.nombre, font=("Verdana", 12), bg="#EAECEE")
        label.pack(side=tk.LEFT, padx=10)

        cantidad_var = tk.IntVar()
        cantidad_var.set(0)

        minus_button = tk.Button(frame, text="-", command=lambda: self.actualizar_cantidad(cantidad_var, -1), font=("Verdana", 12), width=2)
        minus_button.pack(side=tk.LEFT)

        cantidad_label = tk.Label(frame, textvariable=cantidad_var, font=("Verdana", 12), width=4, anchor='center')
        cantidad_label.pack(side=tk.LEFT, padx=5)

        plus_button = tk.Button(frame, text="+", command=lambda: self.actualizar_cantidad(cantidad_var, 1), font=("Verdana", 12), width=2)
        plus_button.pack(side=tk.LEFT)

        add_button = tk.Button(frame, text="Añadir", command=lambda: self.add_producto(producto.id, cantidad_var.get()), font=("Verdana", 12))
        add_button.pack(side=tk.LEFT, padx=10)

    def actualizar_cantidad(self, var, delta):
        var.set(max(0, var.get() + delta))

    def add_producto(self, producto_id, cantidad):
        if cantidad > 0:
            add_producto_to_pedido(self.pedido_id, producto_id, cantidad)
            tk.messagebox.showinfo("Éxito", "Producto añadido al pedido.")
        else:
            tk.messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")

    def terminar_pedido(self):
        # Mostrar resumen del pedido para confirmarlo
        resumen_view = ResumenPedidoView(self.master, self.pedido_id)
        resumen_view.lift()  # Traer la ventana al frente
        resumen_view.focus_force()  # Forzar el foco a la ventana de resumen
        self.destroy()


