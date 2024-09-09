import tkinter as tk
from tkinter import ttk
from controllers.categoria_controller import get_all_categorias
from controllers.producto_controller import get_productos_by_categoria
from controllers.pedido_controller import update_producto_cantidad, get_detalle_by_pedido
from views.resumen_pedido import ResumenPedidoView
import os

class ProductoSeleccionView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Seleccionar Productos - Beef Point")
        self.geometry("600x500")
        self.configure(bg="#34495E")  # Fondo oscuro profesional

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id
        self.categorias = get_all_categorias()
        self.productos_seleccionados = {}  # Almacenar productos seleccionados con sus cantidades

        # Estilo para etiquetas y botones
        label_style = {"font": ("Helvetica", 14, "bold"), "bg": "#34495E", "fg": "white"}
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#218ff9",
            "fg": "white",
            "activebackground": "#1d71c2",
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2"
        }

        self.label_categoria = tk.Label(self, text="Seleccione la Categoría:", **label_style)
        self.label_categoria.pack(pady=15)

        self.categoria_var = tk.StringVar(self)
        self.categoria_var.set("Seleccionar Categoría")

        self.categoria_dropdown = ttk.Combobox(self, textvariable=self.categoria_var, values=[cat.nombre for cat in self.categorias], font=("Helvetica", 12))
        self.categoria_dropdown.pack(pady=15)
        
        # Asociar el cambio en la selección de categoría al método para mostrar productos
        self.categoria_dropdown.bind("<<ComboboxSelected>>", lambda event: self.mostrar_productos())

        # Frame para productos con scrollbar
        self.producto_frame = tk.Frame(self, bg="#34495E")
        self.producto_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.producto_frame, bg="#34495E")
        self.scrollbar = tk.Scrollbar(self.producto_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#34495E")

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
        self.button_terminar.pack(pady=25)

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
        frame = tk.Frame(self.scrollable_frame, bg="#34495E")
        frame.pack(pady=10, fill=tk.X)

        label = tk.Label(frame, text=producto.nombre, font=("Helvetica", 12), bg="#34495E", fg="white")
        label.pack(side=tk.LEFT, padx=15)

        cantidad_var = tk.IntVar()
        cantidad_var.set(self.productos_seleccionados.get(producto.id, 0))  # Inicializar con la cantidad actual o 0

        minus_button = tk.Button(frame, text="-", command=lambda: self.actualizar_cantidad(producto.id, cantidad_var, -1), font=("Helvetica", 12), width=2)
        minus_button.pack(side=tk.LEFT)

        cantidad_label = tk.Label(frame, textvariable=cantidad_var, font=("Helvetica", 12), width=4, anchor='center', bg="#34495E", fg="white")
        cantidad_label.pack(side=tk.LEFT, padx=10)

        plus_button = tk.Button(frame, text="+", command=lambda: self.actualizar_cantidad(producto.id, cantidad_var, 1), font=("Helvetica", 12), width=2)
        plus_button.pack(side=tk.LEFT)

    def actualizar_cantidad(self, producto_id, var, delta):
        nueva_cantidad = max(0, var.get() + delta)
        var.set(nueva_cantidad)

        # Actualizar o eliminar la cantidad en el pedido
        if nueva_cantidad > 0:
            self.productos_seleccionados[producto_id] = nueva_cantidad
        elif producto_id in self.productos_seleccionados:
            del self.productos_seleccionados[producto_id]

    def terminar_pedido(self):
        # Verificar si al menos un producto tiene una cantidad mayor a 0
        if any(cantidad > 0 for cantidad in self.productos_seleccionados.values()):
            # Guardar todas las cantidades actualizadas en el pedido
            for producto_id, cantidad in self.productos_seleccionados.items():
                update_producto_cantidad(self.pedido_id, producto_id, cantidad)
            
            # Mostrar resumen del pedido para confirmarlo
            resumen_view = ResumenPedidoView(self.master, self.pedido_id)
            resumen_view.lift()  # Traer la ventana al frente
            resumen_view.focus_force()  # Forzar el foco a la ventana de resumen
            self.destroy()
        else:
            # Mostrar mensaje de advertencia si no hay productos seleccionados
            tk.messagebox.showinfo("Información", "Debe seleccionar al menos un producto y asignar una cantidad mayor a 0.")

