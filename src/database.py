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
        password TEXT NOT NULL,
        rol TEXT NOT NULL  -- Añadir columna rol
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
        precio REAL NOT NULL DEFAULT 0, -- Agregar columna de precio
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mesa_id INTEGER,
        trabajador_id INTEGER NOT NULL,
        fecha_hora TEXT NOT NULL,
        estado TEXT NOT NULL,
        estado_trabajador TEXT DEFAULT 'En preparación',  -- Nueva columna con valor predeterminado
        direccion TEXT,
        numero_contacto TEXT,
        nombre_cliente TEXT,
        tiempo_llegada TEXT,
        tipo_pago TEXT,
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

    # Insertar trabajadores con roles
    trabajadores = [
        ('Cristian Plazas', 'cplazas', 'clave1', 'Administrador'),
        ('Samuel Gutiérrez', 'gsamuel', 'clave2', 'Administrador'),
        ('Santiago Lopez', 'slopez', 'clave3', 'Administrador'),
        ('Jorge Pérez', 'mesero', 'mesero', 'Mesero'),
        ('María Rojas', 'domiciliario', 'domiciliario', 'Domiciliario'),
        ('Lucía Martínez', 'chef', 'chef', 'Chef'),
        ('Carlos Sánchez', 'auxiliar', 'auxiliar', 'Auxiliar Cocina'),
        ('Ana Torres', 'Copropietario', 'Copropietario', 'Co-propietario')
    ]
    cursor.executemany('''
    INSERT INTO trabajadores (nombre, usuario, password, rol) VALUES (?, ?, ?, ?)
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
        ('Patacones con Hogao', categorias_dict['Entradas'], 8000),
        ('Butifarras', categorias_dict['Entradas'], 9000),
        ('Deditos de Yuca', categorias_dict['Entradas'], 7000),
        ('Morcilla', categorias_dict['Entradas'], 8500),
        ('Carne de Res', categorias_dict['Carnes'], 22000),
        ('Carne de Cerdo', categorias_dict['Carnes'], 18000),
        ('Pollo', categorias_dict['Carnes'], 15000),
        ('Hamburguesa Tradicional', categorias_dict['Hamburguesas'], 16000),
        ('Hamburguesa Argentina', categorias_dict['Hamburguesas'], 18000),
        ('Hamburguesa Super Beef', categorias_dict['Hamburguesas'], 20000),
        ('Arepa', categorias_dict['Otros'], 4000),
        ('Patacón', categorias_dict['Otros'], 5000),
        ('Papas Beef', categorias_dict['Otros'], 7000),
        ('Chicken Bacon', categorias_dict['Otros'], 12000),
        ('Nuggets', categorias_dict['Infantil'], 9000),
        ('Salchipapa', categorias_dict['Infantil'], 10000),
        ('Jugo', categorias_dict['Bebidas'], 4000),
        ('Gaseosa', categorias_dict['Bebidas'], 3000),
        ('Cerveza', categorias_dict['Bebidas'], 7000),
    ]
    cursor.executemany('''
    INSERT INTO productos (nombre, categoria_id, precio) VALUES (?, ?, ?)
    ''', productos)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_initial_data()
