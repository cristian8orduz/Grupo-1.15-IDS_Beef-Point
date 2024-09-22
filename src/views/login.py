import tkinter as tk
from tkinter import messagebox
from controllers.trabajador_controller import get_trabajador_by_usuario
import os

class LoginView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Iniciar Sesión - Beef Point")
        self.geometry("450x300")
        self.configure(bg="#2C3E50")  # Fondo oscuro profesional
        
        # Centrar la ventana
        self.center_window()

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        # Logo o título en la parte superior
        self.label_logo = tk.Label(self, text="Beef Point", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="#218ff9")
        self.label_logo.pack(pady=20)

        # Estilo de los campos de entrada
        entry_style = {
            "font": ("Helvetica", 12),
            "bd": 2,
            "relief": "flat",
            "highlightthickness": 1,
            "highlightcolor": "#218ff9",
            "highlightbackground": "#34495E"
        }

        # Estilo de las etiquetas
        label_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#2C3E50",
            "fg": "white"
        }

        # Usuario
        self.label_usuario = tk.Label(self, text="Usuario", **label_style)
        self.label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self, **entry_style)
        self.entry_usuario.pack(pady=5, padx=40)

        # Contraseña
        self.label_password = tk.Label(self, text="Contraseña", **label_style)
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*", **entry_style)
        self.entry_password.pack(pady=5, padx=40)

        # Estilo del botón de inicio de sesión
        self.button_login = tk.Button(self, text="Iniciar Sesión", command=self.login,
                                      font=("Helvetica", 12, "bold"),
                                      bg="#218ff9", fg="white",
                                      activebackground="#1b73c8",
                                      bd=0, relief="flat", cursor="hand2")
        self.button_login.pack(pady=20)
        self.button_login.bind("<Enter>", lambda e: self.button_login.config(bg="#1b73c8"))
        self.button_login.bind("<Leave>", lambda e: self.button_login.config(bg="#218ff9"))

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

        # Verificar si ambos campos están llenos
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        trabajador = get_trabajador_by_usuario(usuario)
        
        # Verificar si se encontró un trabajador y si la contraseña es correcta
        if trabajador:
            if trabajador.password == password:
                messagebox.showinfo("Éxito", f"Bienvenido {trabajador.nombre}")
                self.destroy()  # Cierra la ventana de inicio de sesión
                from views.menu_principal import MenuPrincipalView  # Importación movida aquí
                MenuPrincipalView(self.parent, trabajador)  # Abre la vista del menú principal
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")


