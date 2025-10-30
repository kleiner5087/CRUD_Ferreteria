import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_port = 587 # Puerto de Google SMTP Server
smtp_server = "smtp.gmail.com"  # Servidor de correo de Google

email_from = "vardo704@gmail.com" # Correo de donde se envía el mensaje
pswd = "juehwynffetcjdyd" # Contraseña del correo

# Función para enviar correos
def enviar_correo(destinatario, asunto, cuerpo):    
    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = email_from
    message["To"] = destinatario
    message["Subject"] = asunto
    message.attach(MIMEText(cuerpo, "plain", "utf-8"))
    
    try:
        print("Conectandose al servidor...")
        simple_email_context = ssl.create_default_context()
        
        # Conectar y enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as TIE_server:
            TIE_server.starttls(context=simple_email_context)
            TIE_server.login(email_from, pswd)
            print("Conectado al servidor")
            
            print(f"Enviando correo a - {destinatario}")
            TIE_server.sendmail(email_from, destinatario, message.as_string())
            print("Correo enviado")

    except Exception as e:
        print("Error:", e)

