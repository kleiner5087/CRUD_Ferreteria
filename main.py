import tkinter as tk
from tkinter import ttk, messagebox
from clases.usuario import Usuario
from ventanas.facturacion import ventana_facturacion

# ===== Colores y estilo =====
COLOR_FONDO = "#e8eef1"
COLOR_FRAME = "#ffffff"
COLOR_PRINCIPAL = "#4caf50"
COLOR_SECUNDARIO = "#2196f3"
COLOR_ALERTA = "#ff5722"

# Variable global para recordar si estaba en pantalla completa
pantalla_completa = False


def crear_ventana_inicio():
    """Crea la ventana principal de inicio de sesión"""
    global pantalla_completa
    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")
    ventana.geometry("500x480")
    ventana.config(bg=COLOR_FONDO)

    # Si estaba en pantalla completa, mantenerlo
    ventana.attributes("-fullscreen", pantalla_completa)

    # ===== Evento: detectar F11 y Escape =====
    def toggle_fullscreen(event=None):
        global pantalla_completa
        pantalla_completa = not pantalla_completa
        ventana.attributes("-fullscreen", pantalla_completa)

    def exit_fullscreen(event=None):
        global pantalla_completa
        pantalla_completa = False
        ventana.attributes("-fullscreen", False)

    ventana.bind("<F11>", toggle_fullscreen)
    ventana.bind("<Escape>", exit_fullscreen)

    # ===== Estilos TTK =====
    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 11), padding=6)
    style.configure("TLabel", background=COLOR_FRAME)

    # ===== Título =====
    tk.Label(
        ventana, text="💻 Iniciar Sesión",
        font=("Segoe UI", 22, "bold"), bg=COLOR_FONDO, fg="#333"
    ).pack(pady=20)

    # ===== Frame principal =====
    frame = tk.Frame(ventana, bg=COLOR_FRAME, padx=30, pady=30, relief="raised", bd=3)
    frame.pack(pady=10)

    ttk.Label(frame, text="Usuario:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=10)
    entry_usuario = ttk.Entry(frame, font=("Segoe UI", 12), width=25)
    entry_usuario.grid(row=0, column=1, pady=10)

    ttk.Label(frame, text="Contraseña:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=10)
    entry_contrasena = ttk.Entry(frame, font=("Segoe UI", 12), show="*", width=25)
    entry_contrasena.grid(row=1, column=1, pady=10)

    def iniciar_sesion():
        usuario = entry_usuario.get()
        contraseña = entry_contrasena.get()
        usuario_obj = Usuario(usuario=usuario, contraseña=contraseña)

        if usuario_obj.valida_usuario_contraseña():
            ventana.destroy()
            ventana_facturacion.deiconify()
        elif not (usuario and contraseña):
            messagebox.showwarning("Error", "Debes ingresar un usuario y una contraseña.")
        else:
            messagebox.showwarning("Error", "Usuario o contraseña incorrectos.")

    ttk.Button(frame, text="Iniciar Sesión", command=iniciar_sesion).grid(row=2, column=0, columnspan=2, pady=15, sticky="nsew")

    # ===== Botones secundarios =====
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(pady=15)

    ttk.Button(frame_botones, text="Registrarse", command=lambda: abrir_registro(ventana)).grid(row=0, column=0, padx=10)
    ttk.Button(frame_botones, text="Recuperar Contraseña", command=lambda: abrir_recuperacion(ventana)).grid(row=0, column=1, padx=10)

    ventana.mainloop()


# ===== Ventana de registro =====
def abrir_registro(ventana_anterior):
    global pantalla_completa
    ventana_anterior.destroy()

    ventana_registro = tk.Tk()
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("400x480")
    ventana_registro.config(bg=COLOR_FONDO)

    # Mantener pantalla completa si estaba activa
    ventana_registro.attributes("-fullscreen", pantalla_completa)

    def toggle_fullscreen(event=None):
        global pantalla_completa
        pantalla_completa = not pantalla_completa
        ventana_registro.attributes("-fullscreen", pantalla_completa)

    def exit_fullscreen(event=None):
        global pantalla_completa
        pantalla_completa = False
        ventana_registro.attributes("-fullscreen", False)

    ventana_registro.bind("<F11>", toggle_fullscreen)
    ventana_registro.bind("<Escape>", exit_fullscreen)

    frame = tk.Frame(ventana_registro, bg=COLOR_FRAME, padx=20, pady=20, relief="raised", bd=3)
    frame.pack(pady=20)

    ttk.Label(frame, text="👤 Registro de Usuario", font=("Segoe UI", 16, "bold")).pack(pady=10)

    ttk.Label(frame, text="Usuario:", font=("Segoe UI", 11)).pack(pady=5, anchor="w")
    entry_usuario = ttk.Entry(frame, font=("Segoe UI", 11))
    entry_usuario.pack(fill="x", pady=5)

    ttk.Label(frame, text="Contraseña:", font=("Segoe UI", 11)).pack(pady=5, anchor="w")
    entry_contra = ttk.Entry(frame, font=("Segoe UI", 11), show="*")
    entry_contra.pack(fill="x", pady=5)

    ttk.Label(frame, text="Confirmar Contraseña:", font=("Segoe UI", 11)).pack(pady=5, anchor="w")
    entry_confirma = ttk.Entry(frame, font=("Segoe UI", 11), show="*")
    entry_confirma.pack(fill="x", pady=5)

    ttk.Label(frame, text="Email:", font=("Segoe UI", 11)).pack(pady=5, anchor="w")
    entry_email = ttk.Entry(frame, font=("Segoe UI", 11))
    entry_email.pack(fill="x", pady=5)

    ttk.Label(frame, text="Teléfono:", font=("Segoe UI", 11)).pack(pady=5, anchor="w")
    entry_tel = ttk.Entry(frame, font=("Segoe UI", 11))
    entry_tel.pack(fill="x", pady=5)

    def guardar_usuario():
        usuario = entry_usuario.get()
        contra = entry_contra.get()
        confirma = entry_confirma.get()
        email = entry_email.get()
        tel = entry_tel.get()

        if not all([usuario, contra, confirma, email, tel]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return
        if contra != confirma:
            messagebox.showwarning("Error", "Las contraseñas no coinciden.")
            return

        nuevo = Usuario(usuario=usuario, contraseña=contra, email=email, tel=tel)
        nuevo.crear()
        messagebox.showinfo("Registro", "Usuario registrado correctamente.")
        ventana_registro.destroy()
        crear_ventana_inicio()

    ttk.Button(frame, text="Registrar", command=guardar_usuario).pack(pady=15)
    ttk.Button(frame, text="← Regresar", command=lambda: [ventana_registro.destroy(), crear_ventana_inicio()]).pack(pady=5)

    ventana_registro.mainloop()


# ===== Ventana de recuperación =====
def abrir_recuperacion(ventana_anterior):
    global pantalla_completa
    ventana_anterior.destroy()

    ventana_recuperar = tk.Tk()
    ventana_recuperar.title("Recuperar Contraseña")
    ventana_recuperar.geometry("400x250")
    ventana_recuperar.config(bg=COLOR_FONDO)

    # Mantener pantalla completa si estaba activa
    ventana_recuperar.attributes("-fullscreen", pantalla_completa)

    def toggle_fullscreen(event=None):
        global pantalla_completa
        pantalla_completa = not pantalla_completa
        ventana_recuperar.attributes("-fullscreen", pantalla_completa)

    def exit_fullscreen(event=None):
        global pantalla_completa
        pantalla_completa = False
        ventana_recuperar.attributes("-fullscreen", False)

    ventana_recuperar.bind("<F11>", toggle_fullscreen)
    ventana_recuperar.bind("<Escape>", exit_fullscreen)

    frame = tk.Frame(ventana_recuperar, bg=COLOR_FRAME, padx=20, pady=20, relief="raised", bd=3)
    frame.pack(pady=30)

    ttk.Label(frame, text="🔐 Recuperar Contraseña", font=("Segoe UI", 16, "bold")).pack(pady=10)
    ttk.Label(frame, text="Ingresa tu correo electrónico", font=("Segoe UI", 11)).pack(pady=5)
    entry_email = ttk.Entry(frame, font=("Segoe UI", 11), width=30)
    entry_email.pack(pady=10)

    def enviar_recuperacion():
        email = entry_email.get()
        if email:
            usuario = Usuario(email=email)
            usuario.enviar_correo_recuperacion()
            messagebox.showinfo("Recuperación", f"Se enviaron los datos al correo {email}.")
            ventana_recuperar.destroy()
            crear_ventana_inicio()
        else:
            messagebox.showwarning("Error", "Por favor, ingresa un correo electrónico.")

    ttk.Button(frame, text="Enviar", command=enviar_recuperacion).pack(pady=10)
    ttk.Button(frame, text="← Regresar", command=lambda: [ventana_recuperar.destroy(), crear_ventana_inicio()]).pack(pady=5)

    ventana_recuperar.mainloop()


# ===== Iniciar programa =====
if __name__ == "__main__":
    crear_ventana_inicio()
