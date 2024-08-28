import sqlite3
from database import connect
from models.mesa import Mesa

def get_all_mesas():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mesas")
    rows = cursor.fetchall()
    conn.close()

    return [Mesa(*row) for row in rows]

def create_mesa(numero):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mesas (numero) VALUES (?)", (numero,))
    conn.commit()
    conn.close()
