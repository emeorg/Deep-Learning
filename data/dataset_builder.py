from libs import *
from utils.helpers import debug
from utils.logger import log_dict_to_excel

def build_dataset():

    debug("=== CONSTRUCCIÓN DATASET FINAL ===")

    path = "outputs/datasets/raw_weather_multi.csv"

    if not os.path.exists(path):
        debug("Archivo base NO existe")
        return

    df = pd.read_csv(path)

    debug(f"Dataset cargado: {df.shape}")

    # 🔥 LIMPIEZA
    df = df.dropna()

    debug(f"Después de dropna: {df.shape}")

    # 🔥 crear target
    df["target"] = (df["rain"] > 0).astype(int)

    # 🔥 validación básica
    debug("Distribución target:")
    debug(df["target"].value_counts(normalize=True))

    output_path = "outputs/datasets/big_dataset.csv"
    df.to_csv(output_path, index=False)

    # 🔥 LOG
    log_data = {
        "rows": len(df),
        "features": df.shape[1],
        "cities": df["city"].nunique()
    }

    log_dict_to_excel(log_data, filename="dataset_log.xlsx")

    debug("Resumen final:")
    debug("Filas", len(df))
    debug("Columnas", df.shape[1])
    debug("Ciudades", df["city"].nunique())

    debug(f"Dataset guardado en {output_path}")