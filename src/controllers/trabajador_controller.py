# src/controllers/trabajador_controller.py

import sqlite3
from database import connect
from models.trabajador import Trabajador

def get_trabajador_by_usuario(usuario=None):
    conn = connect()
    cursor = conn.cursor()
    
    if usuario:
        cursor.execute("SELECT * FROM trabajadores WHERE usuario = ?", (usuario,))
        row = cursor.fetchone()
        conn.close()
        if row:
            print(f"Usuario encontrado: {row}")  # Agregar depuración para verificar qué devuelve la base de datos
            return Trabajador(*row)  # Devolver un solo trabajador
        print("No se encontró el usuario.")  # Depuración si no se encontró el usuario
        return None
    else:
        cursor.execute("SELECT * FROM trabajadores")
        rows = cursor.fetchall()
        conn.close()
        return [Trabajador(*row) for row in rows]

def create_trabajador(nombre, usuario, password, rol):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trabajadores (nombre, usuario, password, rol) VALUES (?, ?, ?, ?)",
                   (nombre, usuario, password, rol))
    conn.commit()
    conn.close()

def update_trabajador(id, nuevo_nombre, nuevo_usuario, nuevo_password, nuevo_rol):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE trabajadores SET nombre = ?, usuario = ?, password = ?, rol = ? WHERE id = ?",
                   (nuevo_nombre, nuevo_usuario, nuevo_password, nuevo_rol, id))
    conn.commit()
    conn.close()

def delete_trabajador(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trabajadores WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def existe_usuario(usuario, id=None):
    conn = connect()
    cursor = conn.cursor()
    
    if id:
        # Verifica si existe un usuario con el mismo nombre pero distinto ID
        cursor.execute("SELECT id FROM trabajadores WHERE usuario = ? AND id != ?", (usuario, id))
    else:
        # Verifica si el usuario ya existe (para nuevas inserciones)
        cursor.execute("SELECT id FROM trabajadores WHERE usuario = ?", (usuario,))
        
    row = cursor.fetchone()
    conn.close()
    
    return row is not None  # Devuelve True si el usuario ya existe

