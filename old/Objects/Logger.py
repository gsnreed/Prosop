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
from Objects.Config import AppConfig

def setup_logging():
    """Richtet das Logging-System ein"""
    try:
        # Stelle sicher, dass das Log-Verzeichnis existiert
        os.makedirs(AppConfig.LOG_DIR, exist_ok=True)
        
        # Konfiguriere das Root-Logger
        logging.basicConfig(
            filename=AppConfig.LOG_FILE,
            encoding='utf-8',  # UTF-8 für Umlaute
            level=logging.INFO,  # Setze auf INFO statt NOTSET
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S',
            force=True  # Erzwinge die Konfiguration, überschreibe bestehende
        )
        
        # Erstelle einen zusätzlichen Konsolen-Logger für direkte Ausgabe
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
        # Teste den Logger sofort
        logger = logging.getLogger(__name__)
        logger.info("Logger erfolgreich initialisiert")
        
        # Prüfe, ob die Datei wirklich beschreibbar ist
        with open(AppConfig.LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"Manuelle Log-Prüfung: {logger.name} ist bereit.\n")
        
        return logger
        
    except Exception as e:
        # Im Fehlerfall, schreibe auf die Konsole
        print(f"FEHLER beim Einrichten des Loggers: {e}")
        print(traceback.format_exc())
        
        # Erstelle einen einfachen Konsolen-Logger als Fallback
        fallback_logger = logging.getLogger("fallback")
        fallback_logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('FALLBACK: %(asctime)s - %(message)s'))
        fallback_logger.addHandler(handler)
        
        fallback_logger.info("Fallback-Logger wird verwendet (keine Dateien)")
        return fallback_logger

# Logger initialisieren
logger = setup_logging()

# Prüfe sofort
if __name__ == "__main__":
    logger.info("Test-Log mit Umlauten: äöüÄÖÜß")
    print(f"Log-Datei sollte hier sein: {os.path.abspath(AppConfig.LOG_FILE)}")