from database.conexion import conexion
from utils.enviar_correo import enviar_correo

# Clase Usuario
class Usuario:
    # Constructor de la clase
    def __init__(self, id=None, usuario=None, email=None, contraseña=None, tel=None) -> None:
        self.id = id
        self.usuario = usuario
        self.contraseña = contraseña
        self.email = email
        self.tel = tel
    
    # Método para crear un usuario
    def crear(self):
        cursor = conexion.cursor()

        # Insertar usuario en la base de datos
        cursor.execute(
            "INSERT INTO usuarios (Usuario, Contraseña, Email, Tel) VALUES (?, ?, ?, ?)",
            (self.usuario, self.contraseña, self.email, self.tel)
        )
        cursor.close() # Cerrar cursor
        conexion.commit()
    
    # Método para validar usuario y contraseña
    def valida_usuario_contraseña(self) -> bool:
        cursor = conexion.cursor()

        # Buscar usuario en la base de datos por usuario y contraseña
        cursor.execute(
            "SELECT * FROM usuarios WHERE Usuario = ? AND Contraseña = ?",
            (self.usuario, self.contraseña)
        )
        usuario = cursor.fetchone()
        cursor.close()
        
        return usuario is not None

    # Método para enviar correo de recuperación de contraseña
    def enviar_correo_recuperacion(self):
        cursor = conexion.cursor()

        # Buscar usuario en la base de datos por email y obtener usuario y contraseña
        cursor.execute(
            "SELECT Usuario, Contraseña FROM usuarios WHERE Email = ?",
            (self.email,)
        )
        datos = cursor.fetchone()
        cursor.close()

        # Si no se encontró el usuario, no se envía el correo
        if datos is None:
            return
        
        usuario, contraseña = datos
        asunto = "Recuperación de contraseña"
        cuerpo = f"usuario: {usuario} contraseña: {contraseña}"

        enviar_correo(self.email, asunto, cuerpo)
    
    def obtener_clientes(self):
        cursor = conexion.cursor()
        
        cursor.execute("SELECT * FROM clientes")
        data = cursor.fetchall()
        usuarios = []
        
        for registro in data:
            id, nombre, email, tel, direccion, rfc, fecha_nac = registro
            usuarios.append(
                {"id": str(id), "nombre": nombre, "email": email, "telefono": tel, "direccion": direccion, "rfc": rfc, "fecha": fecha_nac}
            )
        
        return usuarios
        
        
