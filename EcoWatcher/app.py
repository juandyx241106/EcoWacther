import os
from pathlib import Path
from flask import Flask
from joblib import load

# ===== IMPORTAR CONFIGURACIÓN =====
from config import BASE_DIR, MODEL_PATH, SECRET_KEY, DEBUG

# ===== IMPORTAR BASES DE DATOS =====
from database.db import init_db
from database.usuarios import init_db as init_db_usuarios

# ===== IMPORTAR BLUEPRINTS =====
from routes.auth import auth
from routes.predicciones import predicciones, set_model
from routes.api import api

# ===== IMPORTAR SENSOR =====
from sensor.simulador import iniciar_simulador_sensores


# ===== INICIALIZAR APP =====
app = Flask(__name__)
app.secret_key = SECRET_KEY

# ===== INICIALIZAR BASES DE DATOS =====
init_db()
init_db_usuarios()

# ===== CARGAR MODELO ML =====
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Modelo no encontrado en: {MODEL_PATH}")
model = load(MODEL_PATH)
set_model(model)  # Establecer el modelo globalmente en el blueprint

# ===== REGISTRAR BLUEPRINTS =====
app.register_blueprint(auth)
app.register_blueprint(predicciones)
app.register_blueprint(api)


# ===== MAIN =====
if __name__ == "__main__":
    iniciar_simulador_sensores()
    app.run(debug=DEBUG)
