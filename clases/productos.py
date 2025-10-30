from database.conexion import conexion

class Producto:
    def obtener_productos(self):
        cursor = conexion.cursor()
        
        cursor.execute("SELECT * FROM productos")
        data = cursor.fetchall()
        productos = []
        
        for registro in data:
            id, nombre, descripcion, precio, existencia, fecha_alta, unidad = registro
            productos.append(
                {
                    "id": str(id),  # Convertir a string para consistencia
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio": precio,  # Convertir a string si se manejará todo como texto
                    "existencia": str(existencia),  # Convertir a string
                    "fecha_alta": fecha_alta,
                    "unidad": unidad,
                }
            )

        return productos

    def actualizar_existencia(self, producto_id, cantidad):
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET existencia = existencia - ? WHERE id = ?", 
                       (cantidad, producto_id))
        conexion.commit()
        cursor.close()
        print(f"✅ Producto ID {producto_id}: se descontaron {cantidad} unidades del inventario")