import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump

# ===== RUTAS =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "bogota_procesado.csv")
MODEL_PATH = os.path.join(BASE_DIR, "modelo", "modelo_entrenado.pkl")


# ===== CARGA DE DATOS =====
def cargar_datos(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encuentra el archivo: {path}")

    df = pd.read_csv(path)

    columnas_entrada = [
        "ha_verdes_km2_norm",
        "cobertura_arbolado_pct_norm",
        "pm25_norm",
        "pm10_norm",
        "residuos_no_gestionados_norm",
        "porcentaje_reciclaje_norm",
        "porcentaje_transporte_limpio_norm",
    ]

    columna_objetivo = "ecoscore_0_500"

    X = df[columnas_entrada].values
    y = df[columna_objetivo].values

    return X, y, columnas_entrada


# ===== ENTRENAMIENTO =====
def entrenar_modelo(X, y):
    # Dividir datos
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Crear modelo
    modelo = RandomForestRegressor(n_estimators=300, random_state=42)

    print("Entrenando modelo...")
    modelo.fit(X_train, Y_train)

    # Predicciones
    y_pred = modelo.predict(X_test)

    # Métricas
    mse = mean_squared_error(Y_test, y_pred)
    r2 = r2_score(Y_test, y_pred)

    print("\n==== RESULTADOS DEL MODELO ====")
    print(f"MSE: {mse:.4f}")
    print(f"R² : {r2:.4f}")

    return modelo


# ===== GUARDAR MODELO =====
def guardar_modelo(modelo, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    dump(modelo, path)
    print(f"\nModelo guardado en: {path}")


# ===== MAIN =====
if __name__ == "__main__":
    X, y, columnas = cargar_datos(DATA_PATH)
    modelo = entrenar_modelo(X, y)
    guardar_modelo(modelo, MODEL_PATH)

    print("\nColumnas usadas en el entrenamiento:")
    for c in columnas:
        print(f" - {c}")
