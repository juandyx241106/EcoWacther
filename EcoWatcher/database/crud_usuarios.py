from sqlalchemy.orm import Session
from database.modelo_usuarios import Usuarios
from database.usuarios import SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash


def crear_usuario(nombre: str, email: str, contraseña: str, db: Session = None):
    """
    Crear un nuevo usuario en la base de datos.
    
    Args:
        nombre: Nombre del usuario
        email: Email único del usuario
        contraseña: Contraseña en texto plano (se hashea automáticamente)
        db: Sesión de la base de datos (opcional, crea una si no se proporciona)
    
    Returns:
        Usuario creado o None si hubo error
    """
    if db is None:
        db = SessionLocal()
        close_session = True
    else:
        close_session = False
    
    try:
        # Hash de la contraseña con bcrypt
        contraseña_hash = generate_password_hash(contraseña)
        
        # Crear usuario
        usuario = Usuarios(
            nombre=nombre,
            email=email,
            contraseña_hash=contraseña_hash,
            misiones_hechas=0,
            ecopoints=0
        )
        
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        return usuario
    
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
        return None
    
    finally:
        if close_session:
            db.close()


def obtener_usuario_por_email(email: str, db: Session = None):
    """
    Obtener un usuario por email.
    
    Args:
        email: Email del usuario
        db: Sesión de la base de datos (opcional)
    
    Returns:
        Usuario encontrado o None
    """
    if db is None:
        db = SessionLocal()
        close_session = True
    else:
        close_session = False
    
    try:
        usuario = db.query(Usuarios).filter(Usuarios.email == email).first()
        return usuario
    
    finally:
        if close_session:
            db.close()


def obtener_usuario_por_id(usuario_id: int, db: Session = None):
    """
    Obtener un usuario por ID.
    
    Args:
        usuario_id: ID del usuario
        db: Sesión de la base de datos (opcional)
    
    Returns:
        Usuario encontrado o None
    """
    if db is None:
        db = SessionLocal()
        close_session = True
    else:
        close_session = False
    
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
        return usuario
    
    finally:
        if close_session:
            db.close()


def verificar_contraseña(email: str, contraseña: str, db: Session = None):
    """
    Verificar si la contraseña es correcta para un usuario.
    
    Args:
        email: Email del usuario
        contraseña: Contraseña en texto plano
        db: Sesión de la base de datos (opcional)
    
    Returns:
        Usuario si es correcto, None si no
    """
    usuario = obtener_usuario_por_email(email, db)
    
    if usuario:
        if check_password_hash(usuario.contraseña_hash, contraseña):
            return usuario
    
    return None


def actualizar_ecopoints(usuario_id: int, cantidad: float, db: Session = None):
    """
    Sumar ecopoints a un usuario.
    
    Args:
        usuario_id: ID del usuario
        cantidad: Cantidad de ecopoints a sumar
        db: Sesión de la base de datos (opcional)
    
    Returns:
        Usuario actualizado o None
    """
    if db is None:
        db = SessionLocal()
        close_session = True
    else:
        close_session = False
    
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
        if usuario:
            usuario.ecopoints += cantidad
            db.commit()
            db.refresh(usuario)
            return usuario
        return None
    
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar ecopoints: {e}")
        return None
    
    finally:
        if close_session:
            db.close()


def incrementar_misiones(usuario_id: int, db: Session = None):
    """
    Incrementar el contador de misiones realizadas.
    
    Args:
        usuario_id: ID del usuario
        db: Sesión de la base de datos (opcional)
    
    Returns:
        Usuario actualizado o None
    """
    if db is None:
        db = SessionLocal()
        close_session = True
    else:
        close_session = False
    
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
        if usuario:
            usuario.misiones_hechas += 1
            db.commit()
            db.refresh(usuario)
            return usuario
        return None
    
    except Exception as e:
        db.rollback()
        print(f"Error al incrementar misiones: {e}")
        return None
    
    finally:
        if close_session:
            db.close()
