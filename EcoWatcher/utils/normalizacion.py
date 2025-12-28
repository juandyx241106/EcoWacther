import json
from pathlib import Path
from config import PARAMS_PATH


# ===== CARGAR PARÁMETROS DE NORMALIZACIÓN =====
with open(PARAMS_PATH, "r") as f:
    norm_params = json.load(f)


def apply_minmax(value, vmin, vmax):
    """Normalización MinMax."""
    if vmin is None or vmax is None or vmax == vmin:
        return 0.5
    return float((value - vmin) / (vmax - vmin))


def normalize_feature(name, raw_value):
    """Normalizar una feature según los parámetros guardados."""
    method = norm_params.get("method", "minmax")
    colparams = norm_params.get("columns", {}).get(name, {})
    x = float(raw_value)

    if method == "minmax":
        return apply_minmax(x, colparams.get("vmin"), colparams.get("vmax"))

    return 0.5  # fallback seguro
