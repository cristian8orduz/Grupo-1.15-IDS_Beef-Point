import tkinter as tk
from tkinter import ttk, Scrollbar, messagebox
from controllers.producto_controller import get_all_categorias, get_productos_by_categoria, update_precio_producto, create_producto, delete_producto
import os

class AdminProductosView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Administrar Productos por Categoría - Beef Point")
        self.geometry("700x450")
        self.configure(bg="#34495E")

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.categorias = get_all_categorias()

        # Instrucciones para el usuario
        instrucciones = (
            "1. Selecciona una categoría para ver los productos.\n"
            "2. Edita el precio y presiona 'Guardar'.\n"
            "3. Presiona 'Eliminar' para borrar un producto.\n"
            "4. Para agregar, selecciona una categoría, ingresa el nombre y presiona 'Agregar Producto'."
        )

        self.label_instrucciones = tk.Label(self, text=instrucciones, font=("Helvetica", 10), bg="#34495E", fg="white", justify="left")
        self.label_instrucciones.pack(pady=10, padx=10)

        label_style = {"font": ("Helvetica", 14, "bold"), "bg": "#34495E", "fg": "white"}

        # Categoría Dropdown
        self.label_categoria = tk.Label(self, text="Seleccione Categoría", **label_style)
        self.label_categoria.pack(pady=10)

        self.categoria_var = tk.StringVar(self)
        self.categoria_dropdown = ttk.Combobox(self, textvariable=self.categoria_var, values=[cat.nombre for cat in self.categorias], font=("Helvetica", 12))
        self.categoria_dropdown.pack(pady=10)
        self.categoria_dropdown.bind("<<ComboboxSelected>>", self.mostrar_productos)

        # Añadir encabezados para los productos
        self.header_frame = tk.Frame(self, bg="#34495E")
        self.header_frame.pack(fill=tk.X, padx=20)

        self.label_nombre = tk.Label(self.header_frame, text="Nombre", font=("Helvetica", 12, "bold"), bg="#34495E", fg="white")
        self.label_nombre.pack(side=tk.LEFT, padx=50)

        self.label_precio = tk.Label(self.header_frame, text="Precio", font=("Helvetica", 12, "bold"), bg="#34495E", fg="white")
        self.label_precio.pack(side=tk.LEFT, padx=100)

        # Configuración del Canvas y Scrollbar
        self.canvas = tk.Canvas(self, bg="#34495E")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Crear un frame dentro del canvas
        self.frame_productos = tk.Frame(self.canvas, bg="#34495E")
        self.canvas.create_window((0, 0), window=self.frame_productos, anchor="nw")

        # Vincular el evento de la rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.frame_productos.bind("<Configure>", self.on_frame_configure)

        # Entrada para agregar un nuevo producto
        self.label_nuevo_producto = tk.Label(self, text="Agregar Nuevo Producto", **label_style)
        self.label_nuevo_producto.pack(pady=10)

        self.nuevo_producto_entry = tk.Entry(self, font=("Helvetica", 12), width=20)
        self.nuevo_producto_entry.pack(pady=10)

        self.add_button = tk.Button(self, text="Agregar Producto", command=self.agregar_producto, bg="#27AE60", fg="white", font=("Helvetica", 12))
        self.add_button.pack(pady=10)

        # Registro de validación para permitir solo números enteros
        self.validar_numero = self.register(self.solo_numeros_enteros)

    def solo_numeros_enteros(self, text):
        """Permitir solo números enteros."""
        return text.isdigit() or text == ""

    def on_frame_configure(self, event):
        """Actualizar la región de scroll para el canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Permitir desplazamiento con la rueda del mouse solo si el canvas existe."""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def mostrar_productos(self, event):
        # Limpiar el frame de productos
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        categoria_nombre = self.categoria_var.get()
        categoria = next((c for c in self.categorias if c.nombre == categoria_nombre), None)
        if categoria:
            productos = get_productos_by_categoria(categoria.id)
            for producto in productos:
                self.crear_producto_widget(producto)

    def crear_producto_widget(self, producto):
        label_style = {"font": ("Helvetica", 12), "bg": "#34495E", "fg": "white"}

        frame = tk.Frame(self.frame_productos, bg="#34495E")
        frame.pack(pady=5, fill=tk.X)

        label = tk.Label(frame, text=producto.nombre, **label_style)
        label.pack(side=tk.LEFT, padx=10)

        precio_var = tk.StringVar(value=str(int(producto.precio)))
        entry_precio = tk.Entry(frame, textvariable=precio_var, font=("Helvetica", 12), width=8, 
                                validate="key", validatecommand=(self.validar_numero, "%P"))
        entry_precio.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(frame, text="Guardar", command=lambda p=producto.id, v=precio_var: self.guardar_precio(p, v), bg="#218ff9", fg="white", font=("Helvetica", 10))
        save_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(frame, text="Eliminar", command=lambda p=producto.id: self.eliminar_producto(p), bg="#E74C3C", fg="white", font=("Helvetica", 10))
        delete_button.pack(side=tk.LEFT, padx=5)

    def guardar_precio(self, producto_id, precio_var):
        nuevo_precio = int(precio_var.get())  # Convertir a número entero
        update_precio_producto(producto_id, nuevo_precio)
        tk.messagebox.showinfo("Éxito", "Precio actualizado con éxito.")

    def eliminar_producto(self, producto_id):
        respuesta = tk.messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este producto?")
        if respuesta:
            delete_producto(producto_id)
            tk.messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.mostrar_productos(None)  # Refrescar la lista de productos

    def agregar_producto(self):
        """Agregar un nuevo producto a la categoría seleccionada."""
        nombre_nuevo_producto = self.nuevo_producto_entry.get()
        categoria_nombre = self.categoria_var.get()

        if not nombre_nuevo_producto:
            tk.messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
            return

        if not categoria_nombre:
            tk.messagebox.showerror("Error", "Por favor selecciona una categoría.")
            return

        categoria = next((c for c in self.categorias if c.nombre == categoria_nombre), None)
        if categoria:
            create_producto(nombre_nuevo_producto, categoria.id)
            tk.messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            self.mostrar_productos(None)  # Refrescar la lista de productos
            self.nuevo_producto_entry.delete(0, tk.END)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
