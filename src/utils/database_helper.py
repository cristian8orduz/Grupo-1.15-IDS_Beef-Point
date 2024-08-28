import sqlite3
from config import DATABASE_PATH

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return cursor

def fetch_one(query, params=()):
    cursor = execute_query(query, params)
    return cursor.fetchone()

def fetch_all(query, params=()):
    cursor = execute_query(query, params)
    return cursor.fetchall()
