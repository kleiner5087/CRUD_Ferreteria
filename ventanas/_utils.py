import tkinter as tk
from tkinter import ttk

def crear_campo(parent, texto, bg_card="#ffffff", borde_color="#d0d4d9"):
    """Crea un campo de formulario (label + entry) dentro de `parent` y devuelve el Entry."""
    frame = tk.Frame(parent, bg=bg_card)
    frame.pack(fill="x", pady=5)
    tk.Label(frame, text=texto, font=("Segoe UI", 11, "bold"), bg=bg_card, fg="#444").pack(side="left", padx=10)
    entry = tk.Entry(frame, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=borde_color)
    entry.pack(side="right", padx=10, ipadx=8, ipady=4, fill="x", expand=True)
    return entry

def hover_boton(boton, color_hover, color_base):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_base))

def crear_boton(parent, texto, color, comando, width, padx, pady, color_hover = None):
    boton = tk.Button(
        parent, text=texto, font=("Segoe UI", 13, "bold"), bg=color, fg="white",
        relief="flat", width=width, height=2, cursor="hand2", command=comando
    )
    boton.config(borderwidth=0)
    hover_boton(boton, color_hover=color_hover if color_hover else color, color_base=color)
    boton.pack(side="left", padx=padx, pady=pady)
    return boton
 
def configurar_treeview_style(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")  # Usar un tema que permita personalización completa
    estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white")
    estilo.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#ffbb88")
