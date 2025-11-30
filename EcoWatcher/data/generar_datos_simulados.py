import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(BASE_DIR, "data", "dataset_mejorado.csv")


# ===== HELPERS =====
def normalizar_minmax(x, vmin, vmax):
    return (x - vmin) / (vmax - vmin)


def generar_un_valor(rango):
    return np.random.uniform(rango[0], rango[1])


# ===== RANGOS ESTABLECIDOS =====

RANGOS = {
    "ha_verdes_km2": (0.0077, 39.85),
    "cobertura_arbolado_pct": (5.07, 49.96),
    "pm25": (5.04, 59.79),
    "pm10": (10.32, 99.96),
    "residuos_no_gestionados": (0.005, 1.497),
    "porcentaje_reciclaje": (0.22, 59.9),
    "porcentaje_transporte_limpio": (0.0036, 79.94),
}

# Variables donde MÁS = PEOR (son invertidas en el ecoscore)
NEGATIVAS = {"pm25", "pm10", "residuos_no_gestionados"}


# ===== GENERADORES DE CASOS =====
def generar_casos_perfectos(n):
    """
    Casos 100% ideales → ecoscore = 500
    """
    filas = []
    for _ in range(n):
        fila = {
            "ha_verdes_km2": RANGOS["ha_verdes_km2"][1],
            "cobertura_arbolado_pct": RANGOS["cobertura_arbolado_pct"][1],
            "pm25": RANGOS["pm25"][0],
            "pm10": RANGOS["pm10"][0],
            "residuos_no_gestionados": RANGOS["residuos_no_gestionados"][0],
            "porcentaje_reciclaje": RANGOS["porcentaje_reciclaje"][1],
            "porcentaje_transporte_limpio": RANGOS["porcentaje_transporte_limpio"][1],
            "ecoscore_0_500": 500,
        }
        filas.append(fila)
    return filas


def generar_casos_muy_buenos(n):
    """
    Casos buenos pero no perfectos → ecoscore 430–490
    """
    filas = []
    for _ in range(n):
        fila = {
            "ha_verdes_km2": np.random.uniform(0.75, 1.0) * RANGOS["ha_verdes_km2"][1],
            "cobertura_arbolado_pct": np.random.uniform(0.75, 1.0)
            * RANGOS["cobertura_arbolado_pct"][1],
            "pm25": np.random.uniform(RANGOS["pm25"][0], RANGOS["pm25"][0] + 4),
            "pm10": np.random.uniform(RANGOS["pm10"][0], RANGOS["pm10"][0] + 10),
            "residuos_no_gestionados": np.random.uniform(
                0.0, RANGOS["residuos_no_gestionados"][0] + 0.05
            ),
            "porcentaje_reciclaje": np.random.uniform(0.75, 1.0)
            * RANGOS["porcentaje_reciclaje"][1],
            "porcentaje_transporte_limpio": np.random.uniform(0.75, 1.0)
            * RANGOS["porcentaje_transporte_limpio"][1],
            "ecoscore_0_500": np.random.uniform(430, 490),
        }
        filas.append(fila)
    return filas


def generar_casos_terribles(n):
    """
    Casos desastrosos → ecoscore 0–50
    (Se empujan a los extremos negativos)
    """
    filas = []
    for _ in range(n):
        fila = {
            "ha_verdes_km2": RANGOS["ha_verdes_km2"][0],
            "cobertura_arbolado_pct": RANGOS["cobertura_arbolado_pct"][0],
            "pm25": RANGOS["pm25"][1],
            "pm10": RANGOS["pm10"][1],
            "residuos_no_gestionados": RANGOS["residuos_no_gestionados"][1],
            "porcentaje_reciclaje": RANGOS["porcentaje_reciclaje"][0],
            "porcentaje_transporte_limpio": RANGOS["porcentaje_transporte_limpio"][0],
            "ecoscore_0_500": np.random.uniform(0, 50),
        }
        filas.append(fila)
    return filas


# ===== MAIN =====
if __name__ == "__main__":
    print("Generando dataset mejorado...")

    filas = []
    filas += generar_casos_perfectos(100)
    filas += generar_casos_muy_buenos(100)
    filas += generar_casos_terribles(100)

    df = pd.DataFrame(filas)

    df.to_csv(OUT_PATH, index=False)

    print(f"Dataset mejorado guardado en:\n{OUT_PATH}")
    print(df.head())
