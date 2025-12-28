from sqlalchemy import Boolean, Column, Integer, Float, DateTime, String
from sqlalchemy.sql import func
from .usuarios import Base


class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    # ===== VARIABLES DE ENTRADA =====
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    contraseña_hash = Column(String, nullable=False)
    misiones_hechas = Column(Integer, default=0)
    ecopoints = Column(Float, default=0)
    localidad = Column(String, nullable=True)
    email_confirmado = Column(Boolean, default=False)
    codigo_confirmacion = Column(String)
    fecha_expiracion_codigo = Column(DateTime)
    