import tkinter as tk
from tkinter import ttk
from controllers.pedido_controller import get_detalle_by_pedido, update_producto_cantidad, add_producto_to_pedido, delete_producto_from_pedido, get_all_categorias, get_productos_by_categoria
import os

class EditarPedidoView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Editar Pedido - Beef Point")
        self.geometry("480x530")
        self.configure(bg="#F0F0F0")

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id
        self.parent = parent  # Para actualizar el historial al cerrar la ventana
        self.productos_actualizados = {}  # Diccionario para almacenar los productos y cantidades actualizadas
        self.nuevos_productos = []  # Lista para almacenar los nuevos productos a agregar
        self.productos_eliminar = []  # Lista para almacenar los productos a eliminar

        self.mostrar_detalles()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_detalles(self):
        detalles = get_detalle_by_pedido(self.pedido_id)
        
        categoria_label = tk.Label(self, text="Productos del Pedido Actual:", font=("Arial", 14), bg="#F0F0F0")
        categoria_label.pack(pady=10)

        for detalle in detalles:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            frame = tk.Frame(self, bg="#F0F0F0")
            frame.pack(pady=8, fill=tk.X)
            
            label = tk.Label(frame, text=producto_nombre, font=("Arial", 12), bg="#F0F0F0")
            label.pack(side=tk.LEFT, padx=10)
            
            cantidad_var = tk.IntVar(value=cantidad)
            cantidad_entry = tk.Entry(frame, textvariable=cantidad_var, font=("Arial", 12), width=4)
            cantidad_entry.pack(side=tk.LEFT, padx=5)
            
            self.productos_actualizados[producto_id] = (cantidad_var, frame)

            delete_button = tk.Button(frame, text="Eliminar", command=lambda pid=producto_id: self.eliminar_producto(pid), font=("Arial", 10), bg="#FF0000", fg="white")
            delete_button.pack(side=tk.LEFT, padx=10)

        # Mostrar productos adicionales por categoría
        categorias = get_all_categorias()
        categoria_label = tk.Label(self, text="Agregar mas Productos por Categoría:", font=("Arial", 14), bg="#F0F0F0")
        categoria_label.pack(pady=10)
        
        self.categoria_var = tk.StringVar(self)
        self.categoria_var.set("Seleccionar Categoría")
        self.categoria_dropdown = ttk.Combobox(self, textvariable=self.categoria_var, values=[cat.nombre for cat in categorias], font=("Arial", 12))
        self.categoria_dropdown.pack(pady=10)
        self.categoria_dropdown.bind("<<ComboboxSelected>>", self.mostrar_productos_categoria)

        self.producto_frame = tk.Frame(self, bg="#F0F0F0")
        self.producto_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Botón para guardar todos los cambios
        save_button = tk.Button(self, text="Guardar Cambios", command=self.guardar_cambios, font=("Arial", 12), bg="#4CAF50", fg="white")
        save_button.pack(pady=20)

    def mostrar_productos_categoria(self, event):
        categoria_nombre = self.categoria_var.get()
        categoria = next((c for c in get_all_categorias() if c.nombre == categoria_nombre), None)

        if categoria:
            productos = get_productos_by_categoria(categoria.id)
            for widget in self.producto_frame.winfo_children():
                widget.destroy()

            for producto in productos:
                self.crear_producto_widget(producto)

    def crear_producto_widget(self, producto):
        frame = tk.Frame(self.producto_frame, bg="#F0F0F0")
        frame.pack(pady=8, fill=tk.X)

        label = tk.Label(frame, text=producto.nombre, font=("Arial", 12), bg="#F0F0F0")
        label.pack(side=tk.LEFT, padx=10)

        cantidad_var = tk.IntVar(value=0)
        cantidad_entry = tk.Entry(frame, textvariable=cantidad_var, font=("Arial", 12), width=4)
        cantidad_entry.pack(side=tk.LEFT, padx=5)

        self.nuevos_productos.append((producto.id, cantidad_var))

    def eliminar_producto(self, producto_id):
        if producto_id in self.productos_actualizados:
            _, frame = self.productos_actualizados.pop(producto_id)
            self.productos_eliminar.append(producto_id)
            frame.destroy()

    def guardar_cambios(self):
        # Eliminar productos seleccionados
        for producto_id in self.productos_eliminar:
            delete_producto_from_pedido(self.pedido_id, producto_id)

        # Actualizar cantidades de productos existentes
        for producto_id, (cantidad_var, _) in self.productos_actualizados.items():
            nueva_cantidad = cantidad_var.get()
            if nueva_cantidad > 0:
                update_producto_cantidad(self.pedido_id, producto_id, nueva_cantidad)

        # Agregar nuevos productos al pedido
        for producto_id, cantidad_var in self.nuevos_productos:
            nueva_cantidad = cantidad_var.get()
            if nueva_cantidad > 0:
                add_producto_to_pedido(self.pedido_id, producto_id, nueva_cantidad)

        tk.messagebox.showinfo("Éxito", "Todos los cambios han sido guardados.")
        self.parent.mostrar_historial()  # Actualiza el historial de pedidos
        self.destroy()
