# src/views/producto_seleccion.py
import tkinter as tk
from controllers.categoria_controller import get_all_categorias
from controllers.producto_controller import get_productos_by_categoria
from controllers.pedido_controller import add_producto_to_pedido
from views.resumen_pedido import ResumenPedidoView
import os

class ProductoSeleccionView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Seleccionar Productos")
        self.geometry("400x500")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id

        self.categorias = get_all_categorias()

        self.label_categoria = tk.Label(self, text="Seleccione la Categoría:")
        self.label_categoria.pack(pady=5)

        self.categoria_var = tk.StringVar(self)
        self.categoria_var.set("Seleccionar Categoría")

        self.categoria_dropdown = tk.OptionMenu(self, self.categoria_var, *[cat.nombre for cat in self.categorias])
        self.categoria_dropdown.pack(pady=10)

        self.button_mostrar_productos = tk.Button(self, text="Mostrar Productos", command=self.mostrar_productos)
        self.button_mostrar_productos.pack(pady=10)

        self.producto_frame = tk.Frame(self)
        self.producto_frame.pack(pady=20)

        self.button_terminar = tk.Button(self, text="Terminar Pedido", command=self.terminar_pedido)
        self.button_terminar.pack(pady=10)

    def mostrar_productos(self):
        categoria_nombre = self.categoria_var.get()
        categoria = next((c for c in self.categorias if c.nombre == categoria_nombre), None)

        if categoria:
            productos = get_productos_by_categoria(categoria.id)
            for widget in self.producto_frame.winfo_children():
                widget.destroy()

            for producto in productos:
                self.crear_producto_widget(producto)

    def crear_producto_widget(self, producto):
        frame = tk.Frame(self.producto_frame)
        frame.pack(pady=5)

        label = tk.Label(frame, text=producto.nombre)
        label.pack(side=tk.LEFT, padx=10)

        cantidad_var = tk.IntVar()
        cantidad_var.set(0)

        minus_button = tk.Button(frame, text="-", command=lambda: self.actualizar_cantidad(cantidad_var, -1))
        minus_button.pack(side=tk.LEFT)

        cantidad_label = tk.Label(frame, textvariable=cantidad_var)
        cantidad_label.pack(side=tk.LEFT, padx=5)

        plus_button = tk.Button(frame, text="+", command=lambda: self.actualizar_cantidad(cantidad_var, 1))
        plus_button.pack(side=tk.LEFT)

        add_button = tk.Button(frame, text="Añadir", command=lambda: self.add_producto(producto.id, cantidad_var.get()))
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
        ResumenPedidoView(self.master, self.pedido_id)
        self.destroy()
