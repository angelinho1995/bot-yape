# modules/logger.py

import os
from datetime import datetime

LOG_DIR = "logs"

# Asegura que exista la carpeta logs
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def save_log(module_name, content):
    """Guarda los resultados de cada módulo en archivos separados."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{LOG_DIR}/{module_name}_{timestamp}.log"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename  # Devuelve la ruta para enviar por el bot si quieres
    except Exception as e:
        return f"❌ Error al guardar log: {str(e)}"
