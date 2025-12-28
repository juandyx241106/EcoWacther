import os
from pathlib import Path

# ===== RUTAS =====
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "modelo" / "modelo_entrenado.pkl"
PARAMS_PATH = BASE_DIR / "preprocesamiento_datos" / "parametros_normalizados.json"

# ===== CONFIGURACIÓN FLASK =====
SECRET_KEY = "tu_clave_secreta_aqui_cambiar_en_produccion"
DEBUG = True

# ===== COLUMNAS DEL MODELO =====
FEATURE_ORDER = [
    "ha_verdes_km2",
    "cobertura_arbolado_pct",
    "pm25",
    "pm10",
    "residuos_no_gestionados",
    "porcentaje_reciclaje",
    "porcentaje_transporte_limpio",
]
