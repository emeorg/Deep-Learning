from libs import *
from utils.helpers import info, success, warning, error
from utils.logger import log_dict_to_excel

def cargar_dataset_consolidado(ruta):
    """Carga el dataset generado en la etapa anterior."""
    if not os.path.exists(ruta):
        error(f"Dataset no encontrado en {ruta}. ¿Ejecutaste construir_dataset()?")
        return None
    
    info(f"Cargando dataset consolidado desde {ruta}...")
    df = pd.read_csv(ruta)
    info(f"Dataset cargado -> {df.shape}")
    return df

def generar_caracteristicas(df):
    """Ejecuta ingeniería de variables para enriquecer el dataset."""
    info("Generando nuevas características (Feature Engineering)...")
    
    # Amplitud térmica
    if "temperature_2m" in df.columns and "dew_point_2m" in df.columns:
        df["temp_range"] = df["temperature_2m"] - df["dew_point_2m"]
    
    # Interacción Viento-Nubes
    if "windspeed_10m" in df.columns and "cloudcover" in df.columns:
        df["wind_effect"] = df["windspeed_10m"] * df["cloudcover"]
        
    success("Ingeniería de características completada.")
    return df

def preparar_variables_y_target(df):
    """
    Separa las características (X) de la etiqueta objetivo (y).
    
    --- ✅ DATA LEAKAGE CORREGIDO ✅ ---
    Se eliminan las columnas que contienen información directa sobre la lluvia.
    Esto permite que el modelo aprenda a predecir basándose solo en 
    variables ambientales indirectas.
    """
    info("Preparando matrices X (features) e y (target)...")
    
    # El target ya viene pre-calculado de la etapa anterior
    y = df["target"]
    
    # CORRECCIÓN: Eliminamos el target y las variables que causan filtración de datos.
    X = df.drop(columns=[
        "target", "time", "city", 
        "rain", "precipitation", "snowfall"
    ], errors='ignore')
    
    success("Matrices preparadas - Data Leakage eliminado satisfactoriamente.")
    return X, y

def escalar_datos(X):
    """Normaliza las características usando StandardScaler."""
    info("Escalando datos con StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    success("Normalización completada.")
    return X_scaled

def dividir_dataset(X, y):
    """Divide los datos en conjuntos de Entrenamiento, Validación y Prueba."""
    info("Dividiendo dataset en Train (80%), Val (10%) y Test (10%)...")
    
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )
    
    info(f"Train: {X_train.shape} | Val: {X_val.shape} | Test: {X_test.shape}")
    return X_train, X_val, X_test, y_train, y_val, y_test

def registrar_metricas_preprocesamiento(df, X_train, X_val, X_test, y):
    """Guarda metadatos del preprocesamiento en Excel."""
    log_data = {
        "timestamp": pd.Timestamp.now(),
        "total_samples": len(df),
        "features_finales": X_train.shape[1],
        "train_size": X_train.shape[0],
        "val_size": X_val.shape[0],
        "test_size": X_test.shape[0],
        "balance_clases": (y == 1).mean()
    }
    log_dict_to_excel(log_data, filename="preprocessing_log.xlsx")
    info("Metadatos de preprocesamiento registrados.")

def preprocesar_datos():
    """Función orquestadora del preprocesamiento."""
    info("=== INICIANDO PIPELINE DE PREPROCESAMIENTO ===")
    
    ruta_dataset = "outputs/datasets/big_dataset.csv"
    
    df = cargar_dataset_consolidado(ruta_dataset)
    if df is not None:
        df = generar_caracteristicas(df)
        X, y = preparar_variables_y_target(df)
        
        # Nota: Por ahora escalamos DESPUÉS de separar pero ANTES de dividir
        X_scaled = escalar_datos(X)
        
        X_train, X_val, X_test, y_train, y_val, y_test = dividir_dataset(X_scaled, y)
        
        registrar_metricas_preprocesamiento(df, X_train, X_val, X_test, y)
        
        success("¡Pipeline de preprocesamiento completado!")
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    return None, None, None, None, None, None

# Alias para compatibilidad con cuadernos previos
def preprocess_data():
    return preprocesar_datos()