# Objects/Logger.py
import logging
import os
import sys
import traceback

# Projektverzeichnis zum Suchpfad hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Absoluter Import
from utils.config import AppConfig

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def setup_logging():
    """Richtet das Logging-System ein"""
    try:
        # Absoluter Pfad für das Log-Verzeichnis (immer im echten Dateisystem)
        log_dir = os.path.abspath(AppConfig.LOG_DIR)
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, os.path.basename(AppConfig.LOG_FILE))
        
        logging.basicConfig(
            filename=log_file,
            encoding='utf-8',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S',
            force=True
        )
        
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
        logger = logging.getLogger(__name__)
        return logger
        
    except Exception as e:
        print(f"FEHLER beim Einrichten des Loggers: {e}")
        print(traceback.format_exc())
        fallback_logger = logging.getLogger("fallback")
        fallback_logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('FALLBACK: %(asctime)s - %(message)s'))
        fallback_logger.addHandler(handler)
        fallback_logger.info("Fallback-Logger wird verwendet (keine Dateien)")
        return fallback_logger


# Logger initialisieren
logger = setup_logging()