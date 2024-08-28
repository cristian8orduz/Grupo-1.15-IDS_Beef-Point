import sqlite3
from database import connect
from models.categoria import Categoria

def get_all_categorias():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    rows = cursor.fetchall()
    conn.close()

    return [Categoria(*row) for row in rows]

def create_categoria(nombre):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()
