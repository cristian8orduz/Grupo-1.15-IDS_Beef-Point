import tkinter as tk
from controllers.pedido_controller import get_detalle_by_pedido, confirmar_pedido, cancelar_pedido, get_pedido, update_pedido_info
from controllers.producto_controller import get_precio_producto
import os

class ResumenPedidoView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Resumen del Pedido - Beef Point")
        self.geometry("550x500")
        self.configure(bg="#2C3E50")  # Fondo oscuro para un diseño más profesional

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.pedido_id = pedido_id

        # Cargar información del pedido
        self.pedido = get_pedido(self.pedido_id)

        label_style = {"font": ("Helvetica", 14, "bold"), "bg": "#2C3E50", "fg": "white"}
        entry_style = {"font": ("Helvetica", 12), "bd": 2, "relief": "solid"}
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#218ff9",
            "fg": "white",
            "activebackground": "#1d71c2",
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "width": 47,
            "height": 2
        }

        title_style = {"font": ("Helvetica", 16, "bold"), "bg": "#2C3E50", "fg": "#218ff9"}

        self.label_resumen = tk.Label(self, text="Resumen del Pedido", **label_style)
        self.label_resumen.pack(pady=20)

        # Crear un Canvas para permitir el scroll
        self.canvas = tk.Canvas(self, bg="#2C3E50")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2C3E50")

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

        # Habilitar el scroll con la rueda del ratón en cualquier parte del canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.resumen_frame = tk.Frame(self.scrollable_frame, bg="#34495E", bd=2, relief="solid")
        self.resumen_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Mostrar campos de cliente solo si el pedido es a domicilio
        if self.pedido.direccion or self.pedido.numero_contacto or self.pedido.nombre_cliente:
            
            self.label_datos_cliente = tk.Label(self.scrollable_frame, text="Datos del Cliente", **title_style)
            self.label_datos_cliente.pack(pady=15)

            self.label_nombre_cliente = tk.Label(self.scrollable_frame, text="Nombre del Cliente:", **label_style)
            self.label_nombre_cliente.pack(pady=5)
            self.entry_nombre_cliente = tk.Entry(self.scrollable_frame, **entry_style)
            self.entry_nombre_cliente.pack(pady=5, fill=tk.X, padx=20)
            if self.pedido.nombre_cliente:
                self.entry_nombre_cliente.insert(0, self.pedido.nombre_cliente)


            self.label_direccion = tk.Label(self.scrollable_frame, text="Dirección:", **label_style)
            self.label_direccion.pack(pady=5)
            self.entry_direccion = tk.Entry(self.scrollable_frame, **entry_style)
            self.entry_direccion.pack(pady=5, fill=tk.X, padx=20)
            if self.pedido.direccion:
                self.entry_direccion.insert(0, self.pedido.direccion)

            self.label_contacto = tk.Label(self.scrollable_frame, text="Número de Contacto:", **label_style)
            self.label_contacto.pack(pady=5)
            self.entry_contacto = tk.Entry(self.scrollable_frame, **entry_style)
            self.entry_contacto.pack(pady=5, fill=tk.X, padx=20)
            if self.pedido.numero_contacto:
                self.entry_contacto.insert(0, self.pedido.numero_contacto)
        else:
            self.entry_nombre_cliente = None
            self.entry_direccion = None
            self.entry_contacto = None

        self.mostrar_resumen()

        self.button_confirmar = tk.Button(self.scrollable_frame, text="Confirmar Pedido", command=self.confirmar_pedido, **button_style)
        self.button_confirmar.pack(pady=20)

        self.button_cancelar = tk.Button(self.scrollable_frame, text="Cancelar Pedido", command=self.cancelar_pedido, **button_style)
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
        total = 0  # Variable para calcular el total

        for widget in self.resumen_frame.winfo_children():
            widget.destroy()

        for detalle in detalles:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            precio = get_precio_producto(producto_id)  # Obtener el precio del producto
            subtotal = cantidad * precio  # Calcular el subtotal
            total += subtotal  # Sumar el subtotal al total

            label = tk.Label(self.resumen_frame, text=f"{categoria_nombre} - {producto_nombre} x {cantidad} (${subtotal:,.0f})", font=("Helvetica", 12), bg="#34495E", fg="white")
            label.pack(anchor="w", padx=10, pady=5)

        # Mostrar el total
        total_label = tk.Label(self.resumen_frame, text=f"Total: ${total:,.0f}", font=("Helvetica", 14, "bold"), bg="#34495E", fg="white")
        total_label.pack(anchor="w", padx=10, pady=10)

    def confirmar_pedido(self):
        # Validar que los campos del cliente no estén vacíos si es un pedido a domicilio
        if self.entry_nombre_cliente and self.entry_direccion and self.entry_contacto:
            nombre_cliente = self.entry_nombre_cliente.get().strip()
            direccion = self.entry_direccion.get().strip()
            numero_contacto = self.entry_contacto.get().strip()

            if not nombre_cliente or not direccion or not numero_contacto:
                tk.messagebox.showerror("Error", "Los campos de Nombre del Cliente, Dirección y Número de Contacto no pueden estar vacíos.")
                return
            
            # Actualizar la información del cliente si todo es válido
            update_pedido_info(self.pedido_id, nombre_cliente, direccion, numero_contacto)

        # Confirmar el pedido
        confirmar_pedido(self.pedido_id)
        tk.messagebox.showinfo("Éxito", "Pedido confirmado.")
        self.destroy()

    def cancelar_pedido(self):
        cancelar_pedido(self.pedido_id)
        tk.messagebox.showinfo("Información", "Pedido cancelado.")
        self.destroy()

    def _on_mousewheel(self, event):
        """Desplazamiento con la rueda del ratón solo si el canvas es válido"""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
