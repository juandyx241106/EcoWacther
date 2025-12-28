from flask import Blueprint, render_template, request, redirect, url_for, session
from database.crud_usuarios import crear_usuario, verificar_contraseña

auth = Blueprint('auth', __name__)


@auth.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        contraseña = request.form.get("contraseña", "")
        contraseña_confirm = request.form.get("contraseña_confirm", "")
        
        if not nombre or not email or not contraseña:
            return render_template("crear_cuenta.html", error="Todos los campos son requeridos")
        
        if contraseña != contraseña_confirm:
            return render_template("crear_cuenta.html", error="Las contraseñas no coinciden")
        
        if len(contraseña) < 6:
            return render_template("crear_cuenta.html", error="La contraseña debe tener al menos 6 caracteres")
        
        usuario = crear_usuario(nombre, email, contraseña)
        
        if usuario:
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            return redirect(url_for("predicciones.index"))
        else:
            return render_template("crear_cuenta.html", error="El email ya está registrado")
    
    return render_template("crear_cuenta.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        contraseña = request.form.get("contraseña", "")
        
        if not email or not contraseña:
            return render_template("login.html", error="Email y contraseña requeridos")
        
        usuario = verificar_contraseña(email, contraseña)
        
        if usuario:
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
