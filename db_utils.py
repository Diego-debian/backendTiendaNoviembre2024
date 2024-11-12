import sqlite3

def get_db_connection():
    conn =  sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def ini_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios(
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(80) NOT NULL,
            apellido TEXT NOT NULL,
            telefono BIGINT(11) NOT NULL,
            direccion TEXT NOT NULL
                       )
                       """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Productos(
            idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(80) NOT NULL,
            descripcion TEXT NOT NULL
                       )
                       """)
        conn.commit()
