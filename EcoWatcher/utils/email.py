"""
Funciones para enviar emails en la aplicación.
Usa SMTP por defecto (sin librería externa).
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


# Configuración de email
EMAIL_CONFIG = {
    "sender_email": os.getenv("EMAIL_SENDER", "ecowatcherauth@gmail.com"),
    "sender_password": os.getenv("EMAIL_PASSWORD", "dagv klby pypl uvyh"),
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
}


def enviar_codigo_verificacion(email_destino: str, codigo: str) -> bool:
    """
    Enviar código de verificación por email.
    
    Args:
        email_destino: Email del usuario
        codigo: Código de 6 dígitos
    
    Returns:
        True si se envió correctamente, False si no
    """
    try:
        # Crear mensaje
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = "Código de verificación - EcoWatcher"
        mensaje["From"] = EMAIL_CONFIG["sender_email"]
        mensaje["To"] = email_destino

        # HTML del email
        html = f"""\
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
              <h2 style="color: #6c3483;">¡Bienvenido a EcoWatcher!</h2>
              <p>Para confirmar tu email, usa el siguiente código:</p>
              
              <div style="text-align: center; margin: 30px 0;">
                <h1 style="color: #58D68D; letter-spacing: 2px; font-size: 32px;">{codigo}</h1>
              </div>
              
              <p style="color: #666;">Este código expira en 10 minutos.</p>
              <p style="color: #666;">Si no solicitaste este código, ignora este email.</p>
              
              <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
              <p style="font-size: 12px; color: #999;">EcoWatcher © 2025</p>
            </div>
          </body>
        </html>
        """

        parte_html = MIMEText(html, "html")
        mensaje.attach(parte_html)

        # Enviar email
        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            server.sendmail(EMAIL_CONFIG["sender_email"], email_destino, mensaje.as_string())

        print(f"Email enviado a {email_destino}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Error: Credenciales de email incorrectas")
        return False
    except smtplib.SMTPException as e:
        print(f"Error al enviar email: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def enviar_codigo_reset_contraseña(email_destino: str, codigo: str) -> bool:
    """
    Enviar código de reset de contraseña por email.
    
    Args:
        email_destino: Email del usuario
        codigo: Código de 6 dígitos
    
    Returns:
        True si se envió correctamente, False si no
    """
    try:
        # Crear mensaje
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = "Código para resetear contraseña - EcoWatcher"
        mensaje["From"] = EMAIL_CONFIG["sender_email"]
        mensaje["To"] = email_destino

        # HTML del email
        html = f"""\
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
              <h2 style="color: #6c3483;">Resetear Contraseña</h2>
              <p>Recibimos una solicitud para resetear tu contraseña. Usa el siguiente código:</p>
              
              <div style="text-align: center; margin: 30px 0;">
                <h1 style="color: #e53935; letter-spacing: 2px; font-size: 32px;">{codigo}</h1>
              </div>
              
              <p style="color: #666;">Este código expira en 15 minutos.</p>
              <p style="color: #666;">Si no solicitaste resetear tu contraseña, ignora este email.</p>
              
              <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
              <p style="font-size: 12px; color: #999;">EcoWatcher © 2025</p>
            </div>
          </body>
        </html>
        """

        parte_html = MIMEText(html, "html")
        mensaje.attach(parte_html)

        # Enviar email
        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            server.sendmail(EMAIL_CONFIG["sender_email"], email_destino, mensaje.as_string())

        print(f"Email de reset enviado a {email_destino}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Error: Credenciales de email incorrectas")
        return False
    except smtplib.SMTPException as e:
        print(f"Error al enviar email: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False