import threading
import time
import random
import numpy as np
from joblib import load
from pathlib import Path
import json

from database.db import SessionLocal
from database.modelodb import Prediccion

# ===== RUTAS =====
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "modelo" / "modelo_entrenado.pkl"
PARAMS_PATH = BASE_DIR / "preprocesamiento_datos" / "parametros_normalizados.json"

# ===== CARGAR MODELO =====
model = load(MODEL_PATH)

# ===== CARGAR PARÁMETROS DE NORMALIZACIÓN =====
with open(PARAMS_PATH, "r") as f:
    norm_params = json.load(f)

FEATURE_ORDER = [
    "ha_verdes_km2",
    "cobertura_arbolado_pct",
    "pm25",
    "pm10",
    "residuos_no_gestionados",
    "porcentaje_reciclaje",
    "porcentaje_transporte_limpio",
]


# ===== NORMALIZACIÓN =====


def apply_minmax(value, vmin, vmax):
    if vmax == vmin:
        return 0.5
    return (value - vmin) / (vmax - vmin)


def normalize_feature(name, value):
    col = norm_params["columns"][name]
    vmin = col["vmin"]
    vmax = col["vmax"]
    return apply_minmax(value, vmin, vmax)


# ===== GENERACIÓN DE DATOS (sensores simulados) =====


def generar_dato_realista():
    """
    Genera valores con rango razonable para simular un sensor real.
    """

    return {
        "ha_verdes_km2": random.uniform(5, 35),
        "cobertura_arbolado_pct": random.uniform(10, 45),
        "pm25": random.uniform(10, 50),
        "pm10": random.uniform(20, 90),
        "residuos_no_gestionados": random.uniform(0.2, 1.0),
        "porcentaje_reciclaje": random.uniform(5, 50),
        "porcentaje_transporte_limpio": random.uniform(10, 60),
    }


# ===== HILO DEL SIMULADOR =====


def simulador_sensores(intervalo=60):
    """
    Hilo que corre indefinidamente generando datos, normalizando,
    prediciendo y guardando en la BD.
    """
    print("[SIMULADOR] Iniciado correctamente.")

    while True:
        # ===== GENERAR DATO =====
        raw_data = generar_dato_realista()

        # ===== NORMALIZAR =====
        x_norm = [normalize_feature(feat, raw_data[feat]) for feat in FEATURE_ORDER]

        X = np.array([x_norm])

        # ===== PREDECIR =====
        ecoscore = float(model.predict(X)[0])

        # ===== GUARDAR EN BD =====
        db = SessionLocal()
        try:
            registro = Prediccion(
                ha_verdes_km2=raw_data["ha_verdes_km2"],
                cobertura_arbolado_pct=raw_data["cobertura_arbolado_pct"],
                pm25=raw_data["pm25"],
                pm10=raw_data["pm10"],
                residuos_no_gestionados=raw_data["residuos_no_gestionados"],
                porcentaje_reciclaje=raw_data["porcentaje_reciclaje"],
                porcentaje_transporte_limpio=raw_data["porcentaje_transporte_limpio"],
                ecoscore=ecoscore,
            )
            db.add(registro)
            db.commit()
        finally:
            db.close()

        print(f"[SIMULADOR] Nuevo ecoscore generado: {ecoscore:.2f}")

        # 5. esperar X segundos
        time.sleep(intervalo)


def iniciar_simulador_sensores():
    hilo = threading.Thread(
        target=simulador_sensores,
        args=(60,),  # tiempo entre predicciones (60 segundos)
        daemon=True,  # se cierra con Flask
    )
    hilo.start()
