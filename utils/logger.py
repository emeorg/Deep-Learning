from libs import *
from utils.helpers import debug

LOG_PATH = "outputs/logs/"

def ensure_log_dir():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)


def log_dict_to_excel(data: dict, filename="log.xlsx", sheet="Sheet1"):
    ensure_log_dir()

    path = os.path.join(LOG_PATH, filename)

    df = pd.DataFrame([data])

    if os.path.exists(path):
        existing = pd.read_excel(path)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_excel(path, index=False)

    debug(f"Log guardado en {path}")

def log_training_history(history):
    ensure_log_dir()

    df = pd.DataFrame(history.history)

    path = os.path.join(LOG_PATH, "training_log.xlsx")

    if os.path.exists(path):
        existing = pd.read_excel(path)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_excel(path, index=False)

    debug("Training log guardado")

def log_model_summary(model):
    ensure_log_dir()

    summary_list = []

    model.summary(print_fn=lambda x: summary_list.append(x))

    df = pd.DataFrame({"summary": summary_list})

    path = os.path.join(LOG_PATH, "model_summary.xlsx")
    df.to_excel(path, index=False)

    debug("Model summary guardado")