from libs import time

# Debug helper
def debug(msg, data=None):
    print(f"[DEBUG] {time.strftime('%H:%M:%S')} - {msg}")
    if data is not None:
        print(f"        → {data}")