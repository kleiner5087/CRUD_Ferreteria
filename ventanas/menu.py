import tkinter as tk
from tkinter import ttk
from ventanas.crud_productos import crear_ventana_crud_productos, cargar_productos
from ventanas.crud_clientes import crear_ventana_crud_clientes, cargar_clientes
from ventanas.crear_factura import crear_ventana_factura
from ventanas.ayuda import crear_ventana_ayuda
from ventanas.informes import crear_ventana_informes
from ventanas._utils import crear_boton

# ===== Colores base =====
COLOR_FONDO = "#e8eef1"
COLOR_BOTON = "#007bff"
COLOR_BOTON_HOVER = "#0056b3"
COLOR_TEXTO = "#ffffff"
COLOR_TITULO = "#333333"

# Variables para almacenar las ventanas (inicialmente no existen)
ventana_menu = None
ventana_submenu_cruds = None

# ======= FUNCIONES DE NAVEGACIÓN =======
def abrir_catalogos(ventana_padre):
    global ventana_submenu_cruds
    ventana_padre.withdraw()
    if ventana_submenu_cruds is None or not ventana_submenu_cruds.winfo_exists():
        ventana_submenu_cruds = crear_ventana_submenu_cruds(ventana_padre)
    ventana_submenu_cruds.deiconify()

def abrir_crear_factura(ventana_padre):
    ventana_padre.withdraw()
    ventana = crear_ventana_factura(ventana_padre)
    ventana.deiconify()
    from ventanas.crear_factura import actualizar_datos_al_abrir # Esto podría necesitar refactorización
    actualizar_datos_al_abrir()

def abrir_ayuda(ventana_padre):
    ventana_padre.withdraw()
    ventana = crear_ventana_ayuda(ventana_padre)
    ventana.deiconify()

def abrir_informes(ventana_padre):
    ventana_padre.withdraw()
    ventana = crear_ventana_informes(ventana_padre)
    ventana.deiconify()

def regresar_a_ventana(ventana_actual, ventana_a_mostrar):
    ventana_actual.withdraw()
    ventana_a_mostrar.deiconify()

def abrir_crud_productos(ventana_padre):
    ventana_padre.withdraw()
    ventana = crear_ventana_crud_productos(ventana_padre)
    ventana.deiconify()
    cargar_productos(ventana)

def abrir_crud_clientes(ventana_padre):
    ventana_padre.withdraw()
    ventana = crear_ventana_crud_clientes(ventana_padre)
    ventana.deiconify()
    cargar_clientes(ventana)


# ======= FUNCIÓN PARA EFECTO HOVER =======
def hover_boton(boton, color_hover, color_base):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_base))


# ======= CONFIGURACIÓN DE VENTANA PRINCIPAL =======
def crear_ventana_menu(ventana_padre):
    global ventana_menu
    if ventana_menu is None or not ventana_menu.winfo_exists():
        ventana_menu = tk.Toplevel(ventana_padre)
        ventana_menu.title("Menú Principal - Facturación")
        ventana_menu.geometry("700x500")
        ventana_menu.config(bg=COLOR_FONDO)

        # ======= TÍTULO =======
        titulo_facturacion = tk.Label(
            ventana_menu,
            text="📦 Menú de Facturación",
            font=("Segoe UI", 22, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TITULO
        )
        titulo_facturacion.pack(pady=30)

        # ======= FRAME PRINCIPAL =======
        frame_facturacion = tk.Frame(ventana_menu, bg=COLOR_FONDO)
        frame_facturacion.pack(pady=20)

        # ======= FILAS DE BOTONES =======
        fila1 = tk.Frame(frame_facturacion, bg=COLOR_FONDO)
        fila1.pack(pady=15)
        crear_boton(fila1,"📚 CRUDS", COLOR_BOTON, lambda: abrir_catalogos(ventana_menu), width=15, padx=30, pady=2, color_hover=COLOR_BOTON_HOVER)
        crear_boton(fila1,"🧾 Facturación", COLOR_BOTON, lambda: abrir_crear_factura(ventana_menu), width=15, padx=30, pady=2, color_hover=COLOR_BOTON_HOVER)

        fila2 = tk.Frame(frame_facturacion, bg=COLOR_FONDO)
        fila2.pack(pady=15)
        crear_boton(fila2,"📊 Informes", COLOR_BOTON, lambda: abrir_informes(ventana_menu), width=15, padx=30, pady=2, color_hover=COLOR_BOTON_HOVER)
        crear_boton(fila2,"❓ Ayuda", COLOR_BOTON, lambda: abrir_ayuda(ventana_menu), width=15, padx=30, pady=2, color_hover=COLOR_BOTON_HOVER)

        # Ocultar al inicio
    return ventana_menu


# ======= VENTANA DE SELECCION DE CRUDS =======
def crear_ventana_submenu_cruds(ventana_padre):
    global ventana_submenu_cruds
    ventana_submenu_cruds = tk.Toplevel(ventana_padre)
    ventana_submenu_cruds.title("CRUDS - Registros")
    ventana_submenu_cruds.geometry("700x500")
    ventana_submenu_cruds.config(bg=COLOR_FONDO)
    
    titulo_catalogos = tk.Label(
        ventana_submenu_cruds,
        text="📂 CRUDS - Registros",
        font=("Segoe UI", 22, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TITULO
    )
    titulo_catalogos.pack(pady=30)

    boton_regresar = tk.Button(
        ventana_submenu_cruds,
        text="← Regresar",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_BOTON,
        relief="flat",
        cursor="hand2",
        command=lambda: regresar_a_ventana(ventana_submenu_cruds, ventana_padre)
    )
    boton_regresar.place(x=20, y=20)
    hover_boton(boton_regresar, "#cfe3ff", COLOR_FONDO)

    frame_catalogos = tk.Frame(ventana_submenu_cruds, bg=COLOR_FONDO)
    frame_catalogos.pack(pady=40)

    fila1_catalogos = tk.Frame(frame_catalogos, bg=COLOR_FONDO)
    fila1_catalogos.pack(pady=15)
    crear_boton(fila1_catalogos,"📦 Productos", COLOR_BOTON, lambda: abrir_crud_productos(ventana_submenu_cruds), width=15, padx=40, pady=2, color_hover=COLOR_BOTON_HOVER)
    crear_boton(fila1_catalogos,"👥 Clientes", COLOR_BOTON, lambda: abrir_crud_clientes(ventana_submenu_cruds), width=15, padx=40, pady=2, color_hover=COLOR_BOTON_HOVER)

    return ventana_submenu_cruds
