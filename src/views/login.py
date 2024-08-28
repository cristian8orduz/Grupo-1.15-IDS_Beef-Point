import tkinter as tk
from tkinter import messagebox
from controllers.trabajador_controller import get_trabajador_by_usuario
import os

class LoginView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Guarda la referencia al padre
        self.title("Iniciar Sesión - Beef Point")
        self.geometry("400x200")

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        self.label_usuario = tk.Label(self, text="Usuario")
        self.label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.label_password = tk.Label(self, text="Contraseña")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(self, text="Iniciar Sesión", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        trabajador = get_trabajador_by_usuario(usuario)
        if trabajador and trabajador.password == password:
            messagebox.showinfo("Éxito", f"Bienvenido {trabajador.nombre}")
            self.destroy()  # Cierra la ventana de inicio de sesión
            from views.menu_principal import MenuPrincipalView  # Importación movida aquí
            MenuPrincipalView(self.parent, trabajador)  # Abre la vista del menú principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
