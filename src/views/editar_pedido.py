import tkinter as tk
from tkinter import ttk
from controllers.pedido_controller import (
    get_detalle_by_pedido,
    update_producto_cantidad,
    add_producto_to_pedido,
    delete_producto_from_pedido,
    get_pedido,
    update_pedido_info,
    get_all_categorias,
    get_productos_by_categoria,
)
import os

class EditarPedidoView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Editar Pedido - Beef Point")
        self.geometry("550x450")
        self.configure(bg="#2C3E50")

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id
        self.parent = parent
        self.productos_actualizados = {}
        self.nuevos_productos = []
        self.productos_eliminar = []

        title_style = {"font": ("Helvetica", 16, "bold"), "bg": "#2C3E50", "fg": "#218ff9"}

        # Canvas y scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0, bg="#2C3E50")
        frame = tk.Frame(self.canvas, bg="#2C3E50")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Vincular la rueda del mouse al canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Detalles del pedido y productos
        self.frame = frame
        self.detalles = get_detalle_by_pedido(self.pedido_id)
        self.pedido = get_pedido(self.pedido_id)

        self.mostrar_detalles()

    def _on_mousewheel(self, event):
        # Verificar si el canvas aún existe antes de intentar desplazarse
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_detalles(self):
        # Si es un pedido a domicilio, mostrar campos para editar la información del cliente
        if self.pedido.direccion or self.pedido.numero_contacto or self.pedido.nombre_cliente:
            label_style = {"font": ("Helvetica", 12, "bold"), "bg": "#2C3E50", "fg": "white"}
            entry_style = {"font": ("Helvetica", 12), "bd": 2, "relief": "solid"}

            categoria_label = tk.Label(self.frame, text="Datos del Cliente:", font=("Helvetica", 14, "bold"), bg="#2C3E50", fg="#218ff9")
            categoria_label.pack(pady=10)

            self.label_nombre_cliente = tk.Label(self.frame, text="Nombre del Cliente:", **label_style)
            self.label_nombre_cliente.pack(pady=5)
            self.entry_nombre_cliente = tk.Entry(self.frame, **entry_style)
            self.entry_nombre_cliente.insert(0, self.pedido.nombre_cliente)
            self.entry_nombre_cliente.pack(pady=5, fill=tk.X, padx=20)

            self.label_direccion = tk.Label(self.frame, text="Dirección:", **label_style)
            self.label_direccion.pack(pady=5)
            self.entry_direccion = tk.Entry(self.frame, **entry_style)
            self.entry_direccion.insert(0, self.pedido.direccion)
            self.entry_direccion.pack(pady=5, fill=tk.X, padx=20)

            self.label_contacto = tk.Label(self.frame, text="Número de Contacto:", **label_style)
            self.label_contacto.pack(pady=5)
            self.entry_contacto = tk.Entry(self.frame, **entry_style)
            self.entry_contacto.insert(0, self.pedido.numero_contacto)
            self.entry_contacto.pack(pady=5, fill=tk.X, padx=20)

        # Mostrar productos del pedido
        categoria_label = tk.Label(self.frame, text="Productos del Pedido Actual:", font=("Helvetica", 14, "bold"), bg="#2C3E50", fg="#218ff9")
        categoria_label.pack(pady=10)

        for detalle in self.detalles:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            frame = tk.Frame(self.frame, bg="#34495E")
            frame.pack(pady=8, fill=tk.X, padx=10)

            label = tk.Label(frame, text=producto_nombre, font=("Helvetica", 12), bg="#34495E", fg="white")
            label.pack(side=tk.LEFT, padx=10)

            cantidad_var = tk.IntVar(value=cantidad)
            cantidad_entry = tk.Entry(frame, textvariable=cantidad_var, font=("Helvetica", 12), width=4, bd=1, relief="solid")
            cantidad_entry.pack(side=tk.LEFT, padx=5)

            self.productos_actualizados[producto_id] = (cantidad_var, frame)

            delete_button = tk.Button(frame, text="Eliminar", command=lambda pid=producto_id: self.eliminar_producto(pid), font=("Helvetica", 10, "bold"), bg="#E74C3C", fg="white", relief="flat", cursor="hand2")
            delete_button.pack(side=tk.LEFT, padx=10)

        # Mostrar productos adicionales por categoría
        categorias = get_all_categorias()
        categoria_label = tk.Label(self.frame, text="Agregar más Productos por Categoría:", font=("Helvetica", 14, "bold"), bg="#2C3E50", fg="#218ff9")
        categoria_label.pack(pady=10)
        
        self.categoria_var = tk.StringVar(self)
        self.categoria_var.set("Seleccionar Categoría")
        self.categoria_dropdown = ttk.Combobox(self.frame, textvariable=self.categoria_var, values=[cat.nombre for cat in categorias], font=("Helvetica", 12))
        self.categoria_dropdown.pack(pady=10)
        self.categoria_dropdown.bind("<<ComboboxSelected>>", self.mostrar_productos_categoria)

        self.producto_frame = tk.Frame(self.frame, bg="#2C3E50")
        self.producto_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=10)

        # Botón para guardar todos los cambios
        save_button = tk.Button(self.frame, text="Guardar Cambios", command=self.guardar_cambios, font=("Helvetica", 12, "bold"), bg="#218ff9", fg="white", relief="flat", cursor="hand2")
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
        frame = tk.Frame(self.producto_frame, bg="#34495E")
        frame.pack(pady=8, fill=tk.X)

        label = tk.Label(frame, text=producto.nombre, font=("Helvetica", 12), bg="#34495E", fg="white")
        label.pack(side=tk.LEFT, padx=10)

        cantidad_var = tk.IntVar(value=0)
        cantidad_entry = tk.Entry(frame, textvariable=cantidad_var, font=("Helvetica", 12), width=4, bd=1, relief="solid")
        cantidad_entry.pack(side=tk.LEFT, padx=5)

        self.nuevos_productos.append((producto.id, cantidad_var))

    def eliminar_producto(self, producto_id):
        if producto_id in self.productos_actualizados:
            _, frame = self.productos_actualizados.pop(producto_id)
            self.productos_eliminar.append(producto_id)
            frame.destroy()

    def guardar_cambios(self):

         # Verificar que al menos haya un producto con cantidad mayor a 0
        productos_validos = any(cantidad_var.get() > 0 for _, (cantidad_var, _) in self.productos_actualizados.items()) or \
                            any(cantidad_var.get() > 0 for _, cantidad_var in self.nuevos_productos)

        if not productos_validos:
            tk.messagebox.showerror("Error", "El pedido debe tener al menos un producto con cantidad mayor a 0.")
            return
    
        # Si es un pedido a domicilio, validar que los campos de información del cliente no estén vacíos
        if hasattr(self, 'entry_nombre_cliente') and hasattr(self, 'entry_direccion') and hasattr(self, 'entry_contacto'):
            nombre_cliente = self.entry_nombre_cliente.get().strip()
            direccion = self.entry_direccion.get().strip()
            numero_contacto = self.entry_contacto.get().strip()

            if not nombre_cliente or not direccion or not numero_contacto:
                tk.messagebox.showerror("Error", "Los campos de Nombre del Cliente, Dirección y Número de Contacto no pueden estar vacíos.")
                return

            update_pedido_info(self.pedido_id, nombre_cliente, direccion, numero_contacto)

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
        self.parent.mostrar_historial()
        self.destroy()
