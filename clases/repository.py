from database.conexion import conexion

def fetch_all(table, columns='*'):
    cursor = conexion.cursor()
    cursor.execute(f"SELECT {columns} FROM {table}")
    data = cursor.fetchall()
    cursor.close()
    return data

# ---- Productos ----
def get_all_products():
    return fetch_all('productos')

def add_product(nombre, descripcion, precio, existencia, fecha_alta, unidad):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT 1 FROM productos WHERE nombre = ? AND descripcion = ?", (nombre, descripcion))
        if cursor.fetchone():
            return False, "exists"

        cursor.execute(
            'INSERT INTO productos (nombre, descripcion, precio, existencia, fecha_alta, unidad) VALUES (?, ?, ?, ?, ?, ?)',
            (nombre, descripcion, precio, existencia, fecha_alta, unidad)
        )
        conexion.commit()
        lastid = cursor.lastrowid
        return True, lastid
    finally:
        cursor.close()

def update_product(producto_id, nombre, descripcion, precio, existencia, unidad, fecha_alta):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT 1 FROM productos WHERE nombre = ? AND descripcion = ? AND id != ?",
                       (nombre, descripcion, producto_id))
        if cursor.fetchone():
            return False, "exists"

        cursor.execute('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?, existencia = ?, unidad = ?, fecha_alta = ?
            WHERE id = ?
        ''', (nombre, descripcion, precio, existencia, unidad, fecha_alta, producto_id))
        conexion.commit()
        return True, None
    finally:
        cursor.close()

def delete_product(producto_id):
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conexion.commit()
        return True
    finally:
        cursor.close()

# ---- Clientes ----
def get_all_clients():
    return fetch_all('clientes')

def search_clients_by_rfc(partial_rfc):
    cursor = conexion.cursor()
    try:
        # Usamos LIKE para buscar RFCs que comiencen con el texto ingresado
        cursor.execute("SELECT * FROM clientes WHERE rfc LIKE ?", (f"{partial_rfc}%",))
        return cursor.fetchall()
    finally:
        cursor.close()

def add_client(nombre, email, tel, direccion, rfc, fecha_nac):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT 1 FROM clientes WHERE rfc = ?", (rfc,))
        if cursor.fetchone():
            return False, "exists"

        cursor.execute(
            "INSERT INTO clientes (nombre, email, tel, direccion, rfc, fecha_nac) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, email, tel, direccion, rfc, fecha_nac)
        )
        conexion.commit()
        return True, cursor.lastrowid
    finally:
        cursor.close()

def update_client(cliente_id, nombre, email, tel, direccion, rfc, fecha_nac):
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE clientes SET nombre=?, email=?, tel=?, direccion=?, rfc=?, fecha_nac=? WHERE id=?",
            (nombre, email, tel, direccion, rfc, fecha_nac, cliente_id)
        )
        conexion.commit()
        return True
    finally:
        cursor.close()

def delete_client(cliente_id):
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        conexion.commit()
        return True
    finally:
        cursor.close()

def search_products_by_name(partial_name):
    cursor = conexion.cursor()
    try:
        # Usamos LIKE para buscar productos cuyo nombre comience con el texto ingresado
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"{partial_name}%",))
        return cursor.fetchall()
    finally:
        cursor.close()

# ---- Usuarios ----
def get_user_by_credentials(usuario, contraseña):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE Usuario = ? AND Contraseña = ?", (usuario, contraseña))
        return cursor.fetchone()
    finally:
        cursor.close()

def create_user(usuario, contraseña, email, tel):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT 1 FROM usuarios WHERE Usuario = ?", (usuario,))
        if cursor.fetchone():
            return False, "exists"

        cursor.execute(
            "INSERT INTO usuarios (Usuario, Contraseña, Email, Tel) VALUES (?, ?, ?, ?)",
            (usuario, contraseña, email, tel)
        )
        conexion.commit()
        return True, cursor.lastrowid
    finally:
        cursor.close()

def get_user_by_email(email):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT Usuario, Contraseña FROM usuarios WHERE Email = ?", (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
