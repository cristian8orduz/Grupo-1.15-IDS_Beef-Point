import sqlite3
from database import connect
from models.producto import Producto

def get_productos_by_categoria(categoria_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE categoria_id = ?", (categoria_id,))
    rows = cursor.fetchall()
    conn.close()

    return [Producto(*row) for row in rows]

def create_producto(nombre, categoria_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, categoria_id) VALUES (?, ?)", (nombre, categoria_id))
    conn.commit()
    conn.close()
