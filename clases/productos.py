from clases.repository import get_all_products


class Producto:
    def obtener_productos(self):
        data = get_all_products()
        productos = []
        for registro in data:
            id, nombre, descripcion, precio, existencia, fecha_alta, unidad = registro
            productos.append(
                {
                    "id": str(id),
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio": precio,
                    "existencia": str(existencia),
                    "fecha_alta": fecha_alta,
                    "unidad": unidad,
                }
            )
        return productos

    def actualizar_existencia(self, producto_id, cantidad):
        # Si se necesita lógica específica para decrementar inventario,
        # se puede implementar aquí o en el repository.
        from database.conexion import conexion
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET existencia = existencia - ? WHERE id = ?", (cantidad, producto_id))
        conexion.commit()
        cursor.close()
        print(f"✅ Producto ID {producto_id}: se descontaron {cantidad} unidades del inventario")