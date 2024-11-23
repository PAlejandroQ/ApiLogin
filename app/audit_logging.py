import logging
import os
from datetime import datetime

# Configuración del archivo de logs
def setup_log():
    LOG_DIR = "logs"
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    LOG_FILE = os.path.join(LOG_DIR, f"audit_{datetime.now().strftime('%Y-%m-%d')}.log")

    # Configurar el logger
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    print("LOG FILE CREATED")

# Función para registrar eventos
def log_event(level, message):
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)
    else:
        logging.debug(message)
