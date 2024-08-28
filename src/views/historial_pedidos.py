import tkinter as tk
from controllers.pedido_controller import get_pedidos_confirmados
import os

class HistorialPedidosView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Pedidos")
        self.geometry("500x500")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.label_historial = tk.Label(self, text="Historial de Pedidos Confirmados")
        self.label_historial.pack(pady=10)

        self.historial_frame = tk.Frame(self)
        self.historial_frame.pack(pady=20)

        self.mostrar_historial()

    def mostrar_historial(self):
        pedidos, detalles = get_pedidos_confirmados()

        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        for pedido in pedidos:
            pedido_id = pedido[0]
            mesa_o_domicilio = f"Domcilio" if pedido[1] is None else f"Mesa: {pedido[1]}"
            trabajador = pedido[2]

            label = tk.Label(self.historial_frame, text=f"Pedido ID: {pedido_id}, {mesa_o_domicilio}, Trabajador: {trabajador}")
            label.pack()

            # Mostrar detalles del pedido
            for producto, cantidad in detalles[pedido_id]:
                detalle_label = tk.Label(self.historial_frame, text=f"  - {producto}: {cantidad}")
                detalle_label.pack()

            separator = tk.Label(self.historial_frame, text="-" * 50)
            separator.pack()

