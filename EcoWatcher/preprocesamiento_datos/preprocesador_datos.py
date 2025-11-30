import pandas as pd
import numpy as np
import os
import json

# ===== RUTAS =====
INPUT_PATH = "EcoWatcher/data/dataset_mejorado.csv"
OUTPUT_PATH = "EcoWatcher/data/bogota_procesado.csv"
PARAMS_PATH = "EcoWatcher/preprocesamiento_datos/parametros_normalizados.json"


NUMERIC_COLUMNS = [
    "ha_verdes_km2",
    "cobertura_arbolado_pct",
    "pm25",
    "pm10",
    "residuos_no_gestionados",
    "porcentaje_reciclaje",
    "porcentaje_transporte_limpio",
]

# ===== PESOS (suman 1.0) =====
ECO_WEIGHTS = {
    "ha_verdes_km2": 0.18,
    "cobertura_arbolado_pct": 0.15,
    "pm25": 0.22,
    "pm10": 0.08,
    "residuos_no_gestionados": 0.12,
    "porcentaje_reciclaje": 0.12,
    "porcentaje_transporte_limpio": 0.13,
}

NORMALIZATION_METHOD = "minmax"


def ensure_dirs():
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(PARAMS_PATH) or ".", exist_ok=True)


def load_raw(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    df = pd.read_csv(path)
    return df


def clean_numeric_columns(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".", regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            print(f"Advertencia: columna faltante -> {col}")
            df[col] = np.nan
    return df


def impute_missing(df, cols, strategy="median"):
    for col in cols:
        if col in df.columns:
            if df[col].isnull().any():
                val = df[col].median() if strategy == "median" else df[col].mean()
                df[col].fillna(val, inplace=True)
    return df


def normalize_minmax(series, vmin=None, vmax=None):
    if vmin is None:
        vmin = series.min()
    if vmax is None:
        vmax = series.max()
    if vmax == vmin:
        return series.apply(lambda x: 0.5), vmin, vmax
    normalized = (series - vmin) / (vmax - vmin)
    return normalized, vmin, vmax


def normalize_percentile(series, low=1, high=99):
    arr = series.dropna().values
    if len(arr) == 0:
        return series.apply(lambda x: 0.5), None, None
    p_low = np.percentile(arr, low)
    p_high = np.percentile(arr, high)
    if p_high == p_low:
        return series.apply(lambda x: 0.5), p_low, p_high
    clipped = series.clip(lower=p_low, upper=p_high)
    normalized = (clipped - p_low) / (p_high - p_low)
    return normalized, p_low, p_high


def compute_ecoscore_0_500(df, weights):
    # espera columnas {feature}_norm ya creadas
    score = np.zeros(len(df))
    for feature, w in weights.items():
        norm_col = f"{feature}_norm"
        if norm_col not in df.columns:
            raise KeyError(f"Falta {norm_col}")
        # invertir para "más es peor"
        if feature in ["pm25", "pm10", "residuos_no_gestionados"]:
            contrib = (1 - df[norm_col]) * w
        else:
            contrib = df[norm_col] * w
        score += contrib
    # mapear a 0-500
    score_0_500 = (score * 500).clip(0, 500)
    return score_0_500


def main():
    ensure_dirs()
    df = load_raw(INPUT_PATH)
    df = clean_numeric_columns(df, NUMERIC_COLUMNS)
    df = impute_missing(df, NUMERIC_COLUMNS, strategy="median")

    params = {"method": NORMALIZATION_METHOD, "columns": {}}
    for col in NUMERIC_COLUMNS:
        if NORMALIZATION_METHOD == "minmax":
            normalized, vmin, vmax = normalize_minmax(df[col])
            df[f"{col}_norm"] = normalized
            params["columns"][col] = {
                "vmin": None if vmin is None else float(vmin),
                "vmax": None if vmax is None else float(vmax),
            }
        else:
            normalized, p_low, p_high = normalize_percentile(df[col], low=1, high=99)
            df[f"{col}_norm"] = normalized
            params["columns"][col] = {
                "p_low": None if p_low is None else float(p_low),
                "p_high": None if p_high is None else float(p_high),
            }

    df["ecoscore_0_500"] = compute_ecoscore_0_500(df, ECO_WEIGHTS)

    def category_from_score_500(s):
        if s >= 450:
            return "Excelente"
        if s >= 350:
            return "Bueno"
        if s >= 200:
            return "Moderado"
        return "Crítico"

    df["ecoscore_category"] = df["ecoscore_0_500"].apply(category_from_score_500)

    print("\nResumen (primeras filas):")
    print(df.head(6))

    with open(PARAMS_PATH, "w") as f:
        json.dump(params, f, indent=2)

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nProcesado guardado en: {OUTPUT_PATH}")
    print(f"Parámetros guardados en: {PARAMS_PATH}")


if __name__ == "__main__":
    main()
