import tkinter as tk
from tkinter import ttk
from controllers.pedido_controller import get_pedidos_confirmados, delete_pedido
from controllers.producto_controller import get_precio_producto
from views.editar_pedido import EditarPedidoView
from views.comprobante_view import ComprobanteView
import os

class HistorialPedidosView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Pedidos - Beef Point")
        self.geometry("800x450")  # Dimensiones más equilibradas
        self.configure(bg="#2C3E50")

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        # Canvas y scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0, bg="#2C3E50")
        self.frame = tk.Frame(self.canvas, bg="#2C3E50")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Vincular la rueda del mouse al canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Mostrar historial de pedidos
        self.mostrar_historial()

    def _on_mousewheel(self, event):
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

    def mostrar_historial(self):
        pedidos, detalles = get_pedidos_confirmados()

        for widget in self.frame.winfo_children():
            widget.destroy()

        for pedido in pedidos:
            pedido_id = pedido[0]
            mesa_o_domicilio = f"Domicilio - Cliente: {pedido[3]}, Dirección: {pedido[4]}" if pedido[1] is None else f"Mesa: {pedido[1]}"
            trabajador = pedido[2]
            estado_comprobante = pedido[5]  # Estado del comprobante

            # Verificación del estado del comprobante
            print(f"Pedido ID: {pedido_id}, Estado Comprobante: {estado_comprobante}")

            pedido_label = tk.Label(self.frame, text=f"Pedido ID: {pedido_id}", font=("Helvetica", 14, "bold"), fg="#218ff9", bg="#2C3E50")
            pedido_label.pack(anchor="w", padx=10, pady=5)

            detalles_label = tk.Label(self.frame, text=f"{mesa_o_domicilio}, Trabajador: {trabajador}", font=("Helvetica", 12), fg="#BDC3C7", bg="#2C3E50")
            detalles_label.pack(anchor="w", padx=20, pady=5)

            total_pedido = 0

            for producto_id, producto_nombre, cantidad in detalles[pedido_id]:
                precio_producto = get_precio_producto(producto_id)
                total_producto = precio_producto * cantidad
                total_pedido += total_producto
                detalle_label = tk.Label(self.frame, text=f"  - {producto_nombre}: {cantidad} (${total_producto:,.0f})", font=("Helvetica", 11), fg="#ECF0F1", bg="#2C3E50")
                detalle_label.pack(anchor="w", padx=30)

            total_label = tk.Label(self.frame, text=f"Total: ${total_pedido:,.0f}", font=("Helvetica", 12, "bold"), fg="#ECF0F1", bg="#2C3E50")
            total_label.pack(anchor="w", padx=30, pady=5)

            button_frame = tk.Frame(self.frame, bg="#2C3E50")
            button_frame.pack(anchor="w", padx=20, pady=5)

            # Mostrar el botón de comprobante siempre
            comprobante_button = tk.Button(button_frame, text="Comprobante", command=lambda pid=pedido_id: self.mostrar_comprobante(pid), bg="#27AE60", fg="white", font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2")
            comprobante_button.pack(side="left", padx=5)

            # Condiciones para los roles que pueden Editar y Eliminar
            if self.master.trabajador.rol in ['Administrador', 'Mesero', 'Auxiliar Cocina']:
                # Mostrar botones de editar y eliminar si el comprobante no ha sido confirmado
                if estado_comprobante != 'Confirmado por Cliente':
                    edit_button = tk.Button(button_frame, text="Editar", command=lambda pid=pedido_id: self.editar_pedido(pid), bg="#218ff9", fg="white", font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2")
                    edit_button.pack(side="left", padx=5)

                    delete_button = tk.Button(button_frame, text="Eliminar", command=lambda pid=pedido_id: self.eliminar_pedido(pid), bg="#E74C3C", fg="white", font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2")
                    delete_button.pack(side="left", padx=5)

            # Condiciones para los roles que solo pueden acceder al comprobante (Domiciliario y Co-propietario)
            elif self.master.trabajador.rol in ['Domiciliario', 'Co-propietario', 'Chef']:
                # Solo se muestra el botón de comprobante, ya que no pueden editar ni eliminar
                pass

            separator = tk.Label(self.frame, text="─" * 60, fg="#7F8C8D", bg="#2C3E50")
            separator.pack(pady=10)

        self.bind_scroll_event()

    def bind_scroll_event(self):
        """Vincular el evento de scroll con la rueda del mouse."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def editar_pedido(self, pedido_id):
        EditarPedidoView(self, pedido_id)
        # Actualizar el historial de pedidos después de cerrar la ventana de edición
        self.wait_window(self.winfo_children()[-1])
        self.mostrar_historial()

    def eliminar_pedido(self, pedido_id):
        if tk.messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este pedido?"):
            delete_pedido(pedido_id)
            tk.messagebox.showinfo("Éxito", "Pedido eliminado.")
            self.mostrar_historial()

    def mostrar_comprobante(self, pedido_id):
        # Pasamos 'self' como parent
        ComprobanteView(self, pedido_id)  
        self.wait_window(self.winfo_children()[-1])
        self.mostrar_historial()



