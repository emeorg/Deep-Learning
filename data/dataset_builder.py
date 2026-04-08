from libs import *
from utils.helpers import info, success, warning, error
from utils.logger import log_dict_to_excel

def cargar_datos_brutos(ruta):
    """Carga el dataset de Clima Crudo desde la ruta especificada."""
    if not os.path.exists(ruta):
        error(f"Archivo base NO existe en {ruta}")
        return None
    
    info(f"Cargando dataset base desde {ruta}...")
    df = pd.read_csv(ruta)
    info(f"Dataset cargado -> Dimensiones iniciales: {df.shape}")
    return df

def limpiar_datos(df):
    """Realiza la limpieza básica de nulos."""
    inicial = len(df)
    df = df.dropna()
    final = len(df)
    
    eliminados = inicial - final
    if eliminados > 0:
        warning(f"Limpieza completada: Se eliminaron {eliminados} filas con nulos.")
    else:
        success("Limpieza completada: No se encontraron valores nulos.")
    return df

def crear_columna_objetivo(df, columna_lluvia="rain"):
    """
    Crea el 'target' binario (1 si llueve, 0 si no).
    Muestra el desbalance de clases para auditoría.
    """
    if columna_lluvia not in df.columns:
        error(f"Falta columna crítica '{columna_lluvia}' para generar el target.")
        return df

    info("Generando columna objetivo (target)...")
    df["target"] = (df[columna_lluvia] > 0).astype(int)
    
    distribucion = df["target"].value_counts(normalize=True).to_dict()
    info(f"Distribución de clases -> {distribucion}")
    return df

def guardar_dataset(df, ruta):
    """Guarda el resultado final en formato CSV."""
    info(f"Guardando dataset final en {ruta}...")
    df.to_csv(ruta, index=False)
    success(f"Dataset guardado exitosamente: {df.shape}")

def registrar_metadatos(df):
    """Guarda resumen estadístico en archivo Excel log."""
    log_data = {
        "timestamp": pd.Timestamp.now(),
        "rows": len(df),
        "features": df.shape[1],
        "cities": df["city"].nunique()
    }
    log_dict_to_excel(log_data, filename="dataset_log.xlsx")
    info("Metadatos del dataset registrados en log Excel.")

def construir_dataset():
    """Función orquestadora de la construcción del dataset."""
    info("=== INICIANDO CONSTRUCCIÓN DEL DATASET FINAL ===")
    
    ruta_raw = "outputs/datasets/raw_weather_multi.csv"
    ruta_final = "outputs/datasets/big_dataset.csv"

    # Pipeline de ejecución
    df = cargar_datos_brutos(ruta_raw)
    if df is not None:
        df = limpiar_datos(df)
        df = crear_columna_objetivo(df)
        guardar_dataset(df, ruta_final)
        registrar_metadatos(df)
        success("¡Pipeline de dataset completado!")

# Alias para compatibilidad con cuadernos previos
def build_dataset():
    construir_dataset()
