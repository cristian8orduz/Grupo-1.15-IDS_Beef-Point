import tkinter as tk
from tkinter import messagebox
from controllers.trabajador_controller import get_trabajador_by_usuario
import os

class LoginView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Iniciar Sesión - Beef Point")
        self.geometry("400x250")
        self.configure(bg="#F0F0F0")  # Color de fondo suave
        
        # Centrar la ventana
        self.center_window()
        
        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        label_style = {
            "font": ("Arial", 12),
            "bg": "#F0F0F0"
        }

        entry_style = {
            "font": ("Arial", 12),
            "bd": 2,
            "relief": "groove"
        }

        # Estilo del botón de inicio de sesión
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#4CAF50",  # Color verde suave
            "fg": "white",  # Color de texto blanco
            "activebackground": "#45A049",
            "bd": 0,
            "relief": "flat",
            "width": 15,
            "height": 2
        }

        # Usuario
        self.label_usuario = tk.Label(self, text="Usuario", **label_style)
        self.label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self, **entry_style)
        self.entry_usuario.pack(pady=5)

        # Contraseña
        self.label_password = tk.Label(self, text="Contraseña", **label_style)
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*", **entry_style)
        self.entry_password.pack(pady=5)

        # Botón de inicio de sesión
        self.button_login = tk.Button(self, text="Iniciar Sesión", command=self.login, **button_style)
        self.button_login.pack(pady=20)

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

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
