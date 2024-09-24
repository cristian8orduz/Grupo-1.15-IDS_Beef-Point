import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from controllers.pedido_controller import validar_comprobante_y_enviar_captura, confirmar_comprobante_cliente, get_pedido, get_detalle_by_pedido, comprobar_estado_comprobante
from controllers.producto_controller import get_precio_producto
import os

class ComprobanteView(tk.Toplevel):
    def __init__(self, parent, pedido_id):
        super().__init__(parent)
        self.title("Gestión de Comprobante - Beef Point")
        self.geometry("600x450")
        self.configure(bg="#2C3E50")
        self.parent = parent
        self.pedido_id = pedido_id
        self.pedido = get_pedido(self.pedido_id)
        self.tiempo_var = tk.StringVar(value="15")
        self.tipo_pago_var = tk.StringVar(value="Efectivo")
        self.comprobante_subido = None

        # Cargar los valores de tiempo_llegada y tipo_pago desde la base de datos
        tiempo_llegada = self.pedido.tiempo_llegada if self.pedido.tiempo_llegada else "15"
        tipo_pago = self.pedido.tipo_pago if self.pedido.tipo_pago else "Efectivo"

        self.tiempo_var = tk.StringVar(value=tiempo_llegada)
        self.tipo_pago_var = tk.StringVar(value=tipo_pago)
        self.comprobante_subido = None

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        # Crear canvas y frame
        self.canvas = tk.Canvas(self, bg="#2C3E50", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.frame = tk.Frame(self.canvas, bg="#34495E")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw",  width=600)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Añadir eventos para scroll con la rueda del ratón
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # Título
        title_label = tk.Label(self.frame, text="Gestión de Comprobante", font=("Helvetica", 20, "bold"), bg="#34495E", fg="white")
        title_label.pack(pady=20, fill="x")

        # Sección de detalles del pedido
        self.mostrar_detalles_pedido()

        # Mostrar "Tiempo estimado de llegada" solo si el pedido es a domicilio
        if self.pedido.mesa_id is None:
            tiempo_frame = tk.Frame(self.frame, bg="#34495E")
            tiempo_frame.pack(pady=15)
            tk.Label(tiempo_frame, text="Tiempo estimado de llegada (min):", font=("Helvetica", 14), bg="#34495E", fg="white").pack(side="left")
            self.tiempo_entry = tk.Entry(tiempo_frame, textvariable=self.tiempo_var, font=("Helvetica", 14), width=5)
            self.tiempo_entry.pack(side="left", padx=10)

        # Divisor
        self.crear_divisor()

        # Botón para descargar el comprobante
        enviar_button = tk.Button(self.frame, text="Descargar Comprobante", command=self.enviar_captura, bg="#27AE60", fg="white", font=("Helvetica", 14, "bold"), width=25)
        enviar_button.pack(pady=20)

        # Crear un frame separado para los comprobantes
        self.descargarcomprobante_frame = tk.Frame(self.frame, bg="#34495E")
        self.descargarcomprobante_frame.pack(pady=10, fill="x")

        # Vista del comprobante descargado
        self.mostrar_comprobante_pedido()

        # Divisor
        self.crear_divisor()

        # Sección para subir comprobante del cliente
        subir_frame = tk.Frame(self.frame, bg="#34495E")
        subir_frame.pack(pady=15)
        tk.Label(subir_frame, text="Subir Comprobante del Cliente", font=("Helvetica", 14), bg="#34495E", fg="white").pack()
        tk.Button(subir_frame, text="Subir Comprobante", command=self.subir_comprobante, bg="#27AE60", fg="white", font=("Helvetica", 14, "bold"), width=25).pack(pady=10)

        # Crear un frame separado para los comprobantes
        self.clientecomprobante_frame = tk.Frame(self.frame, bg="#34495E")
        self.clientecomprobante_frame.pack(pady=10, fill="x")

        # Vista del comprobante del cliente
        self.mostrar_comprobante_cliente()

        # Divisor
        self.crear_divisor()

        # Confirmación del pago
        confirm_frame = tk.Frame(self.frame, bg="#34495E")
        confirm_frame.pack(pady=15)
        tk.Label(confirm_frame, text="Tipo de Pago:", font=("Helvetica", 14), bg="#34495E", fg="white").pack(side="left")
        opciones_pago = ["Efectivo", "Consignación"]
        self.dropdown_pago = tk.OptionMenu(confirm_frame, self.tipo_pago_var, *opciones_pago)
        self.dropdown_pago.pack(side="left", padx=10)

        confirmar_button = tk.Button(self.frame, text="Confirmar Comprobante", command=self.confirmar_comprobante, bg="#218ff9", fg="white", font=("Helvetica", 14, "bold"), width=25)
        confirmar_button.pack(pady=20)

    def crear_divisor(self):
        """Crea un divisor horizontal para separar las secciones."""
        divisor = tk.Frame(self.frame, bg="white", height=1, bd=0)
        divisor.pack(fill="x", padx=5, pady=15)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_detalles_pedido(self):
        detalles_frame = tk.Frame(self.frame, bg="#34495E")
        detalles_frame.pack(pady=10, fill="x")

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

        for detalle in detalles_pedido:
            producto_id, producto_nombre, categoria_nombre, cantidad = detalle
            precio = get_precio_producto(producto_id)
            total_producto = cantidad * precio
            total += total_producto
            detalles += f"- {categoria_nombre} - {producto_nombre} x {cantidad} (${total_producto:,.0f})\n"

        detalles_label = tk.Label(detalles_frame, text=detalles, font=("Helvetica", 12), bg="#34495E", fg="white", justify=tk.LEFT)
        detalles_label.pack(pady=10)

        # Mostrar el total con letra más grande y en negrita
        total_label = tk.Label(self.frame, text=f"Total: ${total:,.0f}", font=("Helvetica", 14, "bold"), bg="#34495E", fg="white")
        total_label.pack(pady=5)

    def enviar_captura(self):
        """Generar y guardar el comprobante como una imagen JPG."""
        
        # Verificar si ya existe un comprobante
        folder_path = os.path.join(os.getcwd(), 'src', 'comprobantes')
        file_path = os.path.join(folder_path, f'comprobante_{self.pedido_id}.jpg')
        
        if os.path.exists(file_path):
            # Mostrar mensaje si el comprobante ya existe
            messagebox.showinfo("Aviso", "El comprobante ya ha sido generado y no se puede generar otro.")
        else:
            # Proceder a generar el comprobante si no existe
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
            os.makedirs(folder_path, exist_ok=True)  # Crear carpeta si no existe
            imagen.save(file_path)

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Comprobante generado y guardado en: {file_path}")

            # Mostrar el comprobante después de generarlo
            self.mostrar_comprobante_pedido()  # Llamada para mostrar la imagen descargada

    def subir_comprobante(self):
        filepath = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg")])
        if filepath:
            folder_path = os.path.join(os.getcwd(), 'src', 'clientes')
            os.makedirs(folder_path, exist_ok=True)
            file_extension = os.path.splitext(filepath)[1]
            destination = os.path.join(folder_path, f'comprobante_{self.pedido_id}{file_extension}')
            
            if os.path.exists(destination):
                messagebox.showerror("Error", "El pedido ya fue confirmado y hay un comprobante de pago del cliente cargado.")
            else:
                os.rename(filepath, destination)
                self.comprobante_subido = destination  # Actualiza la variable correctamente

                # Forzar actualización y verificar
                print(f"Archivo subido: {self.comprobante_subido}")
                
                # Muestra el mensaje de éxito y actualiza la vista
                messagebox.showinfo("Éxito", "Comprobante subido correctamente.")
                self.mostrar_comprobante_cliente()

                # Verificar si el archivo realmente existe
                if not os.path.exists(self.comprobante_subido):
                    print("Error: el archivo no se encuentra donde debería estar.")
        else:
            self.comprobante_subido = None

    def mostrar_comprobante_pedido(self):
        # Limpiar cualquier contenido anterior del frame
        for widget in self.descargarcomprobante_frame.winfo_children():
            widget.destroy()

        folder_path = os.path.join(os.getcwd(), 'src', 'comprobantes')
        file_path = os.path.join(folder_path, f'comprobante_{self.pedido_id}.jpg')

        if os.path.exists(file_path):
            img = Image.open(file_path)
            img = img.resize((300, 200), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            label = tk.Label(self.descargarcomprobante_frame, text="Comprobante Pedido", font=("Helvetica", 12, "bold"), bg="#34495E", fg="white")
            label.pack(pady=5)
            img_label = tk.Label(self.descargarcomprobante_frame, image=img, bg="#34495E")
            img_label.image = img
            img_label.pack(pady=5)
        else:
            tk.Label(self.descargarcomprobante_frame, text="No se ha generado el comprobante del pedido.", font=("Helvetica", 12), bg="#34495E", fg="white").pack(pady=5)

    def mostrar_comprobante_cliente(self):
        # Limpiar cualquier contenido anterior del frame
        for widget in self.clientecomprobante_frame.winfo_children():
            widget.destroy()

        folder_path = os.path.join(os.getcwd(), 'src', 'clientes')
        file_path_jpg = os.path.join(folder_path, f'comprobante_{self.pedido_id}.jpg')
        file_path_png = os.path.join(folder_path, f'comprobante_{self.pedido_id}.png')
        
        file_path = file_path_jpg if os.path.exists(file_path_jpg) else (file_path_png if os.path.exists(file_path_png) else None)

        if file_path:
            img = Image.open(file_path)
            img = img.resize((300, 200), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            label = tk.Label(self.clientecomprobante_frame, text="Comprobante Cliente", font=("Helvetica", 12, "bold"), bg="#34495E", fg="white")
            label.pack(pady=5)
            img_label = tk.Label(self.clientecomprobante_frame, image=img, bg="#34495E")
            img_label.image = img  # Importante: mantener la referencia de la imagen
            img_label.pack(pady=5)
        else:
            tk.Label(self.clientecomprobante_frame, text="No se ha subido el comprobante del cliente.", font=("Helvetica", 12), bg="#34495E", fg="white").pack(pady=5)

    def confirmar_comprobante(self):
        # Verificar si el archivo existe en el directorio
        folder_path = os.path.join(os.getcwd(), 'src', 'clientes')
        file_path_jpg = os.path.join(folder_path, f'comprobante_{self.pedido_id}.jpg')
        file_path_png = os.path.join(folder_path, f'comprobante_{self.pedido_id}.png')
        
        file_path = file_path_jpg if os.path.exists(file_path_jpg) else (file_path_png if os.path.exists(file_path_png) else None)
        
        if file_path:
            estado_comprobante = comprobar_estado_comprobante(self.pedido_id)
            if estado_comprobante == "Confirmado por Cliente":
                messagebox.showinfo("Aviso", "El comprobante ya ha sido confirmado y no se puede modificar nuevamente.")
                return

            if messagebox.askyesno("Confirmación", "¿El cliente ya realizó el pago y se subió el comprobante?"):
                tiempo_llegada = self.tiempo_var.get() if self.pedido.mesa_id is None else None  # Solo para pedidos a domicilio
                tipo_pago = self.tipo_pago_var.get()
                
                confirmar_comprobante_cliente(self.pedido_id, True, tiempo_llegada, tipo_pago)
                messagebox.showinfo("Éxito", "Pedido confirmado.")
                self.parent.mostrar_historial()
                self.destroy()
            else:
                messagebox.showwarning("Información", "El pedido no ha sido confirmado.")
        else:
            messagebox.showerror("Error", "Debe subir un comprobante antes de confirmar.")

    def _on_mousewheel(self, event):
        """Permitir el desplazamiento con la rueda del ratón."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_close(self):
        """Desvincular el evento de la rueda del ratón cuando la ventana se cierra."""
        self.canvas.unbind_all("<MouseWheel>")
        self.destroy()
