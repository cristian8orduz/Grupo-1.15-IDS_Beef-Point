import sqlite3
from database import connect
from models.trabajador import Trabajador

def get_trabajador_by_usuario(usuario):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trabajadores WHERE usuario = ?", (usuario,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Trabajador(*row)
    return None

def create_trabajador(nombre, usuario, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trabajadores (nombre, usuario, password) VALUES (?, ?, ?)",
                   (nombre, usuario, password))
    conn.commit()
    conn.close()
