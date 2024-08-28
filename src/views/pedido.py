# src/views/pedido.py
import tkinter as tk
from controllers.mesa_controller import get_all_mesas
from controllers.pedido_controller import create_pedido
from views.producto_seleccion import ProductoSeleccionView
import os

class PedidoView(tk.Toplevel):
    def __init__(self, parent, trabajador):
        super().__init__(parent)
        self.title("Nuevo Pedido")
        self.geometry("400x300")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.trabajador = trabajador

        self.label_mesa = tk.Label(self, text="Seleccione la Mesa:")
        self.label_mesa.pack(pady=5)

        self.mesas = get_all_mesas()  # Carga todas las mesas disponibles
        self.mesa_var = tk.StringVar(self)
        self.mesa_var.set("Seleccionar Mesa")

        self.mesa_dropdown = tk.OptionMenu(self, self.mesa_var, *[mesa.numero for mesa in self.mesas])
        self.mesa_dropdown.pack(pady=10)

        self.button_crear_pedido = tk.Button(self, text="Crear Pedido", command=self.crear_pedido)
        self.button_crear_pedido.pack(pady=20)

    def crear_pedido(self):
        mesa_numero = self.mesa_var.get()
        # Encuentra la mesa correspondiente al número seleccionado
        mesa = next((m for m in self.mesas if str(m.numero) == mesa_numero), None)

        if mesa:
            # Crea el pedido y luego abre la vista para seleccionar productos
            pedido_id = create_pedido(mesa.id, self.trabajador.id, "Pendiente")
            self.destroy()
            ProductoSeleccionView(self.master, pedido_id)
        else:
            tk.messagebox.showerror("Error", "Debe seleccionar una mesa válida.")


