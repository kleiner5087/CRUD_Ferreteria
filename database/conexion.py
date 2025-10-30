import sqlite3

# Variable de conexión
conexion = None

try:
    # Establecer la conexión con la base de datos
    conexion = sqlite3.connect("database/database.db")
    cursor = conexion.cursor()
    
    # Crear tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Usuario VARCHAR(50),
            Contraseña VARCHAR(50),
            Email VARCHAR(100),
            Tel VARCHAR(20)
        );
    """)

    # Crear tabla productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT,
            precio DECIMAL(10, 2),
            existencia INTEGER,
            fecha_alta DATE,
            unidad VARCHAR(50)
        );
    """)

    # Crear tabla clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            tel VARCHAR(20),
            direccion VARCHAR(100),
            rfc VARCHAR(13),
            fecha_nac DATE
        );
    """)

    # Confirmar cambios
    conexion.commit()

except Exception as ex:
    print("Ocurrió un error:", ex)


