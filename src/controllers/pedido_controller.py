import sqlite3
from database import connect
from models.pedido import Pedido
from models.pedido_detalle import PedidoDetalle
from models.categoria import Categoria  # Asegúrate de importar la clase Categoria
from models.producto import Producto

def create_pedido(mesa_id, trabajador_id, estado, direccion=None, numero_contacto=None, nombre_cliente=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO pedidos (mesa_id, trabajador_id, fecha_hora, estado, direccion, numero_contacto, nombre_cliente) 
    VALUES (?, ?, datetime('now'), ?, ?, ?, ?)
    ''', (mesa_id, trabajador_id, estado, direccion, numero_contacto, nombre_cliente))
    pedido_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pedido_id

def get_pedido(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Pedido(*row)
    return None

def get_pedidos_pendientes():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE estado = 'Pendiente'")
    rows = cursor.fetchall()
    conn.close()

    return [Pedido(*row) for row in rows]

def add_producto_to_pedido(pedido_id, producto_id, cantidad):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)",
                   (pedido_id, producto_id, cantidad))
    conn.commit()
    conn.close()

def confirmar_pedido(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET estado = 'Confirmado' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()

def get_detalle_by_pedido(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, c.nombre AS categoria, pd.cantidad
        FROM pedido_detalle pd
        JOIN productos p ON pd.producto_id = p.id
        JOIN categorias c ON p.categoria_id = c.id
        WHERE pd.pedido_id = ?
    """, (pedido_id,))
    rows = cursor.fetchall()
    conn.close()

    return rows

def cancelar_pedido(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET estado = 'Cancelado' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()

def get_pedidos_confirmados():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.mesa_id, t.nombre, p.nombre_cliente, p.direccion
        FROM pedidos p
        JOIN trabajadores t ON p.trabajador_id = t.id
        WHERE p.estado = 'Confirmado'
    """)
    pedidos = cursor.fetchall()

    detalles = {}
    for pedido in pedidos:
        pedido_id = pedido[0]
        cursor.execute("""
            SELECT pr.nombre, pd.cantidad
            FROM pedido_detalle pd
            JOIN productos pr ON pd.producto_id = pr.id
            WHERE pd.pedido_id = ?
        """, (pedido_id,))
        detalles[pedido_id] = cursor.fetchall()

    conn.close()
    return pedidos, detalles

def delete_pedido(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido_detalle WHERE pedido_id = ?", (pedido_id,))
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()

def update_producto_cantidad(pedido_id, producto_id, nueva_cantidad):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedido_detalle 
        SET cantidad = ? 
        WHERE pedido_id = ? AND producto_id = ?
    """, (nueva_cantidad, pedido_id, producto_id))
    conn.commit()
    conn.close()

def get_all_categorias():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    rows = cursor.fetchall()
    conn.close()
    return [Categoria(*row) for row in rows]

def get_productos_by_categoria(categoria_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE categoria_id = ?", (categoria_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Producto(*row) for row in rows]

def delete_producto_from_pedido(pedido_id, producto_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido_detalle WHERE pedido_id = ? AND producto_id = ?", (pedido_id, producto_id))
    conn.commit()
    conn.close()
