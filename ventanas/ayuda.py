import tkinter as tk
from tkinter import *
from tkinter import ttk

ventana_ayuda = tk.Tk()
ventana_ayuda.title("Ayuda")
ventana_ayuda.geometry("900x910")
ventana_ayuda.resizable(True, True)

color_fondo = "#f0f0f0"
color_titulo = "#1A1A1A"
color_subtitulo = "#555555"
color_texto = "#333333"

frame_principal = tk.Frame(ventana_ayuda, bg=color_fondo)
frame_principal.pack(expand=True, fill='both')

frame_regreso = tk.Frame(frame_principal, bg=color_fondo)
frame_regreso.pack(fill='x', padx=20, pady=10)

frame_contenido = tk.Frame(frame_principal, bg=color_fondo)
frame_contenido.pack(expand=True, fill='both', padx=40, pady=20)

titulo_frame = tk.Frame(frame_contenido, bg=color_fondo)
titulo_frame.pack(fill='x', pady=(0, 20))

tk.Label(titulo_frame,
         text="Sistema de Facturación",
         font=("Roboto", 28, "bold"),
         fg=color_titulo,
         bg=color_fondo).pack()

tk.Canvas(titulo_frame, height=2, bg=color_titulo).pack(fill='x', pady=10)

info_frame = tk.Frame(frame_contenido, bg=color_fondo)
info_frame.pack(fill='x', pady=(0, 20))

tk.Label(info_frame,
         text="Desarrollado por:",
         font=("Roboto", 12),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=5)

tk.Label(info_frame,
         text="Jesús Adrian López Magaña | 222H17059",
         font=("Roboto", 12),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=5)

tk.Label(info_frame,
         text="Ángel Ariel Madrigal Ricardez | 222H17076",
         font=("Roboto", 12),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=5)

tk.Label(info_frame,
         text="Leonardo Santamaria Sánchez | 222H17123",
         font=("Roboto", 12),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=5)


tk.Label(info_frame,
         text="Materia: Laboratorio De Diseño De Software",
         font=("Roboto", 12),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=5)

tk.Label(info_frame,
         text="Docente: Rafael Mena de la Rosa",
         font=("Roboto", 12),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=5)

desc_frame = tk.Frame(frame_contenido, bg=color_fondo)
desc_frame.pack(fill='both', expand=True)

tk.Label(desc_frame,
         text="Descripción del Sistema",
         font=("Roboto", 14, "bold"),
         fg=color_subtitulo,
         bg=color_fondo).pack(pady=(20, 10))

texto_introduccion = """
Este sistema está diseñado para gestionar una tienda de pinturas de manera eficiente, conectándose a una base de datos Sqlite.

El sistema cuenta con los siguientes módulos principales:

1. Ventana de Entrada:
   • Login: Verificación de credenciales (email y contraseña)
   • Registro: Captura de datos personales para nuevos usuarios
   • Recuperación de contraseña: Sistema de recuperación vía email

2. Menú Principal:
   • Catálogo:
     - Productos: Gestión completa de productos (agregar, modificar, eliminar)
     - Clientes: Administración de datos de clientes
   • Facturación:
     - Selección de cliente y productos mediante combobox
     - Opciones para guardar e imprimir PDF
   • Informes:
     - Visualización de historial de facturas
     - Funciones de apertura e impresión de facturas
   • Ayuda:
     - Documentación y guía de uso del sistema
"""

text_widget = tk.Text(desc_frame,
                      wrap=tk.WORD,
                      font=("Roboto", 12),
                      bg=color_fondo,
                      fg=color_texto,
                      height=20,
                      borderwidth=0)
text_widget.pack(fill='both', expand=True, pady=10)
text_widget.insert('1.0', texto_introduccion)
text_widget.config(state='disabled')

def regresar():
    
    ventana_ayuda.withdraw()
    ventana_ayuda.regresar.deiconify()

# Botón para regresar a la ventana de facturación
boton_regresar_ayuda = tk.Button(ventana_ayuda, text="←", font=("Arial", 12), bg="#f0f0f0", fg="#007bff", relief="flat", command=regresar)
boton_regresar_ayuda.place(x=100, y=5)  # Ajusta la posición del botón un poco a la derecha


ventana_ayuda.withdraw()
