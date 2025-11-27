import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random, string, re
from clases.repository import get_all_clients, add_client, update_client, delete_client
from ventanas._utils import crear_campo, crear_boton, configurar_treeview_style

# ======= COLORES BASE =======
COLOR_FONDO = "#e8eef1"
COLOR_CARD = "#ffffff"
COLOR_BORDES = "#cfd3d7"
COLOR_TITULO = "#007bff"
COLOR_VERDE = "#28a745"
COLOR_AMARILLO = "#ffc107"
COLOR_ROJO = "#dc3545"

# ======= CONEXIÓN =======
def cargar_clientes(ventana=None):
    clientes = get_all_clients()
    # Si la ventana no se pasa, usa la global (para compatibilidad)
    tabla_a_usar = ventana.tabla if ventana and hasattr(ventana, 'tabla') else tabla
    tabla_a_usar.delete(*tabla_a_usar.get_children())
    tabla.delete(*tabla.get_children())
    if clientes:
        for c in clientes:
            # DB order: (id, nombre, email, tel, direccion, rfc, fecha_nac)
            # GUI order expected: (id, nombre, direccion, telefono, correo, rfc, fecha_nacimiento)
            id_, nombre, email, tel, direccion, rfc, fecha_nac = c
            tabla.insert('', 'end', values=(id_, nombre, direccion, tel, email, rfc, fecha_nac))
    else:
        messagebox.showinfo("Información", "No se encontraron clientes.")

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
    success, info = add_client(nombre, correo, tel, direccion, rfc, fecha_nac)
    if not success:
        if info == "exists":
            messagebox.showwarning("Advertencia", "Cliente con el mismo RFC ya existe.")
        else:
            messagebox.showerror("Error BD", str(info))
        return

    lastid = info
    tabla.insert('', 'end', values=(lastid, nombre, direccion, tel, correo, rfc, fecha_nac))
    messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
    limpiar_campos()

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
    ok = update_client(cliente_id, nombre, correo, tel, direccion, rfc, fecha_nac)
    if not ok:
        messagebox.showerror("Error", "No se pudo actualizar el cliente.")
        return

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
    ok = delete_client(cliente_id)
    if not ok:
        messagebox.showerror("Error", "No se pudo eliminar el cliente.")
        return

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

# ===== Variables Globales de la Ventana =====
ventana_crud_clientes = None
entry_nombre, entry_direccion, entry_telefono, entry_correo, entry_fecha_nacimiento, tabla = (None,) * 6

def crear_ventana_crud_clientes(ventana_padre):
    global ventana_crud_clientes, entry_nombre, entry_direccion, entry_telefono, entry_correo, entry_fecha_nacimiento, tabla
    if ventana_crud_clientes is None or not ventana_crud_clientes.winfo_exists():
        ventana_crud_clientes = tk.Toplevel(ventana_padre)
        ventana_crud_clientes.title("CRUD de Clientes")
        ventana_crud_clientes.geometry("1100x600")
        ventana_crud_clientes.config(bg=COLOR_FONDO)
        ventana_crud_clientes.regresar = ventana_padre

        tk.Label(ventana_crud_clientes, text="👥 CRUD de Clientes", font=("Segoe UI", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        tk.Button(
            ventana_crud_clientes, text="← Regresar", font=("Segoe UI", 11, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO, relief="flat", cursor="hand2", command=regresar
        ).place(x=20, y=20)

        frame_formulario = tk.Frame(ventana_crud_clientes, bg=COLOR_CARD, relief="groove", bd=2)
        frame_formulario.pack(padx=20, pady=10, fill="x")

        entry_nombre = crear_campo(frame_formulario, "Nombre Completo:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_direccion = crear_campo(frame_formulario, "Dirección:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_telefono = crear_campo(frame_formulario, "Teléfono:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_correo = crear_campo(frame_formulario, "Correo Electrónico:", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)
        entry_fecha_nacimiento = crear_campo(frame_formulario, "Fecha de Nacimiento (DD/MM/AAAA):", bg_card=COLOR_CARD, borde_color=COLOR_BORDES)

        frame_botones = tk.Frame(ventana_crud_clientes, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        crear_boton(frame_botones, "Agregar", COLOR_VERDE, agregar_cliente, width=12, padx=15, pady=10)
        crear_boton(frame_botones, "Modificar", COLOR_AMARILLO, modificar_cliente, width=12, padx=15, pady=10)
        crear_boton(frame_botones, "Eliminar", COLOR_ROJO, eliminar_cliente, width=12, padx=15, pady=10)

        frame_tabla = tk.Frame(ventana_crud_clientes, bg=COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=15)

        configurar_treeview_style(ventana_crud_clientes)

        tabla = ttk.Treeview(
            frame_tabla,
            columns=("id", "nombre", "direccion", "telefono", "correo", "rfc", "fecha_nacimiento"),
            show="headings"
        )
        ventana_crud_clientes.tabla = tabla

        for col, texto in zip(
            ("id", "nombre", "direccion", "telefono", "correo", "rfc", "fecha_nacimiento"),
            ("ID", "Nombre", "Dirección", "Teléfono", "Correo", "RFC", "Fecha Nacimiento")
        ):
            tabla.heading(col, text=texto)
            tabla.column(col, anchor="center", stretch=True)

        tabla.bind('<<TreeviewSelect>>', seleccionar_cliente)
        tabla.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        ventana_crud_clientes.withdraw()
    return ventana_crud_clientes
