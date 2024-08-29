import tkinter as tk
from tkinter import ttk
from controllers.pedido_controller import get_pedidos_confirmados, delete_pedido
from views.editar_pedido import EditarPedidoView
import os
import platform

class HistorialPedidosView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Pedidos")
        self.geometry("800x400")  # Más ancho y menos alto

        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.label_historial = tk.Label(self, text="Historial de Pedidos Confirmados", font=("Arial", 16, "bold"))
        self.label_historial.pack(pady=10)

        # Crear un marco que contenga el Canvas y la Scrollbar
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Crear un canvas donde colocar los elementos con scroll
        self.canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Asociar el scroll con la rueda del ratón
        self.bind_scroll_event()

        self.historial_frame = scrollable_frame

        self.mostrar_historial()

    def bind_scroll_event(self):
        # Detectar plataforma para ajustar el scroll
        if platform.system() == 'Windows':
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", self.on_mousewheel)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel)

    def on_mousewheel(self, event):
        if self.canvas.winfo_exists():  # Verifica si el Canvas aún existe
            if platform.system() == 'Windows':
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                if event.num == 4:
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.canvas.yview_scroll(1, "units")

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

        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        for pedido in pedidos:
            pedido_id = pedido[0]
            mesa_o_domicilio = f"Domicilio - Cliente: {pedido[3]}, Dirección: {pedido[4]}" if pedido[1] is None else f"Mesa: {pedido[1]}"
            trabajador = pedido[2]

            pedido_label = tk.Label(self.historial_frame, text=f"Pedido ID: {pedido_id}", font=("Arial", 14, "bold"), fg="#333")
            pedido_label.pack(anchor="w", padx=10, pady=5)

            detalles_label = tk.Label(self.historial_frame, text=f"{mesa_o_domicilio}, Trabajador: {trabajador}", font=("Arial", 12))
            detalles_label.pack(anchor="w", padx=20, pady=5)

            # Mostrar detalles del pedido
            for producto, cantidad in detalles[pedido_id]:
                detalle_label = tk.Label(self.historial_frame, text=f"  - {producto}: {cantidad}", font=("Arial", 11))
                detalle_label.pack(anchor="w", padx=30)

            # Botones de Editar y Eliminar
            edit_button = tk.Button(self.historial_frame, text="Editar", command=lambda pid=pedido_id: self.editar_pedido(pid), bg="#FFA500", fg="white", font=("Arial", 10))
            edit_button.pack(anchor="w", padx=20, pady=5)

            delete_button = tk.Button(self.historial_frame, text="Eliminar", command=lambda pid=pedido_id: self.eliminar_pedido(pid), bg="#FF0000", fg="white", font=("Arial", 10))
            delete_button.pack(anchor="w", padx=20, pady=5)

            separator = tk.Label(self.historial_frame, text="─" * 60, fg="#888")
            separator.pack(pady=10)

    def editar_pedido(self, pedido_id):
        EditarPedidoView(self, pedido_id)

    def eliminar_pedido(self, pedido_id):
        if tk.messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este pedido?"):
            delete_pedido(pedido_id)
            tk.messagebox.showinfo("Éxito", "Pedido eliminado.")
            self.mostrar_historial()
