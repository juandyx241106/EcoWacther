from flask import Blueprint, render_template, request, redirect, url_for, session
import numpy as np
from database.db import SessionLocal
from database.modelodb import Prediccion
from config import FEATURE_ORDER
from utils.normalizacion import normalize_feature
from utils.recomendaciones import generar_recomendaciones

predicciones = Blueprint('predicciones', __name__)

# Este será importado desde app.py
model = None


def set_model(ml_model):
    """Establecer el modelo de ML globalmente."""
    global model
    model = ml_model


@predicciones.route("/", methods=["GET"])
def index():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("index.html")


@predicciones.route("/predict", methods=["POST"])
def predict():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    
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


@predicciones.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    
    return render_template("dashboard.html")
