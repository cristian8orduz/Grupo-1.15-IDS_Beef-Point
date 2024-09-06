import sqlite3
from database import connect
from models.pedido import Pedido
from models.pedido_detalle import PedidoDetalle
from models.categoria import Categoria  # Asegúrate de importar la clase Categoria
from models.producto import Producto

# Crear pedido con tipo de pedido (Mesa o Domicilio)
def create_pedido(mesa_id, trabajador_id, estado, tipo_pedido='Mesa', direccion=None, numero_contacto=None, nombre_cliente=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO pedidos (mesa_id, trabajador_id, fecha_hora, estado, direccion, numero_contacto, nombre_cliente, tipo_pedido)
    VALUES (?, ?, datetime('now'), ?, ?, ?, ?, ?)
    ''', (mesa_id, trabajador_id, estado, direccion, numero_contacto, nombre_cliente, tipo_pedido))
    pedido_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pedido_id

def get_pedido(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, mesa_id, trabajador_id, fecha_hora, estado, direccion, numero_contacto, nombre_cliente, tipo_pedido 
        FROM pedidos WHERE id = ?
    """, (pedido_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Pedido(*row)  # Asegúrate de que el objeto Pedido incluya todos estos campos
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

    # Verificar si ya existe un detalle para el producto y pedido
    cursor.execute("""
        SELECT cantidad FROM pedido_detalle 
        WHERE pedido_id = ? AND producto_id = ?
    """, (pedido_id, producto_id))
    existing = cursor.fetchone()

    if existing:
        # Si existe, actualizar la cantidad
        cursor.execute("""
            UPDATE pedido_detalle 
            SET cantidad = ? 
            WHERE pedido_id = ? AND producto_id = ?
        """, (nueva_cantidad, pedido_id, producto_id))
    else:
        # Si no existe, insertar un nuevo registro
        cursor.execute("""
            INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad) 
            VALUES (?, ?, ?)
        """, (pedido_id, producto_id, nueva_cantidad))

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

def update_pedido_info(pedido_id, nombre_cliente, direccion, numero_contacto):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedidos 
        SET nombre_cliente = ?, direccion = ?, numero_contacto = ? 
        WHERE id = ?
    """, (nombre_cliente, direccion, numero_contacto, pedido_id))
    conn.commit()
    conn.close()

# Nueva función para enviar comprobante de domicilio o mesa
def enviar_comprobante(pedido_id):
    conn = connect()
    cursor = conn.cursor()

    # Obtener el tipo de pedido (Mesa o Domicilio)
    cursor.execute('SELECT tipo_pedido FROM pedidos WHERE id = ?', (pedido_id,))
    tipo_pedido = cursor.fetchone()[0]

    if tipo_pedido == 'Domicilio':
        estado_comprobante = 'Enviado Domicilio'
    else:
        estado_comprobante = 'Enviado Mesa'

    cursor.execute('''
    INSERT INTO comprobantes_domicilio (pedido_id, fecha_hora, estado_comprobante)
    VALUES (?, datetime('now'), ?)
    ''', (pedido_id, estado_comprobante))

    conn.commit()
    conn.close()

# Función para validar la recepción del comprobante
def validar_comprobante(pedido_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE comprobantes_domicilio
    SET estado_comprobante = 'Validado'
    WHERE pedido_id = ?
    ''', (pedido_id,))
    conn.commit()
    conn.close()

# Confirmar el comprobante si el cliente está de acuerdo
def confirmar_comprobante_cliente(pedido_id, cliente_acuerdo):
    conn = connect()
    cursor = conn.cursor()

    if cliente_acuerdo:
        # Cambiar el estado del comprobante a 'Confirmado por Cliente'
        cursor.execute('''
        UPDATE comprobantes_domicilio
        SET estado_comprobante = 'Confirmado por Cliente'
        WHERE pedido_id = ?
        ''', (pedido_id,))
        
        print("Comprobante confirmado por el cliente.")
    else:
        print("El cliente no está de acuerdo con el comprobante.")
    
    conn.commit()
    conn.close()

# El trabajador valida el comprobante y envía una captura al cliente
def validar_comprobante_y_enviar_captura(pedido_id, captura):
    conn = connect()
    cursor = conn.cursor()

    # Cambiar el estado del comprobante a 'Enviado al Cliente'
    cursor.execute('''
    UPDATE comprobantes_domicilio
    SET estado_comprobante = 'Validado por Trabajador', captura_enviada_cliente = ?
    WHERE pedido_id = ?
    ''', (captura, pedido_id))

    conn.commit()
    conn.close()

    print("Comprobante validado y captura enviada al cliente.")
