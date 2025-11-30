from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ===== RUTA =====
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ===== ARCHIVO DE BASE DE DATOS =====
DB_PATH = os.path.join(BASE_DIR, "data", "ecosense.db")

# ===== MOTOR DE BASE DE DATOS =====
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

# ===== SESIÓN =====
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== BASE DE MODELOS =====
Base = declarative_base()


def init_db():
    """
    Crear las tablas si no existen.
    """
    from . import modelodb  # importar modelos para que SQLAlchemy los registre

    Base.metadata.create_all(bind=engine)
