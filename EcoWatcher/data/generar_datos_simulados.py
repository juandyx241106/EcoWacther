import pandas as pd
import numpy as np
import os

# ===== RUTAS =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "bogota_sin_procesar.csv")

# Localidades de Bogotá
LOCALIDADES = [
    "Usaquén", "Chapinero", "Santa Fe", "San Cristóbal", "Usme",
    "Tunjuelito", "Bosa", "Kennedy", "Fontibón", "Engativá",
    "Suba", "Barrios Unidos", "Teusaquillo", "Los Mártires",
    "Antonio Nariño", "Puente Aranda", "La Candelaria",
    "Rafael Uribe Uribe", "Ciudad Bolívar", "Sumapaz"
]

N = 150  # Número de filas simuladas

# ===== GENERAR DATOS SIMULADOS =====
np.random.seed(42)

df = pd.DataFrame({
    "localidad": np.random.choice(LOCALIDADES, size=N),

    "ha_verdes_km2": np.random.uniform(1.0, 25.0, size=N),

    "cobertura_arbolado_pct": np.random.uniform(5, 70, size=N),

    "pm25": np.random.uniform(5, 45, size=N),

    "pm10": np.random.uniform(15, 100, size=N),

    "residuos_no_gestionados_kg_por_hab_dia": np.random.uniform(0.1, 1.2, size=N),

    "porcentaje_reciclaje": np.random.uniform(5, 40, size=N),

    "porcentaje_transporte_limpio": np.random.uniform(5, 35, size=N)
})

# ===== GUARDAR DATOS SIMULADOS =====
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Archivo generado en:\n{OUTPUT_PATH}")
print(df.head())
