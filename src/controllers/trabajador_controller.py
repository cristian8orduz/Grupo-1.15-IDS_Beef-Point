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
            return Trabajador(*row)  # Devolver un solo trabajador
        return None
    else:
        cursor.execute("SELECT * FROM trabajadores")
        rows = cursor.fetchall()
        conn.close()
        return [Trabajador(*row) for row in rows]  # Devolver lista de trabajadores

def create_trabajador(nombre, usuario, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trabajadores (nombre, usuario, password) VALUES (?, ?, ?)",
                   (nombre, usuario, password))
    conn.commit()
    conn.close()

def update_trabajador(id, nuevo_nombre, nuevo_usuario, nuevo_password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE trabajadores SET nombre = ?, usuario = ?, password = ? WHERE id = ?",
                   (nuevo_nombre, nuevo_usuario, nuevo_password, id))
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

