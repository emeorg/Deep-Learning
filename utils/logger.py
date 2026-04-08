from libs import *
from utils.helpers import info, success, error, warning

LOG_PATH = "outputs/logs/"

def asegurar_directorio_logs():
    """Asegura que la carpeta de logs exista."""
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

def log_dict_to_excel(data: dict, filename="log.xlsx", sheet="Sheet1"):
    """Guarda un diccionario de metadatos en un archivo Excel persistente."""
    asegurar_directorio_logs()
    path = os.path.join(LOG_PATH, filename)
    
    df = pd.DataFrame([data])

    if os.path.exists(path):
        try:
            existing = pd.read_excel(path)
            df = pd.concat([existing, df], ignore_index=True)
        except Exception as e:
            warning(f"No se pudo anexar al log existente, creando uno nuevo. ({e})")

    df.to_excel(path, index=False)
    success(f"Log guardado en {path}")

def log_training_history(history):
    """Guarda el historial de entrenamiento de Keras."""
    asegurar_directorio_logs()
    df = pd.DataFrame(history.history)
    path = os.path.join(LOG_PATH, "training_log.xlsx")

    if os.path.exists(path):
        existing = pd.read_excel(path)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_excel(path, index=False)
    success("Metadatos de entrenamiento guardados.")

def log_model_summary(model):
    """Exporta el resumen de la arquitectura del modelo a Excel."""
    asegurar_directorio_logs()
    summary_list = []
    model.summary(print_fn=lambda x: summary_list.append(x))
    
    df = pd.DataFrame({"arquitectura_detallada": summary_list})
    path = os.path.join(LOG_PATH, "model_summary.xlsx")
    
    try:
        df.to_excel(path, index=False)
        success(f"Resumen del modelo guardado en {path}")
    except Exception as e:
        error("Error al guardar el resumen del modelo", exc=e)