import tkinter as tk
from tkinter import messagebox
from controllers.pedido_controller import validar_comprobante_y_enviar_captura, confirmar_comprobante_cliente, get_pedido, get_detalle_by_pedido
from controllers.producto_controller import get_precio_producto
from PIL import Image, ImageDraw, ImageFont
import os

class ComprobanteView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Gestión de Comprobante - Beef Point")
        self.geometry("600x400")
        self.configure(bg="#2C3E50")

        self.pedido_id = pedido_id
        self.pedido = get_pedido(self.pedido_id)
        self.tiempo_var = tk.StringVar(value="15")  # Tiempo predeterminado en minutos

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        # Crear un canvas con scrollbar
        self.canvas = tk.Canvas(self, bg="#2C3E50")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar el canvas y scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Crear un frame dentro del canvas para colocar los widgets
        self.frame = tk.Frame(self.canvas, bg="#2C3E50")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Vincular la rueda del ratón para desplazamiento
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Actualizar el tamaño del canvas cuando cambia el contenido
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Evento para limpiar el binding de la rueda del ratón al cerrar la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Mostrar título
        title_label = tk.Label(self.frame, text="Gestión de Comprobante", font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="white")
        title_label.pack(pady=15)

        # Mostrar detalles del pedido
        self.mostrar_detalles_pedido()

        # Tiempo estimado de llegada
        tiempo_label = tk.Label(self.frame, text="Tiempo estimado de llegada (minutos):", font=("Helvetica", 12), bg="#2C3E50", fg="white")
        tiempo_label.pack(pady=5)
        self.tiempo_entry = tk.Entry(self.frame, textvariable=self.tiempo_var, font=("Helvetica", 12), width=10)
        self.tiempo_entry.pack(pady=5)

        # Botón para validar y generar la captura
        enviar_button = tk.Button(self.frame, text="Validar y Enviar Captura", command=self.enviar_captura, bg="#27AE60", fg="white", font=("Helvetica", 12, "bold"), width=25)
        enviar_button.pack(pady=10)

        # Botón para confirmar el comprobante si el cliente está de acuerdo
        confirmar_button = tk.Button(self.frame, text="Confirmar Comprobante", command=self.confirmar_comprobante, bg="#218ff9", fg="white", font=("Helvetica", 12, "bold"), width=25)
        confirmar_button.pack(pady=10)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_detalles_pedido(self):
        detalles = ""
        total = 0

        if self.pedido.mesa_id is None:
            detalles += f"Cliente: {self.pedido.nombre_cliente}\n"
            detalles += f"Dirección: {self.pedido.direccion}\n"
            detalles += f"Teléfono: {self.pedido.numero_contacto}\n"
        else:
            detalles += f"Mesa: {self.pedido.mesa_id}\n"

        detalles += "\nDetalles del Pedido:\n"
        detalles_pedido = get_detalle_by_pedido(self.pedido_id)

        # Mostrar cada detalle con letra más pequeña
        for detalle in detalles_pedido:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            precio = get_precio_producto(producto_id)
            total_producto = cantidad * precio
            total += total_producto
            detalles += f"- {categoria_nombre} - {producto_nombre} x {cantidad} (${total_producto:,.0f})\n"

        detalles_label = tk.Label(self.frame, text=detalles, font=("Helvetica", 12), bg="#2C3E50", fg="white", justify=tk.LEFT)
        detalles_label.pack(pady=10)

        # Mostrar el total con letra más grande y en negrita
        total_label = tk.Label(self.frame, text=f"\nTotal: ${total:,.0f}", font=("Helvetica", 14, "bold"), bg="#2C3E50", fg="white")
        total_label.pack(pady=5)

    def enviar_captura(self):
        """Generar y guardar el comprobante como una imagen JPG."""
        tiempo_estimado = self.tiempo_var.get()

        # Crear la imagen del comprobante
        imagen = Image.new('RGB', (600, 400), color=(73, 109, 137))
        d = ImageDraw.Draw(imagen)
        font = ImageFont.load_default()

        # Añadir texto del comprobante a la imagen
        texto_comprobante = f"Comprobante de Pedido ID: {self.pedido_id}\n"
        if self.pedido.mesa_id is None:
            texto_comprobante += f"Cliente: {self.pedido.nombre_cliente}\nDirección: {self.pedido.direccion}\nTeléfono: {self.pedido.numero_contacto}\n"
        texto_comprobante += f"Tiempo estimado de llegada: {tiempo_estimado} minutos\n"
        texto_comprobante += "Detalles del Pedido:\n"

        detalles_pedido = get_detalle_by_pedido(self.pedido_id)
        total = 0
        for detalle in detalles_pedido:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            precio = get_precio_producto(producto_id)
            total_producto = cantidad * precio
            total += total_producto
            texto_comprobante += f"- {categoria_nombre} - {producto_nombre} x {cantidad} (${total_producto:,.0f})\n"

        texto_comprobante += f"\nTotal: ${total:,.0f}"

        d.text((10, 10), texto_comprobante, fill=(255, 255, 255), font=font)

        # Guardar la imagen en la carpeta 'src/comprobantes'
        folder_path = os.path.join(os.getcwd(), 'src', 'comprobantes')
        os.makedirs(folder_path, exist_ok=True)  # Crear carpeta si no existe
        file_path = os.path.join(folder_path, f'comprobante_{self.pedido_id}.jpg')
        imagen.save(file_path)

        messagebox.showinfo("Éxito", f"Comprobante generado y guardado en: {file_path}")

    def confirmar_comprobante(self):
        cliente_acuerdo = messagebox.askyesno("Confirmación", "¿El cliente está de acuerdo con el comprobante?")
        confirmar_comprobante_cliente(self.pedido_id, cliente_acuerdo)
        if cliente_acuerdo:
            messagebox.showinfo("Éxito", "Comprobante confirmado.")
        else:
            messagebox.showwarning("Información", "El cliente no está de acuerdo con el comprobante.")

    def _on_mousewheel(self, event):
        """Permitir el desplazamiento con la rueda del ratón."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_close(self):
        """Desvincular el evento de la rueda del ratón cuando la ventana se cierra."""
        self.canvas.unbind_all("<MouseWheel>")
        self.destroy()
