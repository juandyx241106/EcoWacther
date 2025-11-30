import os
import json
from pathlib import Path
from database.db import SessionLocal, init_db
from database.modelodb import Prediccion
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from joblib import load
import pandas as pd
from sensor.simulador import iniciar_simulador_sensores


# ===== RUTAS DE RECURSOS =====
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "modelo" / "modelo_entrenado.pkl"
PARAMS_PATH = BASE_DIR / "preprocesamiento_datos" / "parametros_normalizados.json"

# ===== INICIALIZAR APP Y CARGAR RECURSOS =====
app = Flask(__name__)

# ===== CARGAR MODELO =====
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Modelo no encontrado en: {MODEL_PATH}")
model = load(MODEL_PATH)

# ===== CARGAR PARÁMETROS DE NORMALIZACIÓN =====
if not PARAMS_PATH.exists():
    raise FileNotFoundError(f"Parámetros no encontrados en: {PARAMS_PATH}")
with open(PARAMS_PATH, "r") as f:
    norm_params = json.load(f)

# ===== COLUMNAS/ORDEN QUE EL MODELO ESPERA =====
FEATURE_ORDER = [
    "ha_verdes_km2",
    "cobertura_arbolado_pct",
    "pm25",
    "pm10",
    "residuos_no_gestionados",
    "porcentaje_reciclaje",
    "porcentaje_transporte_limpio",
]


# ===== FUNCIONES DE NORMALIZACIÓN =====
def apply_minmax(value, vmin, vmax):
    if vmin is None or vmax is None or vmax == vmin:
        return 0.5
    return float((value - vmin) / (vmax - vmin))


def normalize_feature(name, raw_value):
    method = norm_params.get("method", "minmax")
    colparams = norm_params.get("columns", {}).get(name, {})
    x = float(raw_value)

    if method == "minmax":
        return apply_minmax(x, colparams.get("vmin"), colparams.get("vmax"))

    return 0.5  # fallback seguro


# ===== FUNCIONES DE RECOMENDACIONES =====
def generar_recomendaciones(inputs, score):
    recomendaciones = []

    # ===== CATEGORÍA GENERAL =====
    if score < 200:
        recomendaciones.append(
            {
                "texto": "El ecosistema está en estado CRÍTICO. Se requiere intervención urgente.",
                "clase": "critico",
            }
        )
    elif score < 350:
        recomendaciones.append(
            {
                "texto": "Estado MODERADO: hay problemas, pero pueden mejorarse con acciones continuas.",
                "clase": "moderado",
            }
        )
    elif score < 450:
        recomendaciones.append(
            {
                "texto": "Estado BUENO: sigue fortaleciendo los aspectos ambientales.",
                "clase": "bueno",
            }
        )
    else:
        recomendaciones.append(
            {
                "texto": "¡Excelente estado ambiental! Mantén las prácticas actuales.",
                "clase": "excelente",
            }
        )

    # ===== VARIABLES INDIVIDUALES =====
    if inputs["ha_verdes_km2"] < 5:
        recomendaciones.append(
            {
                "texto": "Muy pocas hectáreas verdes. Se recomienda ampliar zonas verdes.",
                "clase": "critico",
            }
        )
    elif inputs["ha_verdes_km2"] < 10:
        recomendaciones.append(
            {
                "texto": "Las zonas verdes son bajas. Plantar árboles ayudaría.",
                "clase": "moderado",
            }
        )

    if inputs["cobertura_arbolado_pct"] < 10:
        recomendaciones.append(
            {
                "texto": "Cobertura arbórea muy baja. Urgente reforestación.",
                "clase": "critico",
            }
        )
    elif inputs["cobertura_arbolado_pct"] < 20:
        recomendaciones.append(
            {
                "texto": "Aumentar árboles mejoraría la calidad ambiental.",
                "clase": "moderado",
            }
        )

    if inputs["pm25"] > 40:
        recomendaciones.append(
            {
                "texto": "PM2.5 extremadamente alto. Revisar fuentes de contaminación.",
                "clase": "critico",
            }
        )
    elif inputs["pm25"] > 25:
        recomendaciones.append(
            {"texto": "PM2.5 elevado. Reducir emisiones ayudaría.", "clase": "moderado"}
        )

    if inputs["pm10"] > 60:
        recomendaciones.append(
            {
                "texto": "PM10 elevado. Revisar fuentes de partículas.",
                "clase": "moderado",
            }
        )

    if inputs["residuos_no_gestionados"] > 0.7:
        recomendaciones.append(
            {
                "texto": "Muchos residuos sin gestionar. Mejorar manejo de basuras.",
                "clase": "critico",
            }
        )
    elif inputs["residuos_no_gestionados"] > 0.3:
        recomendaciones.append(
            {"texto": "Manejo de residuos mejorable.", "clase": "moderado"}
        )

    if inputs["porcentaje_reciclaje"] < 10:
        recomendaciones.append(
            {
                "texto": "Reciclaje muy bajo. Incrementarlo ayudaría mucho.",
                "clase": "critico",
            }
        )
    elif inputs["porcentaje_reciclaje"] < 25:
        recomendaciones.append(
            {"texto": "Se puede mejorar el reciclaje.", "clase": "moderado"}
        )

    if inputs["porcentaje_transporte_limpio"] < 10:
        recomendaciones.append(
            {
                "texto": "Muy poco transporte limpio. Fomentar medios sostenibles.",
                "clase": "critico",
            }
        )
    elif inputs["porcentaje_transporte_limpio"] < 25:
        recomendaciones.append(
            {
                "texto": "Incrementar transporte limpio sería beneficioso.",
                "clase": "moderado",
            }
        )

    return recomendaciones


# ===== RUTAS WEB =====


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    inputs = {}

    # ===== LEER DATOS DEL FORM =====
    for feat in FEATURE_ORDER:
        raw = request.form.get(feat)
        if not raw:
            return render_template("index.html", error=f"Falta valor para {feat}")
        try:
            inputs[feat] = float(raw)
        except:
            return render_template("index.html", error=f"Valor inválido para {feat}")

    # ===== NORMALIZAR =====
    x_norm = [normalize_feature(f, inputs[f]) for f in FEATURE_ORDER]
    X = np.array([x_norm])

    # ===== PREDECIR =====
    pred = model.predict(X)[0]
    pred_rounded = round(float(pred), 3)

    # ===== CATEGORÍA =====
    if pred_rounded >= 450:
        cat = "Excelente"
    elif pred_rounded >= 350:
        cat = "Bueno"
    elif pred_rounded >= 200:
        cat = "Moderado"
    else:
        cat = "Crítico"

    # ===== GENERAR RECOMENDACIONES =====
    recomendaciones = generar_recomendaciones(inputs, pred_rounded)

    # ===== GUARDAR EN BD =====
    db = SessionLocal()
    registro = Prediccion(**inputs, ecoscore=pred_rounded)
    db.add(registro)
    db.commit()
    db.close()

    # ===== RENDER =====
    return render_template(
        "index.html",
        prediction=pred_rounded,
        category=cat,
        inputs=inputs,
        recomendaciones=recomendaciones,
    )


# ===== API PARA EL DASHBOARD =====


@app.route("/api/historico")
def api_historico():
    limit = int(request.args.get("limit", 20))
    db = SessionLocal()
    rows = db.query(Prediccion).order_by(Prediccion.id.desc()).limit(limit).all()
    db.close()

    data = [
        {
            "id": r.id,
            "ecoscore": r.ecoscore,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for r in rows
    ]

    return {"historico": data}


@app.route("/api/ultimo")
def api_ultimo():
    db = SessionLocal()
    row = db.query(Prediccion).order_by(Prediccion.id.desc()).first()
    db.close()

    if not row:
        return {"status": "sin_datos"}

    return {
        "id": row.id,
        "ecoscore": row.ecoscore,
        "timestamp": row.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ===== MAIN =====
if __name__ == "__main__":
    init_db()
    iniciar_simulador_sensores()
    app.run(debug=True)
