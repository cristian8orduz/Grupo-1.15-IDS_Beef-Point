import sqlite3
from config import DATABASE_PATH

def connect():
    """Establece una conexión a la base de datos."""
    return sqlite3.connect(DATABASE_PATH)

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Crear tablas (lo mismo que antes)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabajadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    ''')

    # Agregar columna tipo_pedido para identificar si es Mesa o Domicilio
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mesa_id INTEGER,
        trabajador_id INTEGER NOT NULL,
        fecha_hora TEXT NOT NULL,
        estado TEXT NOT NULL,
        direccion TEXT,
        numero_contacto TEXT,
        nombre_cliente TEXT,
        tipo_pedido TEXT DEFAULT 'Mesa',
        FOREIGN KEY (mesa_id) REFERENCES mesas(id),
        FOREIGN KEY (trabajador_id) REFERENCES trabajadores(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedido_detalle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

   # Crear tabla para registrar comprobantes de pedidos de domicilio o mesa
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comprobantes_domicilio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        fecha_hora TEXT NOT NULL,
        estado_comprobante TEXT NOT NULL,
        captura_enviada_cliente TEXT,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
    )
    ''')

    conn.commit()
    conn.close()

def insert_initial_data():
    conn = connect()
    cursor = conn.cursor()

    # Insertar trabajadores
    trabajadores = [
        ('Cristian Plazas', 'cplazas', 'clave1'),
        ('Samuel Gutiérrez', 'gsamuel', 'clave2'),
        ('Santiago Lopez', 'slopez', 'clave3'),
    ]
    cursor.executemany('''
    INSERT INTO trabajadores (nombre, usuario, password) VALUES (?, ?, ?)
    ''', trabajadores)

    # Insertar mesas
    mesas = [(i,) for i in range(1, 11)]
    cursor.executemany('''
    INSERT INTO mesas (numero) VALUES (?)
    ''', mesas)

    # Insertar categorías
    categorias = [
        ('Entradas',),
        ('Carnes',),
        ('Hamburguesas',),
        ('Otros',),
        ('Infantil',),
        ('Bebidas',),
    ]
    cursor.executemany('''
    INSERT INTO categorias (nombre) VALUES (?)
    ''', categorias)

    # Obtener los IDs de las categorías para insertar los productos
    cursor.execute("SELECT id, nombre FROM categorias")
    categorias_dict = {nombre: id for id, nombre in cursor.fetchall()}

    # Insertar productos
    productos = [
        ('Patacones con Hogao', categorias_dict['Entradas']),
        ('Butifarras', categorias_dict['Entradas']),
        ('Deditos de Yuca', categorias_dict['Entradas']),
        ('Morcilla', categorias_dict['Entradas']),
        ('Carne de Res', categorias_dict['Carnes']),
        ('Carne de Cerdo', categorias_dict['Carnes']),
        ('Pollo', categorias_dict['Carnes']),
        ('Hamburguesa Tradicional', categorias_dict['Hamburguesas']),
        ('Hamburguesa Argentina', categorias_dict['Hamburguesas']),
        ('Hamburguesa Super Beef', categorias_dict['Hamburguesas']),
        ('Arepa', categorias_dict['Otros']),
        ('Patacón', categorias_dict['Otros']),
        ('Papas Beef', categorias_dict['Otros']),
        ('Chicken Bacon', categorias_dict['Otros']),
        ('Nuggets', categorias_dict['Infantil']),
        ('Salchipapa', categorias_dict['Infantil']),
        ('Jugo', categorias_dict['Bebidas']),
        ('Gaseosa', categorias_dict['Bebidas']),
        ('Cerveza', categorias_dict['Bebidas']),
    ]
    cursor.executemany('''
    INSERT INTO productos (nombre, categoria_id) VALUES (?, ?)
    ''', productos)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_initial_data()
