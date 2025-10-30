import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# ===== COLORES BASE =====
COLOR_FONDO = "#e8eef1"
COLOR_CARD = "#ffffff"
COLOR_TEXTO = "#333333"
COLOR_BOTON_VERDE = "#28a745"
COLOR_BOTON_AMARILLO = "#ffc107"
COLOR_BOTON_ROJO = "#dc3545"
COLOR_BORDES = "#d0d4d9"
COLOR_TITULO = "#007bff"

# ===== CONEXIÓN BASE DE DATOS =====
def conectar_db():
    try:
        conexion = sqlite3.connect("database/database.db")
        return conexion
    except sqlite3.Error as error:
        print("Error al conectar a la base de datos", error)
        return None

# ===== CARGAR PRODUCTOS =====
def cargar_productos():
    conn = conectar_db()
    if conn is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    tabla.delete(*tabla.get_children())

    productos = c.fetchall()
    if productos:
        for producto in productos:
            tabla.insert('', 'end', values=producto)
    else:
        messagebox.showinfo("Información", "No se encontraron productos en la base de datos.")

    conn.close()

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

    conn = conectar_db()
    if conn is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        c = conn.cursor()
        c.execute("SELECT * FROM productos WHERE nombre = ? AND descripcion = ?", (nombre, descripcion))
        if c.fetchone():
            messagebox.showwarning("Advertencia", "Ya existe un producto con el mismo nombre y descripción.")
            return

        c.execute('''
            INSERT INTO productos (nombre, descripcion, precio, existencia, fecha_alta, unidad)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, precio, existencia, fecha_actual, unidad))

        conn.commit()
        tabla.insert('', 'end', values=(c.lastrowid, nombre, descripcion, precio, existencia, fecha_actual, unidad))
        messagebox.showinfo("Éxito", "Producto agregado correctamente")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al guardar: {e}")
    finally:
        conn.close()
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

    conn = conectar_db()
    c = conn.cursor()
    c.execute("SELECT * FROM productos WHERE nombre = ? AND descripcion = ? AND id != ?", 
              (nombre, descripcion, producto_id))
    if c.fetchone():
        messagebox.showwarning("Error", "Ya existe un producto con el mismo nombre y descripción.")
        conn.close()
        return

    c.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, precio = ?, existencia = ?, unidad = ?, fecha_alta = ?
        WHERE id = ?
    ''', (nombre, descripcion, precio, existencia, unidad, fecha_actual, producto_id))
    conn.commit()
    conn.close()

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
    conn = conectar_db()
    c = conn.cursor()
    c.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()

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


# ===== VENTANA PRINCIPAL =====
ventana_crud_productos = tk.Tk()
ventana_crud_productos.title("CRUD de Productos")
ventana_crud_productos.geometry("900x600")
ventana_crud_productos.config(bg=COLOR_FONDO)

# ===== TÍTULO =====
tk.Label(
    ventana_crud_productos, text="📦 CRUD de Productos",
    font=("Segoe UI", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO
).pack(pady=20)

# ===== BOTÓN REGRESAR =====
boton_regresar_productos = tk.Button(
    ventana_crud_productos, text="← Regresar", font=("Segoe UI", 11, "bold"),
    bg=COLOR_FONDO, fg=COLOR_TITULO, relief="flat", cursor="hand2", command=regresar
)
boton_regresar_productos.place(x=20, y=20)

# ===== FORMULARIO =====
frame_formulario = tk.Frame(ventana_crud_productos, bg=COLOR_CARD, relief="groove", bd=2)
frame_formulario.pack(padx=30, pady=15, fill="x")

def crear_campo(texto):
    frame = tk.Frame(frame_formulario, bg=COLOR_CARD)
    frame.pack(fill="x", pady=6)
    label = tk.Label(frame, text=texto, font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg="#444")
    label.pack(side="left", padx=10)
    entry = tk.Entry(frame, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDES)
    entry.pack(side="right", padx=10, ipadx=10, ipady=4, fill="x", expand=True)
    return entry

entry_nombre = crear_campo("Nombre:")
entry_descripcion = crear_campo("Descripción:")
entry_precio = crear_campo("Precio Unitario:")
entry_existencia = crear_campo("Existencia:")
entry_unidad = crear_campo("Unidad de Medida:")

# ===== BOTONES CRUD =====
frame_botones = tk.Frame(ventana_crud_productos, bg=COLOR_FONDO)
frame_botones.pack(pady=10)

def crear_boton_crud(texto, color, comando):
    boton = tk.Button(
        frame_botones, text=texto, font=("Segoe UI", 12, "bold"),
        bg=color, fg="white", relief="flat", width=12, height=1,
        command=comando, cursor="hand2", activebackground=color
    )
    boton.pack(side="left", padx=15, pady=10)
    return boton

crear_boton_crud("Agregar", COLOR_BOTON_VERDE, agregar_producto)
crear_boton_crud("Modificar", COLOR_BOTON_AMARILLO, modificar_producto)
crear_boton_crud("Eliminar", COLOR_BOTON_ROJO, eliminar_producto)

# ===== TABLA =====
frame_tabla = tk.Frame(ventana_crud_productos, bg=COLOR_FONDO)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=15)

estilo = ttk.Style()
estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
estilo.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#007bff", foreground="white")

tabla = ttk.Treeview(frame_tabla, columns=("id", "producto", "descripcion", "precio", "existencia", "fecha_alta", "unidad"), show="headings")

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
