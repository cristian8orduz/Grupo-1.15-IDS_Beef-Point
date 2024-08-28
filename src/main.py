import tkinter as tk
from database import create_tables
from views.login import LoginView

def main():
    create_tables()  # Crea las tablas si no existen
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    login = LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
