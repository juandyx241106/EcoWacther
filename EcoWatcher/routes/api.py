from flask import Blueprint, request, jsonify
from database.db import SessionLocal
from database.modelodb import Prediccion

api = Blueprint('api', __name__, url_prefix='/api')


@api.route("/historico")
def historico():
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

    return jsonify({"historico": data})


@api.route("/ultimo")
def ultimo():
    db = SessionLocal()
    row = db.query(Prediccion).order_by(Prediccion.id.desc()).first()
    db.close()

    if not row:
        return jsonify({"status": "sin_datos"})

    return jsonify({
        "id": row.id,
        "ecoscore": row.ecoscore,
        "timestamp": row.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
    })
