import tkinter as tk
from tkinter import ttk
from ventanas.crud_productos import ventana_crud_productos, cargar_productos
from ventanas.crud_clientes import ventana_crud_clientes, cargar_clientes
from ventanas.crear_factura import ventana_crear_factura
from ventanas.ayuda import ventana_ayuda
from ventanas.informes import ventana_facturas

# ===== Colores base =====
COLOR_FONDO = "#e8eef1"
COLOR_BOTON = "#007bff"
COLOR_BOTON_HOVER = "#0056b3"
COLOR_TEXTO = "#ffffff"
COLOR_TITULO = "#333333"

# ===== Variable global para recordar si está en pantalla completa =====
pantalla_completa = False

# ======= FUNCIONES =======
def toggle_fullscreen(event=None):
    """Activa o desactiva pantalla completa."""
    global pantalla_completa
    pantalla_completa = not pantalla_completa
    ventana_facturacion.attributes("-fullscreen", pantalla_completa)

def exit_fullscreen(event=None):
    """Sale del modo pantalla completa."""
    global pantalla_completa
    pantalla_completa = False
    ventana_facturacion.attributes("-fullscreen", False)

# ======= FUNCIONES DE NAVEGACIÓN =======
def abrir_catalogos():
    ventana_facturacion.withdraw()
    ventana_catalogos.deiconify()
    ventana_catalogos.attributes("-fullscreen", pantalla_completa)

def abrir_crear_factura():
    ventana_facturacion.withdraw()
    ventana_crear_factura.deiconify()
    ventana_crear_factura.regresar = ventana_facturacion
    from ventanas.crear_factura import actualizar_datos_al_abrir
    actualizar_datos_al_abrir()
    ventana_crear_factura.attributes("-fullscreen", pantalla_completa)

def abrir_ayuda():
    ventana_facturacion.withdraw()
    ventana_ayuda.deiconify()
    ventana_ayuda.regresar = ventana_facturacion
    ventana_ayuda.attributes("-fullscreen", pantalla_completa)

def abrir_informes():
    ventana_facturacion.withdraw()
    ventana_facturas.deiconify()
    ventana_facturas.regresar = ventana_facturacion
    ventana_facturas.attributes("-fullscreen", pantalla_completa)

def regresar_menu():
    ventana_catalogos.withdraw()
    ventana_facturacion.deiconify()
    ventana_facturacion.attributes("-fullscreen", pantalla_completa)

def abrir_crud_productos():
    ventana_catalogos.withdraw()
    ventana_crud_productos.deiconify()
    ventana_crud_productos.regresar = ventana_catalogos
    cargar_productos()
    ventana_crud_productos.attributes("-fullscreen", pantalla_completa)

def abrir_crud_clientes():
    ventana_catalogos.withdraw()
    ventana_crud_clientes.deiconify()
    ventana_crud_clientes.regresar = ventana_catalogos
    cargar_clientes()
    ventana_crud_clientes.attributes("-fullscreen", pantalla_completa)

def regresar_catalogos():
    ventana_catalogos.deiconify()
    ventana_catalogos.attributes("-fullscreen", pantalla_completa)


# ======= FUNCIÓN PARA EFECTO HOVER =======
def hover_boton(boton, color_hover, color_base):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_base))


# ======= CONFIGURACIÓN DE VENTANA PRINCIPAL =======
ventana_facturacion = tk.Tk()
ventana_facturacion.title("Menú Principal - Facturación")
ventana_facturacion.geometry("700x500")
ventana_facturacion.config(bg=COLOR_FONDO)

# Soporte de pantalla completa
ventana_facturacion.bind("<F11>", toggle_fullscreen)
ventana_facturacion.bind("<Escape>", exit_fullscreen)

# ======= TÍTULO =======
titulo_facturacion = tk.Label(
    ventana_facturacion,
    text="📦 Menú de Facturación",
    font=("Segoe UI", 22, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TITULO
)
titulo_facturacion.pack(pady=30)

# ======= FRAME PRINCIPAL =======
frame_facturacion = tk.Frame(ventana_facturacion, bg=COLOR_FONDO)
frame_facturacion.pack(pady=20)

def crear_boton(texto, comando):
    boton = tk.Button(
        frame_facturacion,
        text=texto,
        font=("Segoe UI", 13, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_TEXTO,
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        relief="flat",
        width=15,
        height=2,
        command=comando,
        cursor="hand2"
    )
    boton.config(borderwidth=0)
    hover_boton(boton, COLOR_BOTON_HOVER, COLOR_BOTON)
    return boton

# ======= FILAS DE BOTONES =======
fila1 = tk.Frame(frame_facturacion, bg=COLOR_FONDO)
fila1.pack(pady=15)
crear_boton("📚 Catálogos", abrir_catalogos).pack(in_=fila1, side="left", padx=30)
crear_boton("🧾 Facturación", abrir_crear_factura).pack(in_=fila1, side="left", padx=30)

fila2 = tk.Frame(frame_facturacion, bg=COLOR_FONDO)
fila2.pack(pady=15)
crear_boton("📊 Informes", abrir_informes).pack(in_=fila2, side="left", padx=30)
crear_boton("❓ Ayuda", abrir_ayuda).pack(in_=fila2, side="left", padx=30)

# ======= PIE DE PÁGINA =======
tk.Label(
    ventana_facturacion,
    text="Presiona F11 para pantalla completa | ESC para salir",
    font=("Segoe UI", 10),
    bg=COLOR_FONDO,
    fg="#555"
).pack(side="bottom", pady=10)


# ======= VENTANA DE CATÁLOGOS =======
ventana_catalogos = tk.Toplevel(ventana_facturacion)
ventana_catalogos.title("Catálogos")
ventana_catalogos.geometry("700x500")
ventana_catalogos.config(bg=COLOR_FONDO)
ventana_catalogos.withdraw()

titulo_catalogos = tk.Label(
    ventana_catalogos,
    text="📂 Catálogos",
    font=("Segoe UI", 22, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TITULO
)
titulo_catalogos.pack(pady=30)

boton_regresar = tk.Button(
    ventana_catalogos,
    text="← Regresar",
    font=("Segoe UI", 11, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_BOTON,
    relief="flat",
    cursor="hand2",
    command=regresar_menu
)
boton_regresar.place(x=20, y=20)
hover_boton(boton_regresar, "#cfe3ff", COLOR_FONDO)

frame_catalogos = tk.Frame(ventana_catalogos, bg=COLOR_FONDO)
frame_catalogos.pack(pady=40)

def crear_boton_catalogo(texto, comando):
    boton = tk.Button(
        frame_catalogos,
        text=texto,
        font=("Segoe UI", 13, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_TEXTO,
        activebackground=COLOR_BOTON_HOVER,
        relief="flat",
        width=15,
        height=2,
        command=comando,
        cursor="hand2"
    )
    boton.config(borderwidth=0)
    hover_boton(boton, COLOR_BOTON_HOVER, COLOR_BOTON)
    return boton

fila1_catalogos = tk.Frame(frame_catalogos, bg=COLOR_FONDO)
fila1_catalogos.pack(pady=15)
crear_boton_catalogo("📦 Productos", abrir_crud_productos).pack(in_=fila1_catalogos, side="left", padx=40)
crear_boton_catalogo("👥 Clientes", abrir_crud_clientes).pack(in_=fila1_catalogos, side="left", padx=40)

# Ocultar al inicio
ventana_facturacion.withdraw()
