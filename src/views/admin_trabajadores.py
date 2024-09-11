import tkinter as tk
from tkinter import ttk, messagebox, Listbox
from controllers.trabajador_controller import create_trabajador, get_trabajador_by_usuario, update_trabajador, delete_trabajador, existe_usuario
import os

class AdminTrabajadoresView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Administrar Trabajadores - Beef Point")
        self.geometry("600x500")  # Aumentar la altura para incluir el campo de rol
        self.configure(bg="#2C3E50")

        # Centrar la ventana
        self.center_window()
        self.selected_id = None  # Variable para almacenar el ID seleccionado
        self.is_editing = False  # Bandera para gestionar si el usuario está editando

        # Establecer el icono de la ventana
        icon_path = os.path.join(os.path.dirname(__file__), '../assets/img/icon.ico')
        self.iconbitmap(icon_path)

        # Marco principal
        main_frame = tk.Frame(self, bg="#2C3E50")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Configurar columnas
        main_frame.grid_columnconfigure(0, weight=1)  # Etiquetas
        main_frame.grid_columnconfigure(1, weight=3)  # Entradas

        # Título
        tk.Label(main_frame, text="Gestión de Trabajadores", font=("Helvetica", 16, "bold"), bg="#2C3E50", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

        # Instrucciones
        tk.Label(main_frame, text="Selecciona un trabajador para modificar o eliminar.\nPara agregar un nuevo trabajador, completa los campos abajo y haz clic en 'Agregar'.", 
                 font=("Helvetica", 10), bg="#2C3E50", fg="white", justify="left").grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Nombre del trabajador
        tk.Label(main_frame, text="Nombre:", font=("Helvetica", 12), bg="#2C3E50", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.nombre_entry = tk.Entry(main_frame, font=("Helvetica", 12))
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Usuario
        tk.Label(main_frame, text="Usuario:", font=("Helvetica", 12), bg="#2C3E50", fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.usuario_entry = tk.Entry(main_frame, font=("Helvetica", 12))
        self.usuario_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Contraseña
        tk.Label(main_frame, text="Contraseña:", font=("Helvetica", 12), bg="#2C3E50", fg="white").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(main_frame, font=("Helvetica", 12), show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Rol del trabajador
        tk.Label(main_frame, text="Rol:", font=("Helvetica", 12), bg="#2C3E50", fg="white").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.rol_combobox = ttk.Combobox(main_frame, font=("Helvetica", 12), state="readonly", values=["Mesero", "Auxiliar Cocina", "Administrador", "Chef", "Domiciliario", "Co-propietario"])
        self.rol_combobox.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Botones de acción
        button_frame = tk.Frame(main_frame, bg="#2C3E50")
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Agregar", command=self.agregar_trabajador, font=("Helvetica", 12, "bold"), bg="#27AE60", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Modificar", command=self.modificar_trabajador, font=("Helvetica", 12, "bold"), bg="#F39C12", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Eliminar", command=self.eliminar_trabajador, font=("Helvetica", 12, "bold"), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cancelar Selección", command=self.cancelar_seleccion, font=("Helvetica", 12, "bold"), bg="#95A5A6", fg="white").pack(side=tk.LEFT, padx=10)

        # Crear un frame para contener el Listbox y el Scrollbar
        listbox_frame = tk.Frame(main_frame, bg="#2C3E50")
        listbox_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Crear el Listbox sin altura fija
        self.listbox_trabajadores = tk.Listbox(listbox_frame, font=("Helvetica", 12))
        self.listbox_trabajadores.grid(row=0, column=0, sticky="nsew")

        # Crear el Scrollbar y vincularlo al Listbox
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar el Listbox para usar el Scrollbar
        self.listbox_trabajadores.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_trabajadores.yview)

        # Expansión adecuada del Listbox y Scrollbar
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        # Asegurarte de que el frame principal también se expande
        main_frame.grid_rowconfigure(7, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Cargar trabajadores al iniciar
        self.cargar_trabajadores()

        # Vincular el evento de selección de la lista para cargar los datos en los campos
        self.listbox_trabajadores.bind('<<ListboxSelect>>', self.cargar_datos_trabajador)

        # Evitar que la selección del trabajador se pierda
        self.bind_eventos()

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def bind_eventos(self):
        """Vincula eventos especiales para evitar que los campos deseleccionen el trabajador."""
        campos = [self.nombre_entry, self.usuario_entry, self.password_entry, self.rol_combobox]

        # Evitar perder selección al interactuar con los campos de texto
        for campo in campos:
            campo.bind("<FocusIn>", self.comenzar_edicion)
            campo.bind("<FocusOut>", self.finalizar_edicion)

    def comenzar_edicion(self, event=None):
        """Bloquea el Listbox cuando empieza la edición."""
        self.is_editing = True
        self.listbox_trabajadores.config(state=tk.DISABLED)  # Deshabilitar la selección en el Listbox

    def finalizar_edicion(self, event=None):
        """Permite que el Listbox esté activo después de la edición."""
        self.is_editing = False
        self.listbox_trabajadores.config(state=tk.NORMAL)  # Habilitar nuevamente el Listbox

    def cancelar_seleccion(self):
        """Cancelar la selección actual y limpiar los campos."""
        self.selected_index = None
        self.selected_id = None  # Limpiar el ID seleccionado
        self.listbox_trabajadores.selection_clear(0, tk.END)  # Limpiar selección
        self.limpiar_campos()  # Limpiar los campos de entrada
        self.finalizar_edicion()

    def limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.nombre_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.rol_combobox.set('')

    def cargar_trabajadores(self):
        """Cargar los trabajadores en el listbox."""
        self.listbox_trabajadores.delete(0, tk.END)
        trabajadores = get_trabajador_by_usuario(None)  # Obtiene todos los trabajadores si usuario es None
        for trabajador in trabajadores:
            self.listbox_trabajadores.insert(tk.END, f"{trabajador.usuario} - {trabajador.nombre}")

    def cargar_datos_trabajador(self, event):
        """Cargar los datos del trabajador seleccionado en los campos de entrada."""
        if not self.is_editing:  # Solo cargar si no estamos editando
            selected = self.listbox_trabajadores.curselection()
            if selected:
                self.selected_index = selected[0]  # Guardar el índice seleccionado
                usuario = self.listbox_trabajadores.get(self.selected_index).split(" - ")[0]
                trabajador = get_trabajador_by_usuario(usuario)  # Obtener el trabajador por usuario
                if trabajador:  # Asegurarse de que el trabajador existe
                    self.selected_id = trabajador.id  # Guardar el ID del trabajador
                    self.nombre_entry.delete(0, tk.END)
                    self.nombre_entry.insert(0, trabajador.nombre)
                    self.usuario_entry.delete(0, tk.END)
                    self.usuario_entry.insert(0, trabajador.usuario)
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, trabajador.password)
                    self.rol_combobox.set(trabajador.rol)  # Cargar el rol en el combobox

    def agregar_trabajador(self):
        """Agregar un nuevo trabajador."""
        nombre = self.nombre_entry.get()
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        rol = self.rol_combobox.get()

        if nombre and usuario and password and rol:
            create_trabajador(nombre, usuario, password, rol)
            messagebox.showinfo("Éxito", "Trabajador agregado correctamente.")
            self.cargar_trabajadores()
            self.finalizar_edicion()  # Finalizar edición después de agregar
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def modificar_trabajador(self):
        """Modificar el trabajador seleccionado."""
        if self.selected_id is not None:
            nuevo_nombre = self.nombre_entry.get()
            nuevo_usuario = self.usuario_entry.get()
            nuevo_password = self.password_entry.get()
            nuevo_rol = self.rol_combobox.get()

            if nuevo_nombre and nuevo_usuario and nuevo_password and nuevo_rol:
                # Verificar si el nuevo usuario ya existe para otro trabajador
                if existe_usuario(nuevo_usuario, self.selected_id):
                    messagebox.showerror("Error", "El usuario ya está en uso por otro trabajador.")
                    return

                # Actualizar el trabajador
                update_trabajador(self.selected_id, nuevo_nombre, nuevo_usuario, nuevo_password, nuevo_rol)
                messagebox.showinfo("Éxito", "Trabajador modificado correctamente.")
                self.cargar_trabajadores()
                self.finalizar_edicion()  # Finalizar edición después de modificar
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
        else:
            messagebox.showerror("Error", "Debes seleccionar un trabajador.")

    def eliminar_trabajador(self):
        """Eliminar el trabajador seleccionado."""
        if self.selected_id is not None:
            delete_trabajador(self.selected_id)
            messagebox.showinfo("Éxito", "Trabajador eliminado correctamente.")
            self.cargar_trabajadores()
            self.finalizar_edicion()  # Finalizar edición después de eliminar
        else:
            messagebox.showerror("Error", "Debes seleccionar un trabajador.")
