import sqlite3
from database import connect
from models.producto import Producto
from models.categoria import Categoria

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

def update_precio_producto(producto_id, nuevo_precio):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, producto_id))
    conn.commit()
    conn.close()

def delete_producto(producto_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()

def get_precio_producto(producto_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT precio FROM productos WHERE id = ?", (producto_id,))
    precio = cursor.fetchone()[0]
    conn.close()
    return precio

def get_all_categorias():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    rows = cursor.fetchall()
    conn.close()
    return [Categoria(*row) for row in rows]