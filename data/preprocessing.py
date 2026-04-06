from libs import *
from utils.helpers import debug
from utils.logger import log_dict_to_excel

def preprocess_data():
    debug("=== INICIO PREPROCESAMIENTO ===")

    path = "outputs/datasets/big_dataset.csv"

    # -------------------------
    # Validación de archivo
    # -------------------------
    if not os.path.exists(path):
        debug("ERROR: Dataset no encontrado")
        return

    df = pd.read_csv(path)

    debug("Dataset cargado", df.shape)

    # -------------------------
    # Feature Engineering 🔥
    # -------------------------
    debug("Creando nuevas features...")

    if "dew_point_2m" in df.columns:
        df["temp_range"] = df["temperature_2m"] - df["dew_point_2m"]

    if "windspeed_10m" in df.columns and "cloudcover" in df.columns:
        df["wind_effect"] = df["windspeed_10m"] * df["cloudcover"]

    debug("Features nuevas agregadas", df.columns.tolist())

    # -------------------------
    # Target (clasificación binaria)
    # -------------------------
    debug("Creando variable objetivo (target)")

    if "rain" not in df.columns:
        debug("ERROR: columna 'rain' no encontrada")
        return

    df["target"] = (df["rain"] > 0).astype(int)

    # -------------------------
    # Análisis básico 🔥 (MUY IMPORTANTE)
    # -------------------------
    debug("Distribución del target")
    debug("Balance de clases", df["target"].value_counts(normalize=True))

    debug("Correlaciones (top 5)")
    try:
        debug("Correlación (sample)")
        debug(df.sample(10000).corr(numeric_only=True))
    except:
        debug("No se pudo calcular correlación")

    # -------------------------
    # Separación X / y
    # -------------------------
    debug("Separando features y target")

    X = df.drop(columns=["target", "time"], errors='ignore')
    y = df["target"]

    debug("Shape X", X.shape)
    debug("Shape y", y.shape)

    # -------------------------
    # Normalización (IMPORTANTE EN DL)
    # -------------------------
    debug("Normalizando datos")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # -------------------------
    # Split Train / Val / Test
    # -------------------------
    debug("Dividiendo dataset")

    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )

    debug("Train shape", X_train.shape)
    debug("Validation shape", X_val.shape)
    debug("Test shape", X_test.shape)

    debug("Ejemplo datos procesados", X_train[:2])
    debug("=== PREPROCESAMIENTO COMPLETO ===")

    log_data = {
    "n_samples": len(df),
    "n_features": X.shape[1],
    "train_size": X_train.shape[0],
    "val_size": X_val.shape[0],
    "test_size": X_test.shape[0],
    "target_balance_0": (y == 0).mean(),
    "target_balance_1": (y == 1).mean()
    }

    log_dict_to_excel(log_data, filename="preprocessing_log.xlsx")

    return X_train, X_val, X_test, y_train, y_val, y_test