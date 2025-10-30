import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import webbrowser
import platform
import subprocess

# Ruta donde se almacenan las facturas
CARPETA_FACTURAS = "./facturas"

def actualizar_lista(lista_archivos):
    # Limpiar el Listbox
    lista_archivos.delete(0, tk.END)

    # Obtener archivos PDF de la carpeta
    if os.path.exists(CARPETA_FACTURAS):
        archivos_pdf = [f for f in os.listdir(CARPETA_FACTURAS) if f.endswith(".pdf")]
        for archivo in archivos_pdf:
            lista_archivos.insert(tk.END, archivo)
    else:
        messagebox.showwarning("Advertencia", f"No se encontró la carpeta: {CARPETA_FACTURAS}")

def abrir_archivo(lista_archivos):
    try:
        archivo_seleccionado = lista_archivos.get(lista_archivos.curselection())
        ruta_completa = os.path.join(CARPETA_FACTURAS, archivo_seleccionado)
        webbrowser.open(ruta_completa)  # Abrir en el visor de PDF predeterminado
    except tk.TclError:
        messagebox.showwarning("Advertencia", "Debe seleccionar un archivo para abrirlo.")

def guardar_archivo(lista_archivos):
    try:
        archivo_seleccionado = lista_archivos.get(lista_archivos.curselection())  # Obtener el archivo seleccionado
        ruta_completa = os.path.join(CARPETA_FACTURAS, archivo_seleccionado)  # Ruta completa del archivo

        # Comprobar si el archivo existe
        if not os.path.exists(ruta_completa):
            messagebox.showwarning("Advertencia", "El archivo no existe.")
            return

        # Abrir un cuadro de diálogo para que el usuario seleccione la carpeta de destino
        carpeta_destino = filedialog.askdirectory(title="Seleccionar Carpeta de Destino")

        # Si el usuario seleccionó una carpeta
        if carpeta_destino:
            # Copiar el archivo a la carpeta seleccionada (manteniendo el mismo nombre)
            archivo_destino = os.path.join(carpeta_destino, archivo_seleccionado)  # Ruta destino
            shutil.copy(ruta_completa, archivo_destino)  # Copiar el archivo

            # Notificación de éxito
            messagebox.showinfo("Éxito", f"El archivo {archivo_seleccionado} ha sido guardado en: {carpeta_destino}")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

    except tk.TclError:
        messagebox.showwarning("Advertencia", "Debe seleccionar un archivo para guardar.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Crear la ventana para la gestión de facturas
ventana_facturas = tk.Tk()  # Se utiliza tk.Tk() en lugar de Toplevel para que la ventana sea principal
ventana_facturas.title("Gestión de Facturas")
ventana_facturas.geometry("400x300")

# Listbox para mostrar los archivos
tk.Label(ventana_facturas, text="Archivos de Facturas", font=("Arial", 12, "bold")).pack(pady=5)
lista_archivos = tk.Listbox(ventana_facturas, height=12, selectmode=tk.SINGLE)
lista_archivos.pack(fill="both", expand=True, padx=10, pady=5)

# Botones
frame_botones = tk.Frame(ventana_facturas)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Actualizar Lista", command=lambda: actualizar_lista(lista_archivos)).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Abrir Archivo", command=lambda: abrir_archivo(lista_archivos)).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Guardar Archivo", command=lambda: guardar_archivo(lista_archivos)).grid(row=0, column=2, padx=5)

# Actualizar lista al abrir la ventana
actualizar_lista(lista_archivos)

def regresar():
    ventana_facturas.withdraw()
    ventana_facturas.regresar.deiconify()

# Botón para regresar a la ventana de facturación
boton_ventana_facturas = tk.Button(ventana_facturas, text="←", font=("Arial", 12), bg="#f0f0f0", fg="#007bff", relief="flat", command=regresar)
boton_ventana_facturas.place(x=300, y=5)  
ventana_facturas.withdraw()
