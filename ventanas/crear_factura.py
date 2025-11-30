import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from clases.usuario import Usuario
from clases.productos import Producto
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from os import listdir
import os 
from os.path import isfile, join
from datetime import datetime

productos_seleccionados = []
usuarios = []

def numero_a_letras(numero):
   
    unidades = ["", "un", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
    decenas = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    centenas = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]
    
    def convertir_hasta_mil(n):
        if n == 0:
            return ""
        
        if n == 100:
            return "cien"
        
        if n < 10:
            return unidades[n]
        
        if n < 20:
            especiales = {
                10: "diez", 11: "once", 12: "doce", 13: "trece", 14: "catorce", 
                15: "quince", 16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve"
            }
            return especiales.get(n, f"dieci{unidades[n-10]}")
        
        if n < 100:
            u = n % 10
            d = n // 10
            if u == 0:
                return decenas[d]
            if d == 2:
                return f"veinti{unidades[u]}"
            return f"{decenas[d]} y {unidades[u]}"
        
        c = n // 100
        resto = n % 100
        if resto == 0:
            return centenas[c]
        
        return f"{centenas[c]} {convertir_hasta_mil(resto)}"
    
    # Separar parte entera y decimal
    partes = str('{:.2f}'.format(abs(numero))).split('.')
    parte_entera = int(partes[0])
    parte_decimal = int(partes[1])
    
    # Manejar millones
    millones = parte_entera // 1000000
    miles = (parte_entera % 1000000) // 1000
    centenas_n = parte_entera % 1000
    
    resultado = []
    if millones > 0:
        if millones == 1:
            resultado.append("un millón")
        else:
            resultado.append(f"{convertir_hasta_mil(millones)} millones")
    
    if miles > 0:
        if miles == 1:
            resultado.append("mil")
        else:
            resultado.append(f"{convertir_hasta_mil(miles)} mil")
    
    if centenas_n > 0 or not resultado:
        resultado.append(convertir_hasta_mil(centenas_n))
    
    # Manejar caso de número cero
    if not resultado:
        resultado.append("cero")
    
    # Agregar pesos y centavos
    texto = " ".join(resultado).strip()
    
    # Manejar "peso" o "pesos" según la parte entera
    if parte_entera == 1:
        texto += f" peso {parte_decimal:02d}/100 M.N."
    else:
        texto += f" pesos {parte_decimal:02d}/100 M.N."
    
    return texto.capitalize()


def generar_pdf_factura(cliente, productos, subtotal, iva, total):
    # Obtener el número de factura basado en la cantidad de archivos en la carpeta "facturas"
    carpeta_facturas = "facturas"
    archivos_existentes = [f for f in listdir(carpeta_facturas) if isfile(join(carpeta_facturas, f))]
    numero_factura = len(archivos_existentes) + 1
    folio = f"f{numero_factura:03}"

    # Crear el nombre del archivo
    archivo_pdf = f"{carpeta_facturas}/Factura_{folio}.pdf"
    
    # Crear un nuevo documento PDF
    c = canvas.Canvas(archivo_pdf, pagesize=letter)
    ancho, alto = letter

    # Información de la empresa
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, alto - 50, "Proveedora de materiales de construcción SA de CV.")
    c.setFont("Helvetica", 10)
    c.drawString(ancho - 200, alto - 50, f"Factura No. {folio}")
    c.drawString(ancho - 200, alto - 70, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

    # Información del cliente
    c.drawString(30, alto - 100, f"Cliente: {cliente['nombre']}")
    c.drawString(30, alto - 120, f"Dir.: {cliente['direccion']}")
    c.drawString(30, alto - 140, f"Tel.: {cliente['telefono']}")
    c.drawString(30, alto - 160, f"RFC: {cliente['rfc']}")

    # Encabezados de tabla
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, alto - 200, "No.")
    c.drawString(80, alto - 200, "Producto")
    c.drawString(250, alto - 200, "Cantidad")
    c.drawString(320, alto - 200, "Precio Unit")
    c.drawString(400, alto - 200, "Importe")

    # Línea divisoria
    c.line(30, alto - 205, ancho - 30, alto - 205)

    # Agregar los productos
    c.setFont("Helvetica", 10)
    y_pos = alto - 220
    print(productos)
    for idx, producto in enumerate(productos, start=1):
        importe = float(producto["precio"]) * float(producto["cantidad"])
        c.drawString(30, y_pos, str(idx))
        c.drawString(80, y_pos, producto["nombre"])
        c.drawString(250, y_pos, str(producto["cantidad"]))
        c.drawString(320, y_pos, f"${float(producto['precio']):.2f}")
        c.drawString(400, y_pos, f"${importe:.2f}")
        y_pos -= 20

    # Línea divisoria final
    c.line(30, y_pos, ancho - 30, y_pos)
    y_pos -= 20

    # Totales
    c.setFont("Helvetica-Bold", 10)
    c.drawString(300, y_pos, "Subtotal")
    c.drawString(400, y_pos, f"${subtotal:.2f}")
    y_pos -= 20
    c.drawString(300, y_pos, "IVA")
    c.drawString(400, y_pos, f"${iva:.2f}")
    y_pos -= 20
    c.drawString(300, y_pos, "Total")
    c.drawString(400, y_pos, f"${total:.2f}")

    # Agregar totales en letras
    c.setFont("Helvetica-Bold", 10)
    y_pos -= 50
    c.drawString(30, y_pos, f"Total en letras: {numero_a_letras(total)}")

    # Guardar el archivo PDF
    c.save()
    print(f"Factura generada: {archivo_pdf}")

def generar_factura():
    if not usuario_seleccionado:
        messagebox.showwarning("Advertencia", "Debe seleccionar un usuario.")
        return
    if not productos_seleccionados:
        messagebox.showwarning("Advertencia", "Debe seleccionar al menos un producto.")
        return
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    # Obtener el número de factura basado en la cantidad de archivos en la carpeta "facturas"
    carpeta_facturas = "facturas"
    archivos_existentes = [f for f in listdir(carpeta_facturas) if isfile(join(carpeta_facturas, f))]
    numero_factura = len(archivos_existentes) + 1
    folio = f"F{numero_factura:03}"  # Formato de folio como f001, f002, etc.

    # Calcular subtotal, IVA y total
    subtotal = sum([float(p["precio"]) * int(p["cantidad"]) for p in productos_seleccionados])
    iva = subtotal * 0.16
    total = subtotal + iva

    # Generar PDF de la factura
    generar_pdf_factura(usuario_seleccionado, productos_seleccionados, subtotal, iva, total)
    
    # ACTUALIZAR INVENTARIO AUTOMÁTICAMENTE
    producto_obj = Producto()
    for producto in productos_seleccionados:
        producto_obj.actualizar_existencia(producto["id"], producto["cantidad"])
    
    # Mostrar mensaje de éxito
    messagebox.showinfo("Factura Generada", f"La factura {folio} se generó exitosamente.")


# Función para actualizar datos de usuario y productos en los combobox
def actualizar_comboboxes(usuarios, productos):
    combo_usuarios['values'] = [f"{u['rfc']} - {u['nombre']}" for u in usuarios]
    combo_productos['values'] = [f"{p['nombre']} (ID: {p['id']})" for p in productos]

_after_id_cliente = None
def actualizar_clientes_autocompletar(event):
    """Filtra la lista de clientes en el combobox mientras el usuario escribe."""
    global _after_id_cliente
    # Si ya hay un temporizador, lo cancelamos
    if _after_id_cliente:
        combo_usuarios.after_cancel(_after_id_cliente)

    # Creamos un nuevo temporizador que llamará a la función de búsqueda después de 300ms
    _after_id_cliente = combo_usuarios.after(1000, lambda: realizar_busqueda_cliente(event))

def realizar_busqueda_cliente(event):
    """Realiza la búsqueda real y actualiza el combobox de clientes."""
    texto_busqueda = combo_usuarios.get()
    if texto_busqueda:
        clientes_filtrados = Usuario.buscar_clientes_por_rfc(texto_busqueda)
        nuevos_valores = [f"{u['rfc']} - {u['nombre']}" for u in clientes_filtrados]
        combo_usuarios['values'] = nuevos_valores
    else:
        nuevos_valores = [f"{u['rfc']} - {u['nombre']}" for u in usuarios]
        combo_usuarios['values'] = nuevos_valores

    # Desplegar la lista si hay texto y resultados
    if texto_busqueda and nuevos_valores:
        combo_usuarios.event_generate('<Down>')

_after_id_producto = None
def actualizar_productos_autocompletar(event):
    """Filtra la lista de productos en el combobox mientras el usuario escribe."""
    global _after_id_producto
    if _after_id_producto:
        combo_productos.after_cancel(_after_id_producto)
    
    _after_id_producto = combo_productos.after(1000, lambda: realizar_busqueda_producto(event))

def realizar_busqueda_producto(event):
    """Realiza la búsqueda real y actualiza el combobox de productos."""
    texto_busqueda = combo_productos.get()
    producto_obj = Producto()
    if texto_busqueda:
        productos_filtrados = producto_obj.buscar_productos_por_nombre(texto_busqueda)
        nuevos_valores = [f"{p['nombre']} (ID: {p['id']})" for p in productos_filtrados]
        combo_productos['values'] = nuevos_valores
    else:
        nuevos_valores = [f"{p['nombre']} (ID: {p['id']})" for p in productos]
        combo_productos['values'] = nuevos_valores
    
    if texto_busqueda and nuevos_valores:
        combo_productos.event_generate('<Down>')
        
# Función para seleccionar usuario desde el combobox
def seleccionar_usuario(event):
    global usuario_seleccionado
    seleccionado = combo_usuarios.get()
    if seleccionado:
        usuario_id = seleccionado.split(" - ")[0]
        usuario_seleccionado = next((u for u in usuarios if u["id"] == usuario_id), None)
        if not usuario_seleccionado: # Si no lo encuentra por ID, lo busca por RFC
            usuario_rfc = seleccionado.split(" - ")[0]
            usuario_seleccionado = next((u for u in usuarios if u["rfc"] == usuario_rfc), None)
        if usuario_seleccionado:    
            mostrar_datos_usuario(usuario_seleccionado)

# Función para seleccionar producto desde el combobox y agregarlo a la lista
def seleccionar_producto():
    cantidad = entry_cantidad_producto.get()

    # Si la cantidad está vacía, se establece un valor por defecto de 1
    if cantidad == "":
        cantidad = 1
    else:
        try:
            cantidad = int(cantidad)
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")
            return

    seleccionado = combo_productos.get()
    
    if seleccionado:
        # Extraemos el ID del producto
        producto_id = seleccionado.split(" (ID: ")[1].replace(")", "")

        # Buscamos el producto en la lista de productos disponibles
        producto = next((p for p in productos if p["id"] == producto_id), None)
        
        if producto and not any(p["id"] == producto_id for p in productos_seleccionados):
            # Agregar producto a la lista de seleccionados
            productos_seleccionados.append({**producto, "cantidad": cantidad})
            
            # Actualizamos la vista de productos seleccionados
            mostrar_productos_seleccionados()
            
            # Limpiar la cantidad para nuevo producto
            entry_cantidad_producto.delete(0, tk.END)        
            

# Funciones para mostrar datos y productos seleccionados (sin cambios)
def mostrar_datos_usuario(usuario):
    # Actualizamos cada Entry con el valor del campo correspondiente
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, usuario['id'])
    entry_id.config(state="readonly")

    entry_nombre.config(state="normal")
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, usuario['nombre'])
    entry_nombre.config(state="readonly")

    entry_direccion.config(state="normal")
    entry_direccion.delete(0, tk.END)
    entry_direccion.insert(0, usuario['direccion'])
    entry_direccion.config(state="readonly")

    entry_telefono.config(state="normal")
    entry_telefono.delete(0, tk.END)
    entry_telefono.insert(0, usuario['telefono'])
    entry_telefono.config(state="readonly")

    entry_rfc.config(state="normal")
    entry_rfc.delete(0, tk.END)
    entry_rfc.insert(0, usuario['rfc'])
    entry_rfc.config(state="readonly")

    entry_email.config(state="normal")
    entry_email.delete(0, tk.END)
    entry_email.insert(0, usuario['email'])
    entry_email.config(state="readonly")
    
def obtener_numero_factura():
    carpeta_facturas = "facturas"
    
    # Obtener los archivos existentes en la carpeta de facturas
    archivos_existentes = [f for f in os.listdir(carpeta_facturas) if os.path.isfile(os.path.join(carpeta_facturas, f))]
    
    # Calcular el número de factura basado en la cantidad de archivos existentes
    numero_factura = len(archivos_existentes) + 1
    
    # Formatear el número de factura con tres dígitos
    return f"F{numero_factura:03}"

# Función para actualizar el número de factura en el Label
def actualizar_numero_factura(frame_fecha_factura):
    folio = obtener_numero_factura()

    # Si ya existe el Label con el número de factura, solo actualizamos el texto
    if hasattr(frame_fecha_factura, 'factura_label'):
        frame_fecha_factura.factura_label.config(text=f"No. Factura: {folio}", bg="#f0f0f0")
    else:
        # Si no existe, lo creamos
        frame_fecha_factura.factura_label = tk.Label(frame_fecha_factura, text=f"No. Factura: {folio}", font=("Arial", 14, "bold"), bg="#f0f0f0")
        frame_fecha_factura.factura_label.grid(row=0, column=1, padx=10, pady=5)       

def limpiar_datos():
    global productos_seleccionados
    productos_seleccionados = []  # Limpiar la lista de productos seleccionados
    
    # Limpiar las entradas de texto
    entry_subtotal.delete(0, tk.END)
    entry_iva.delete(0, tk.END)
    entry_total.delete(0, tk.END)
    entry_total_letras.delete(0, tk.END)

def mostrar_productos_seleccionados():
    tree_seleccionados.delete(*tree_seleccionados.get_children())  # Limpiar los productos seleccionados previos
    
    if not productos_seleccionados:  # Verificar si hay productos seleccionados
        return  # Si no hay productos, no hacer nada más
    
    subtotal = 0  # Inicializar el subtotal

    for producto in productos_seleccionados:
        # Insertar los productos en el Treeview
        tree_seleccionados.insert("", "end", values=(producto["id"], producto["nombre"], producto["precio"], producto["cantidad"]))
        subtotal += producto["precio"] * producto["cantidad"]  # Calcular subtotal

    # Calcular IVA y total
    iva = subtotal * 0.16
    total = subtotal + iva

    # Actualizar los campos de totales
    entry_subtotal.delete(0, tk.END)
    entry_subtotal.insert(0, f"${subtotal:.2f}")
    
    entry_iva.delete(0, tk.END)
    entry_iva.insert(0, f"${iva:.2f}")
    
    entry_total.delete(0, tk.END)
    entry_total.insert(0, f"${total:.2f}")

    entry_total_letras.delete(0, tk.END)
    entry_total_letras.insert(0, numero_a_letras(total))  # Función para convertir el total a letras


ventana_crear_factura = None

def crear_ventana_factura(ventana_padre):
    global ventana_crear_factura, combo_usuarios, combo_productos, entry_cantidad_producto, tree_seleccionados
    global entry_id, entry_nombre, entry_direccion, entry_telefono, entry_rfc, entry_email
    global entry_subtotal, entry_iva, entry_total, entry_total_letras, frame_fecha_factura

    if ventana_crear_factura is None or not ventana_crear_factura.winfo_exists():
        ventana_crear_factura = tk.Toplevel(ventana_padre)
        ventana_crear_factura.title("Facturación")
        ventana_crear_factura.geometry("1550x650")
        ventana_crear_factura.config(bg="#f0f0f0")
        ventana_crear_factura.regresar = ventana_padre

        # Frame izquierdo: Selección de usuario
        frame_izquierda = tk.Frame(ventana_crear_factura, width=600, bg="#f0f0f0", bd=1, relief="solid")
        frame_izquierda.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame_izquierda, text="Información del Cliente", font=("Arial", 14, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        tk.Label(frame_izquierda, text="Buscar Cliente (RFC):", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=5, padx=10, sticky="w")
        combo_usuarios = ttk.Combobox(frame_izquierda, width=35, style="TCombobox", background="#f0f0f0")
        combo_usuarios.grid(row=1, column=1, pady=5, padx=10)
        combo_usuarios.bind("<<ComboboxSelected>>", seleccionar_usuario)
        combo_usuarios.bind("<KeyRelease>", actualizar_clientes_autocompletar)

        etiquetas = ["ID", "Nombre", "Dirección", "Teléfono", "RFC", "Email"]
        entradas = []

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(frame_izquierda, text=etiqueta + ":", bg="#f0f0f0", font=("Arial", 12)).grid(row=i+2, column=0, padx=5, pady=20, sticky="w")
            entrada = tk.Entry(frame_izquierda, state="readonly", width=55, readonlybackground="#ffffff", font=("Arial", 11))
            entrada.grid(row=i+2, column=1, padx=5, pady=5)
            entradas.append(entrada)

        entry_id, entry_nombre, entry_direccion, entry_telefono, entry_rfc, entry_email = entradas

        frame_fecha_factura = tk.Frame(frame_izquierda)
        frame_fecha_factura.grid(row=len(etiquetas)+2, column=0, columnspan=2, pady=10)

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        tk.Label(frame_fecha_factura, text="Fecha: " + fecha_actual, font=("Arial", 14, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=10)
        actualizar_numero_factura(frame_fecha_factura)

        # Frame derecho: Selección de productos
        frame_derecha = tk.Frame(ventana_crear_factura, width=400, bg="#f0f0f0", bd=1, relief="solid")
        frame_derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame_derecha, text="Buscar Producto (Nombre):", font=("Arial", 12, "bold")).pack(pady=5)
        combo_productos = ttk.Combobox(frame_derecha)
        combo_productos.pack(pady=5)
        combo_productos.bind("<KeyRelease>", actualizar_productos_autocompletar)

        tk.Label(frame_derecha, text="Cantidad:", font=("Arial", 10)).pack(pady=5)
        entry_cantidad_producto = tk.Entry(frame_derecha)
        entry_cantidad_producto.pack(pady=5)

        tk.Button(frame_derecha, text="Agregar Producto", command=seleccionar_producto).pack(pady=5)

        tk.Label(frame_derecha, text="Productos seleccionados", font=("Arial", 12, "bold")).pack(pady=5)

        frame_treeview = tk.Frame(frame_derecha, height=150, width=850)
        frame_treeview.pack_propagate(False)
        frame_treeview.pack(padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_treeview)
        scrollbar.pack(side="right", fill="y")

        tree_seleccionados = ttk.Treeview(frame_treeview, columns=("id", "nombre", "precio", "cantidad"), show="headings", height=5, yscrollcommand=scrollbar.set)

        tree_seleccionados.heading("id", text="ID", anchor="center")
        tree_seleccionados.heading("nombre", text="Nombre", anchor="center")
        tree_seleccionados.heading("precio", text="Precio", anchor="center")
        tree_seleccionados.heading("cantidad", text="Cantidad", anchor="center")

        tree_seleccionados.column("id", anchor="center")
        tree_seleccionados.column("nombre", anchor="center")
        tree_seleccionados.column("precio", anchor="center")
        tree_seleccionados.column("cantidad", anchor="center")

        tree_seleccionados.pack(fill="both", expand=True)
        scrollbar.config(command=tree_seleccionados.yview)

        frame_totales = tk.Frame(frame_derecha, bg="#f0f0f0", bd=1, relief="solid")
        frame_totales.pack(padx=10, pady=10, fill="x", expand=True)

        tk.Label(frame_totales, text="Total", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

        labels_totales = ["Subtotal", "IVA (16%)", "Total", "Total en letras"]
        entries_totales = []

        for i, label in enumerate(labels_totales):
            tk.Label(frame_totales, text=label, bg="#f0f0f0", font=("Arial", 12)).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(frame_totales, width=80, font=("Arial", 12))
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            entries_totales.append(entry)

        entry_subtotal, entry_iva, entry_total, entry_total_letras = entries_totales

        tk.Button(frame_derecha, text="Generar Factura", command=generar_factura).pack(pady=10)

        boton_ventana_crear_factura = tk.Button(ventana_crear_factura, text="←", font=("Arial", 12), bg="#f0f0f0", fg="#007bff", relief="flat", command=regresar)
        boton_ventana_crear_factura.place(x=1250, y=20)

        # Inicializar combobox con los datos
        global usuarios, productos
        usuarios = Usuario.obtener_clientes()
        productos = Producto().obtener_productos()
        actualizar_comboboxes(usuarios, productos)

        ventana_crear_factura.withdraw()
    return ventana_crear_factura

def reiniciar_pantalla():
    # Limpiar el combobox de usuarios
    combo_usuarios.set('')

    # Limpiar las entradas de texto de los datos del usuario
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="readonly")

    entry_nombre.config(state="normal")
    entry_nombre.delete(0, tk.END)
    entry_nombre.config(state="readonly")

    entry_direccion.config(state="normal")
    entry_direccion.delete(0, tk.END)
    entry_direccion.config(state="readonly")

    entry_telefono.config(state="normal")
    entry_telefono.delete(0, tk.END)
    entry_telefono.config(state="readonly")

    entry_rfc.config(state="normal")
    entry_rfc.delete(0, tk.END)
    entry_rfc.config(state="readonly")

    entry_email.config(state="normal")
    entry_email.delete(0, tk.END)
    entry_email.config(state="readonly")

    # Limpiar el combobox de productos
    combo_productos.set('')

    # Limpiar la entrada de cantidad de productos
    entry_cantidad_producto.delete(0, tk.END)

    # Limpiar el Treeview de productos seleccionados
    tree_seleccionados.delete(*tree_seleccionados.get_children())

    # Reiniciar el subtotal, IVA y total en las entradas correspondientes
    entry_subtotal.delete(0, tk.END)
    entry_iva.delete(0, tk.END)
    entry_total.delete(0, tk.END)
    entry_total_letras.delete(0, tk.END)


def regresar():
    ventana_crear_factura.withdraw()
    ventana_crear_factura.regresar.deiconify()
    reiniciar_pantalla()
    actualizar_numero_factura(frame_fecha_factura)
    limpiar_datos() 

def actualizar_datos_al_abrir():
    global usuarios, productos
    usuarios = Usuario.obtener_clientes()
    productos = Producto().obtener_productos()
    actualizar_comboboxes(usuarios, productos)
