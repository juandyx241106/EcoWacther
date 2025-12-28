from flask import Blueprint, render_template, request, redirect, url_for, session
from database.crud_usuarios import (
    crear_usuario, 
    verificar_contraseña, 
    crear_usuario_no_confirmado,
    generar_codigo_verificacion,
    verificar_codigo_confirmacion,
    generar_codigo_reset_contraseña,
    verificar_codigo_reset_contraseña,
    obtener_usuario_por_email
)
from utils.email import enviar_codigo_verificacion, enviar_codigo_reset_contraseña

auth = Blueprint('auth', __name__)


@auth.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        contraseña = request.form.get("contraseña", "")
        contraseña_confirm = request.form.get("contraseña_confirm", "")
        localidad = request.form.get("localidad", "").strip()
        
        if not nombre or not email or not contraseña:
            return render_template("crear_cuenta.html", error="Todos los campos son requeridos")
        
        if contraseña != contraseña_confirm:
            return render_template("crear_cuenta.html", error="Las contraseñas no coinciden")
        
        if len(contraseña) < 6:
            return render_template("crear_cuenta.html", error="La contraseña debe tener al menos 6 caracteres")
        
        # Crear usuario sin confirmar
        usuario = crear_usuario_no_confirmado(nombre, email, contraseña, localidad)
        
        if usuario:
            # Generar código de verificación
            codigo = generar_codigo_verificacion(email)
            
            if codigo:
                # Enviar email
                if enviar_codigo_verificacion(email, codigo):
                    # Guardar email en sesión temporal para verificación
                    session["email_pendiente"] = email
                    return redirect(url_for("auth.verificar_email"))
                else:
                    return render_template("crear_cuenta.html", error="Error al enviar email. Intenta de nuevo.")
            else:
                return render_template("crear_cuenta.html", error="Error al generar código de verificación")
        else:
            return render_template("crear_cuenta.html", error="El email ya está registrado")
    
    return render_template("crear_cuenta.html")


@auth.route("/verificar-email", methods=["GET", "POST"])
def verificar_email():
    email = session.get("email_pendiente")
    
    if not email:
        return redirect(url_for("auth.crear_cuenta"))
    
    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()
        
        if not codigo or len(codigo) != 6:
            return render_template("verificar_email.html", error="Código inválido")
        
        # Verificar código
        usuario = verificar_codigo_confirmacion(email, codigo)
        
        if usuario:
            # Limpiar sesión y hacer login automático
            session.pop("email_pendiente", None)
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            return redirect(url_for("predicciones.index"))
        else:
            return render_template("verificar_email.html", error="Código inválido o expirado")
    
    return render_template("verificar_email.html", email=email)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        contraseña = request.form.get("contraseña", "")
        
        if not email or not contraseña:
            return render_template("login.html", error="Email y contraseña requeridos")
        
        usuario = verificar_contraseña(email, contraseña)
        
        if usuario:
            if not usuario.email_confirmado:
                return render_template("login.html", error="Email no confirmado. Revisa tu bandeja de entrada.")
            
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            return redirect(url_for("predicciones.index"))
        else:
            return render_template("login.html", error="Email o contraseña incorrectos")
    
    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth.route("/olvido-contraseña", methods=["GET", "POST"])
def olvido_contraseña():
    """Solicitar reset de contraseña"""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        
        if not email:
            return render_template("olvido_contraseña.html", error="Email requerido")
        
        # Verificar que el usuario existe y está confirmado
        usuario = obtener_usuario_por_email(email)
        
        if not usuario:
            return render_template("olvido_contraseña.html", error="No se encontró una cuenta registrada con ese correo")
        
        if not usuario.email_confirmado:
            return render_template("olvido_contraseña.html", error="Email no confirmado. Completa la verificación primero.")
        
        # Generar código de reset
        codigo = generar_codigo_reset_contraseña(email)
        
        if codigo:
            # Enviar email
            if enviar_codigo_reset_contraseña(email, codigo):
                session["email_reset"] = email
                return redirect(url_for("auth.reset_contraseña"))
            else:
                return render_template("olvido_contraseña.html", error="Error al enviar email. Intenta de nuevo.")
        else:
            return render_template("olvido_contraseña.html", error="Error al generar código. Intenta de nuevo.")
    
    return render_template("olvido_contraseña.html")


@auth.route("/reset-contraseña", methods=["GET", "POST"])
def reset_contraseña():
    """Resetear contraseña con código"""
    email = session.get("email_reset")
    
    if not email:
        return redirect(url_for("auth.olvido_contraseña"))
    
    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()
        nueva_contraseña = request.form.get("nueva_contraseña", "")
        confirmar_contraseña = request.form.get("confirmar_contraseña", "")
        
        if not codigo or len(codigo) != 6:
            return render_template("reset_contraseña.html", error="Código inválido", email=email)
        
        if not nueva_contraseña or not confirmar_contraseña:
            return render_template("reset_contraseña.html", error="Contraseñas requeridas", email=email)
        
        if nueva_contraseña != confirmar_contraseña:
            return render_template("reset_contraseña.html", error="Las contraseñas no coinciden", email=email)
        
        if len(nueva_contraseña) < 6:
            return render_template("reset_contraseña.html", error="La contraseña debe tener al menos 6 caracteres", email=email)
        
        # Verificar código y actualizar contraseña
        usuario = verificar_codigo_reset_contraseña(email, codigo, nueva_contraseña)
        
        if usuario:
            # Limpiar sesión
            session.pop("email_reset", None)
            # Redirigir al login con mensaje
            return redirect(url_for("auth.login"))
        else:
            return render_template("reset_contraseña.html", error="Código inválido o expirado", email=email)
    
    return render_template("reset_contraseña.html", email=email)