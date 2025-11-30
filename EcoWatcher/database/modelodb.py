# database/models.py

from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from .db import Base

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)

    # ===== VARIABLES DE ENTRADA =====
    ha_verdes_km2 = Column(Float, nullable=False)
    cobertura_arbolado_pct = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=False)
    pm10 = Column(Float, nullable=False)
    residuos_no_gestionados = Column(Float, nullable=False)
    porcentaje_reciclaje = Column(Float, nullable=False)
    porcentaje_transporte_limpio = Column(Float, nullable=False)

    # ===== RESULTADO =====
    ecoscore = Column(Float, nullable=False)

    # ===== CUÁNDO SE PRODUJO LA PREDICCIÓN =====
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
