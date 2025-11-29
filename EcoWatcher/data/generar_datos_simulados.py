import numpy as np
import pandas as pd
import os


# ===== RUTAS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(DATA_DIR, "bogota_sin_procesar.csv")



def generar_datos(rango, n):
    """Genera valores uniformes dentro de un rango."""
    return np.random.uniform(rango[0], rango[1], n)

# ===== RANGOS DE DATOS =====
RANGOS_CRITICO = {
    "ha_verdes_km2": (0, 10),
    "cobertura_arbolado_pct": (5, 15),
    "pm25": (40, 60),
    "pm10": (70, 100),
    "residuos_no_gestionados": (0.9, 1.5),
    "porcentaje_reciclaje": (0, 15),
    "porcentaje_transporte_limpio": (0, 15),
    "ecoscore": (0, 200)
}

RANGOS_MODERADO = {
    "ha_verdes_km2": (8, 18),
    "cobertura_arbolado_pct": (15, 28),
    "pm25": (20, 40),
    "pm10": (40, 70),
    "residuos_no_gestionados": (0.4, 0.9),
    "porcentaje_reciclaje": (10, 35),
    "porcentaje_transporte_limpio": (15, 40),
    "ecoscore": (200, 350)
}

RANGOS_BUENO = {
    "ha_verdes_km2": (15, 40),
    "cobertura_arbolado_pct": (28, 50),
    "pm25": (5, 20),
    "pm10": (10, 40),
    "residuos_no_gestionados": (0.0, 0.4),
    "porcentaje_reciclaje": (35, 60),
    "porcentaje_transporte_limpio": (40, 80),
    "ecoscore": (350, 500)
}

# ===== GENERAR DATAFRAME =====
def generar_df(rangos, n):
    data = {}
    for col, r in rangos.items():
        data[col] = generar_datos(r, n)
    return pd.DataFrame(data)

# ===== CREAR DATASET SINTÉTICO =====
df = pd.concat([
    generar_df(RANGOS_CRITICO, 150),
    generar_df(RANGOS_MODERADO, 200),
    generar_df(RANGOS_BUENO, 150)
], ignore_index=True)

# ===== GUARDAR DATASET =====
df.to_csv(OUTPUT_PATH, index=False)

print("Dataset sintético generado con éxito.")
