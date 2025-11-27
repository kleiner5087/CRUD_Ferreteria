from database.conexion import conexion
from utils.enviar_correo import enviar_correo
from clases.repository import get_all_clients, create_user, get_user_by_credentials, get_user_by_email

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
        success, info = create_user(self.usuario, self.contraseña, self.email, self.tel)
        return success, info
    
    # Método para validar usuario y contraseña
    def valida_usuario_contraseña(self) -> bool:
        usuario = get_user_by_credentials(self.usuario, self.contraseña)
        return usuario is not None

    # Método para enviar correo de recuperación de contraseña
    def enviar_correo_recuperacion(self):
        datos = get_user_by_email(self.email)
        if datos is None:
            return False

        usuario, contraseña = datos
        asunto = "Recuperación de contraseña"
        cuerpo = f"usuario: {usuario} contraseña: {contraseña}"

        enviar_correo(self.email, asunto, cuerpo)
        return True
    
    @staticmethod
    def obtener_clientes():
        data = get_all_clients()
        usuarios = []
        for registro in data:
            id, nombre, email, tel, direccion, rfc, fecha_nac = registro
            usuarios.append(
                {"id": str(id), "nombre": nombre, "email": email, "telefono": tel, "direccion": direccion, "rfc": rfc, "fecha": fecha_nac}
            )
        return usuarios