# app.py
import os
import json
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from joblib import load
import pandas as pd

# ===========================
# Rutas (relativas al proyecto)
# ===========================
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "modelo" / "modelo_entrenado.pkl"
PARAMS_PATH = BASE_DIR / "preprocesamiento_datos" / "parametros_normalizados.json"

# ===== INICIALIZAR APP Y CARGAR RECURSOS =====
app = Flask(__name__)

# cargar modelo
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Modelo no encontrado en: {MODEL_PATH}")
model = load(MODEL_PATH)

# cargar parámetros de normalización
if not PARAMS_PATH.exists():
    raise FileNotFoundError(f"Parámetros no encontrados en: {PARAMS_PATH}")
with open(PARAMS_PATH, "r") as f:
    norm_params = json.load(f)

# columnas/orden que el modelo espera (debe coincidir con el entrenamiento)
FEATURE_ORDER = [
    "ha_verdes_km2",
    "cobertura_arbolado_pct",
    "pm25",
    "pm10",
    "residuos_no_gestionados",
    "porcentaje_reciclaje",
    "porcentaje_transporte_limpio",
]

# indicador de variables "más es peor" (invertir)
# El modelo fue entrenado con las columnas normalizadas tal cual (p.ej. pm25_norm)
# y no con su inverso. Por tanto no invertimos las características antes de
# pasar al modelo — la inversión se aplicó en el cálculo del ecoscore durante
# el preprocesamiento para aportar la contribución correcta al score final.
INVERT_FEATURES = set()


# ===== FUNCIONES DE NORMALIZACIÓN =====
def apply_minmax(value, vmin, vmax):
    if vmin is None or vmax is None or vmax == vmin:
        return 0.5
    return float((value - vmin) / (vmax - vmin))


def apply_percentile(value, p_low, p_high):
    if p_low is None or p_high is None or p_high == p_low:
        return 0.5
    x = float(value)
    if x <= p_low:
        return 0.0
    if x >= p_high:
        return 1.0
    return (x - p_low) / (p_high - p_low)


def normalize_feature(name, raw_value):
    """
    Normaliza un valor usando norm_params y el método guardado.
    Devuelve valor normalizado en 0..1
    """
    method = norm_params.get("method", "minmax")
    colparams = norm_params.get("columns", {}).get(name, {})
    # Si el usuario envía string permitido (vacío), convertir a float por seguridad
    x = float(raw_value)
    if method == "minmax":
        vmin = colparams.get("vmin", None)
        vmax = colparams.get("vmax", None)
        return apply_minmax(x, vmin, vmax)
    else:
        p_low = colparams.get("p_low", None)
        p_high = colparams.get("p_high", None)
        return apply_percentile(x, p_low, p_high)


# ===== RUTA WEB ======
@app.route("/", methods=["GET"])
def index():
    # mostrar formulario (vacío)
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # leer inputs desde el form
    inputs = {}
    for feat in FEATURE_ORDER:
        # el nombre del input en el formulario debe coincidir con feat
        raw = request.form.get(feat)
        if raw is None or raw.strip() == "":
            # puedes cambiar comportamiento: ahora devolvemos error simple
            return render_template("index.html", error=f"Falta valor para {feat}")
        try:
            inputs[feat] = float(raw)
        except ValueError:
            return render_template(
                "index.html", error=f"Valor inválido para {feat}: {raw}"
            )

    # normalizar en el mismo orden que el modelo espera
    x_norm = []
    for feat in FEATURE_ORDER:
        norm_val = normalize_feature(feat, inputs[feat])
        # Nota: no invertir aquí — el modelo fue entrenado con los valores
        # normalizados tal cual (v. preprocesador). Mantener consistencia.
        x_norm.append(norm_val)
        print(f"{feat} → normalizado = {norm_val}")


    X = np.array([x_norm])  # forma (1, n_features)

    # predecir con el modelo entrenado
    pred = model.predict(X)[0]  # ecoscore 0-500
    pred_rounded = round(float(pred), 3)

    # categoría simple (mismos umbrales que en preprocesador)
    if pred_rounded >= 450:
        cat = "Excelente"
    elif pred_rounded >= 350:
        cat = "Bueno"
    elif pred_rounded >= 200:
        cat = "Moderado"
    else:
        cat = "Crítico"

    return render_template(
        "index.html", prediction=pred_rounded, category=cat, inputs=inputs
    )


# ===== MAIN =====
if __name__ == "__main__":
    app.run(debug=True)
