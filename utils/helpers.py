from libs import time

# === HELPERS DE LOGGING ===

def debug(msg, data=None):
    """Log detallado para depuración"""
    print(f"[DEBUG] {time.strftime('%H:%M:%S')} - {msg}")
    if data is not None:
        print(f"        → {data}")

def info(msg):
    """Log informativo de flujo"""
    print(f"[INFO] {time.strftime('%H:%M:%S')} - {msg}")

def success(msg):
    """Log de operaciones completadas con éxito"""
    print(f"[SUCCESS] {time.strftime('%H:%M:%S')} - ✅ {msg}")

def warning(msg):
    """Log de advertencias o reintentos"""
    print(f"[WARNING] {time.strftime('%H:%M:%S')} - ⚠️ {msg}")

def error(msg, exc=None):
    """Log de errores críticos"""
    print(f"[ERROR] {time.strftime('%H:%M:%S')} - ❌ {msg}")
    if exc:
        print(f"        → Detalle: {exc}")