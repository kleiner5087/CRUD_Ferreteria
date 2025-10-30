import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3, random, string, re

# ======= COLORES BASE =======
COLOR_FONDO = "#e8eef1"
COLOR_CARD = "#ffffff"
COLOR_TEXTO = "#333333"
COLOR_BORDES = "#cfd3d7"
COLOR_TITULO = "#007bff"
COLOR_VERDE = "#28a745"
COLOR_AMARILLO = "#ffc107"
COLOR_ROJO = "#dc3545"

# ======= CONEXIÓN =======
def conectar_db():
    try:
        conexion = sqlite3.connect("database/database.db")
        return conexion
    except sqlite3.Error as error:
        print("Error al conectar:", error)
        return None

# ======= CARGAR CLIENTES =======
def cargar_clientes():
    conn = conectar_db()
    if conn is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()

    tabla.delete(*tabla.get_children())
    if clientes:
        for cliente in clientes:
            tabla.insert('', 'end', values=cliente)
    else:
        messagebox.showinfo("Información", "No se encontraron clientes.")
    conn.close()

# ======= FUNCIONES AUXILIARES =======
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_fecha_nacimiento.delete(0, tk.END)

def generar_rfc(nombre_completo, fecha_nacimiento):
    partes = nombre_completo.split()
    if len(partes) < 2:
        raise ValueError("Debe incluir al menos un apellido y un nombre.")

    apellido_paterno = partes[0]
    apellido_materno = partes[1] if len(partes) > 2 else ""
    primer_nombre = partes[2] if len(partes) > 2 else partes[1]

    vocal_paterno = next((ch for ch in apellido_paterno[1:] if ch.lower() in "aeiou"), "")
    rfc = (apellido_paterno[:1] + vocal_paterno + (apellido_materno[:1] if apellido_materno else "") + primer_nombre[:1]).upper()
    fecha = datetime.strptime(fecha_nacimiento, "%d/%m/%Y").strftime("%y%m%d")
    homoclave = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return rfc + fecha + homoclave

def validar_campos():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()
    direccion = entry_direccion.get()
    fecha_nac = entry_fecha_nacimiento.get()

    if not all([nombre, correo, telefono, direccion, fecha_nac]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return False

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        messagebox.showerror("Error", "Correo inválido.")
        return False

    if not re.match(r"^\+?[\d\s\(\)-]{10,}$", telefono):
        messagebox.showerror("Error", "Teléfono inválido.")
        return False

    try:
        datetime.strptime(fecha_nac, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Error", "Fecha no válida. Usa formato DD/MM/AAAA.")
        return False

    return True

# ======= CRUD =======
def agregar_cliente():
    if not validar_campos():
        return
    nombre, correo, tel, direccion, fecha_nac = (
        entry_nombre.get(), entry_correo.get(), entry_telefono.get(), entry_direccion.get(), entry_fecha_nacimiento.get()
    )
    try:
        rfc = generar_rfc(nombre, fecha_nac)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    conn = conectar_db()
    if conn is None:
        return

    try:
        c = conn.cursor()
        c.execute("SELECT * FROM clientes WHERE rfc=?", (rfc,))
        if c.fetchone():
            messagebox.showwarning("Advertencia", "Cliente con el mismo RFC ya existe.")
            return

        c.execute("INSERT INTO clientes (nombre, email, tel, direccion, rfc, fecha_nac) VALUES (?, ?, ?, ?, ?, ?)",
                  (nombre, correo, tel, direccion, rfc, fecha_nac))
        conn.commit()

        tabla.insert('', 'end', values=(c.lastrowid, nombre, direccion, tel, correo, rfc, fecha_nac))
        messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        limpiar_campos()
    except sqlite3.Error as e:
        messagebox.showerror("Error BD", str(e))
    finally:
        conn.close()

def modificar_cliente():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar.")
        return

    cliente_id = tabla.item(seleccion, 'values')[0]
    nombre, correo, tel, direccion, fecha_nac = (
        entry_nombre.get(), entry_correo.get(), entry_telefono.get(), entry_direccion.get(), entry_fecha_nacimiento.get()
    )

    try:
        rfc = generar_rfc(nombre, fecha_nac)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    conn = conectar_db()
    if conn is None:
        return
    c = conn.cursor()
    c.execute("UPDATE clientes SET nombre=?, email=?, tel=?, direccion=?, rfc=?, fecha_nac=? WHERE id=?",
              (nombre, correo, tel, direccion, rfc, fecha_nac, cliente_id))
    conn.commit()
    conn.close()

    tabla.item(seleccion, values=(cliente_id, nombre, direccion, tel, correo, rfc, fecha_nac))
    messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
    limpiar_campos()

def eliminar_cliente():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un cliente.")
        return

    if not messagebox.askyesno("Confirmar", "¿Eliminar cliente seleccionado?"):
        return

    cliente_id = tabla.item(seleccion, 'values')[0]
    conn = conectar_db()
    if conn is None:
        return
    c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
    conn.commit()
    conn.close()

    tabla.delete(seleccion)
    messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
    limpiar_campos()

def seleccionar_cliente(event):
    seleccion = tabla.selection()
    if seleccion:
        item = seleccion[0]
        valores = tabla.item(item)['values']
        limpiar_campos()
        entry_nombre.insert(0, valores[1])
        entry_direccion.insert(0, valores[2])
        entry_telefono.insert(0, valores[3])
        entry_correo.insert(0, valores[4])
        entry_fecha_nacimiento.insert(0, valores[6].replace('-', '/'))

def regresar():
    ventana_crud_clientes.withdraw()
    ventana_crud_clientes.regresar.deiconify()

# ======= INTERFAZ =======
ventana_crud_clientes = tk.Tk()
ventana_crud_clientes.title("CRUD de Clientes")
ventana_crud_clientes.geometry("1100x600")
ventana_crud_clientes.config(bg=COLOR_FONDO)

# ======= TÍTULO =======
tk.Label(ventana_crud_clientes, text="👥 CRUD de Clientes", font=("Segoe UI", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

# ======= BOTÓN REGRESAR =======
tk.Button(
    ventana_crud_clientes, text="← Regresar", font=("Segoe UI", 11, "bold"),
    bg=COLOR_FONDO, fg=COLOR_TITULO, relief="flat", cursor="hand2", command=regresar
).place(x=20, y=20)

# ======= FORMULARIO =======
frame_formulario = tk.Frame(ventana_crud_clientes, bg=COLOR_CARD, relief="groove", bd=2)
frame_formulario.pack(padx=20, pady=10, fill="x")

def crear_campo(texto):
    frame = tk.Frame(frame_formulario, bg=COLOR_CARD)
    frame.pack(fill="x", pady=5)
    tk.Label(frame, text=texto, font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg="#444").pack(side="left", padx=10)
    entry = tk.Entry(frame, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDES)
    entry.pack(side="right", padx=10, ipadx=8, ipady=4, fill="x", expand=True)
    return entry

entry_nombre = crear_campo("Nombre Completo:")
entry_direccion = crear_campo("Dirección:")
entry_telefono = crear_campo("Teléfono:")
entry_correo = crear_campo("Correo Electrónico:")
entry_fecha_nacimiento = crear_campo("Fecha de Nacimiento (DD/MM/AAAA):")

# ======= BOTONES CRUD =======
frame_botones = tk.Frame(ventana_crud_clientes, bg=COLOR_FONDO)
frame_botones.pack(pady=10)

def crear_boton(texto, color, comando):
    boton = tk.Button(
        frame_botones, text=texto, font=("Segoe UI", 12, "bold"), bg=color, fg="white",
        relief="flat", width=13, height=1, cursor="hand2", command=comando, activebackground=color
    )
    boton.pack(side="left", padx=12)
    return boton

crear_boton("Agregar", COLOR_VERDE, agregar_cliente)
crear_boton("Modificar", COLOR_AMARILLO, modificar_cliente)
crear_boton("Eliminar", COLOR_ROJO, eliminar_cliente)

# ======= TABLA =======
frame_tabla = tk.Frame(ventana_crud_clientes, bg=COLOR_FONDO)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=15)

estilo = ttk.Style()
estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white")
estilo.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#007bff", foreground="white")

tabla = ttk.Treeview(
    frame_tabla,
    columns=("id", "nombre", "direccion", "telefono", "correo", "rfc", "fecha_nacimiento"),
    show="headings"
)

for col, texto in zip(
    ("id", "nombre", "direccion", "telefono", "correo", "rfc", "fecha_nacimiento"),
    ("ID", "Nombre", "Dirección", "Teléfono", "Correo", "RFC", "Fecha Nacimiento")
):
    tabla.heading(col, text=texto)
    tabla.column(col, anchor="center", stretch=True, width=150)

tabla.bind('<<TreeviewSelect>>', seleccionar_cliente)
tabla.grid(row=0, column=0, sticky="nsew")

scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll_y.set)
scroll_y.grid(row=0, column=1, sticky="ns")

frame_tabla.grid_rowconfigure(0, weight=1)
frame_tabla.grid_columnconfigure(0, weight=1)

ventana_crud_clientes.withdraw()
