import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from clases.repository import get_all_products, add_product, update_product, delete_product
from ventanas._utils import crear_campo, crear_boton, configurar_treeview_style

# ===== COLORES BASE =====
COLOR_FONDO = "#e8eef1"
COLOR_CARD = "#ffffff"
COLOR_BOTON_VERDE = "#28a745"
COLOR_BOTON_AMARILLO = "#ffc107"
COLOR_BOTON_ROJO = "#dc3545"
COLOR_BORDES = "#d0d4d9"
COLOR_TITULO = "#007bff"

# ===== CONEXIÓN BASE DE DATOS =====
def cargar_productos(ventana=None):
    productos = get_all_products()
    # Si la ventana no se pasa, usa la global (para compatibilidad)
    tabla_a_usar = ventana.tabla if ventana and hasattr(ventana, 'tabla') else tabla
    tabla_a_usar.delete(*tabla_a_usar.get_children())
    tabla.delete(*tabla.get_children())
    if productos:
        for producto in productos:
            tabla.insert('', 'end', values=producto)
    else:
        messagebox.showinfo("Información", "No se encontraron productos en la base de datos.")

# ===== FUNCIONES AUXILIARES =====
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_existencia.delete(0, tk.END)
    entry_unidad.delete(0, tk.END)

def validar_campos():
    if not entry_nombre.get() or not entry_descripcion.get() or not entry_precio.get() or not entry_existencia.get() or not entry_unidad.get():
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return False
    try:
        float(entry_precio.get())
        int(entry_existencia.get())
    except ValueError:
        messagebox.showerror("Error", "Precio debe ser decimal y existencia un número entero")
        return False
    return True

# ===== CRUD =====
def agregar_producto():
    if not validar_campos():
        return

    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    precio = float(entry_precio.get())
    existencia = int(entry_existencia.get())
    unidad = entry_unidad.get()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    success, info = add_product(nombre, descripcion, precio, existencia, fecha_actual, unidad)
    if not success:
        if info == "exists":
            messagebox.showwarning("Advertencia", "Ya existe un producto con el mismo nombre y descripción.")
        else:
            messagebox.showerror("Error", f"Error al guardar: {info}")
        return

    lastid = info
    tabla.insert('', 'end', values=(lastid, nombre, descripcion, precio, existencia, fecha_actual, unidad))
    messagebox.showinfo("Éxito", "Producto agregado correctamente")
    limpiar_campos()


def modificar_producto():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un producto para modificar")
        return

    producto_id = tabla.item(seleccion, 'values')[0]
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    precio = float(entry_precio.get())
    existencia = int(entry_existencia.get())
    unidad = entry_unidad.get()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    success, info = update_product(producto_id, nombre, descripcion, precio, existencia, unidad, fecha_actual)
    if not success:
        if info == "exists":
            messagebox.showwarning("Error", "Ya existe un producto con el mismo nombre y descripción.")
        else:
            messagebox.showerror("Error", f"Error al actualizar: {info}")
        return

    tabla.item(seleccion, values=(producto_id, nombre, descripcion, precio, existencia, fecha_actual, unidad))
    messagebox.showinfo("Éxito", "Producto modificado correctamente")
    limpiar_campos()


def eliminar_producto():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
        return
    if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el producto seleccionado?"):
        return

    producto_id = tabla.item(seleccion, 'values')[0]
    success = delete_product(producto_id)
    if not success:
        messagebox.showerror("Error", "No se pudo eliminar el producto")
        return

    tabla.delete(seleccion)
    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
    limpiar_campos()
    cargar_productos()


def seleccionar_producto(event):
    seleccion = tabla.selection()
    if seleccion:
        item = seleccion[0]
        valores = tabla.item(item)['values']
        limpiar_campos()
        entry_nombre.insert(0, valores[1])
        entry_descripcion.insert(0, valores[2])
        entry_precio.insert(0, valores[3])
        entry_existencia.insert(0, valores[4])
        entry_unidad.insert(0, valores[6])

def regresar():
    ventana_crud_productos.withdraw()
    ventana_crud_productos.regresar.deiconify()


# ===== Variables Globales de la Ventana =====
ventana_crud_productos = None
entry_nombre, entry_descripcion, entry_precio, entry_existencia, entry_unidad, tabla = (None,) * 6

def crear_ventana_crud_productos(ventana_padre):
    global ventana_crud_productos, entry_nombre, entry_descripcion, entry_precio, entry_existencia, entry_unidad, tabla
    if ventana_crud_productos is None or not ventana_crud_productos.winfo_exists():
        ventana_crud_productos = tk.Toplevel(ventana_padre)
        ventana_crud_productos.title("CRUD de Productos")
        ventana_crud_productos.geometry("1300x600")
        ventana_crud_productos.config(bg=COLOR_FONDO)
        ventana_crud_productos.regresar = ventana_padre # Guardamos la referencia para poder volver

        tk.Label(
            ventana_crud_productos, text="📦 CRUD de Productos",
            font=("Segoe UI", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO
        ).pack(pady=20)

        boton_regresar_productos = tk.Button(
            ventana_crud_productos, text="← Regresar", font=("Segoe UI", 11, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO, relief="flat", cursor="hand2", command=regresar
        )
        boton_regresar_productos.place(x=20, y=20)

        frame_formulario = tk.Frame(ventana_crud_productos, bg=COLOR_CARD, relief="groove", bd=2)
        frame_formulario.pack(padx=30, pady=15, fill="x")

        entry_nombre = crear_campo(frame_formulario, "Nombre:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_descripcion = crear_campo(frame_formulario, "Descripción:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_precio = crear_campo(frame_formulario, "Precio Unitario:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_existencia = crear_campo(frame_formulario, "Existencia:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_unidad = crear_campo(frame_formulario, "Unidad de Medida:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)

        frame_botones = tk.Frame(ventana_crud_productos, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        crear_boton(frame_botones, "Agregar", COLOR_BOTON_VERDE, agregar_producto, width=12, padx=15, pady=10)
        crear_boton(frame_botones, "Modificar", COLOR_BOTON_AMARILLO, modificar_producto, width=12, padx=15, pady=10)
        crear_boton(frame_botones, "Eliminar", COLOR_BOTON_ROJO, eliminar_producto, width=12, padx=15, pady=10)

        frame_tabla = tk.Frame(ventana_crud_productos, bg=COLOR_FONDO)
        frame_tabla.pack(fill="x", padx=20, pady=15)

        configurar_treeview_style(ventana_crud_productos)

        tabla = ttk.Treeview(
            frame_tabla, 
            columns=("id", "producto", "descripcion", "precio", "existencia", "fecha_alta", "unidad"), 
            show="headings"
        )
        ventana_crud_productos.tabla = tabla # Adjuntamos la tabla a la ventana

        for col, texto in zip(
            ("id", "producto", "descripcion", "precio", "existencia", "fecha_alta", "unidad"),
            ("ID", "Producto", "Descripción", "Precio", "Existencia", "Fecha Alta", "Unidad")
        ):
            tabla.heading(col, text=texto)
            tabla.column(col, anchor="center", stretch=True)

        tabla.bind('<<TreeviewSelect>>', seleccionar_producto)
        tabla.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        ventana_crud_productos.withdraw()
    return ventana_crud_productos
