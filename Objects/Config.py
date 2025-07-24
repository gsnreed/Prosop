# --- Konstanten und Konfiguration ---
class AppConfig:
    """Zentrale Konfigurationsklasse für die Anwendung"""
    # Fensterkonfiguration
    APP_TITLE = 'Prosop'
    WINDOW_SIZE = "1200x800"
    
    # Dateipfade
    APP_ICON = './Pictures/KULogo.png'
    UNIVERSITY_LOGO = './Pictures/KU.png'
    LOG_DIR = './Log'
    LOG_FILE = './Log/log.log'
    
    # Anwendungstexte
    MAIN_TITLE = 'Prosopographie der Julisch-Claudischen Kaiserzeit'
    NAVIGATION_TITLE = 'Navigation'
    NAV_OPTIONS = ['Startseite', 'Ansicht', 'Erstellung', 'Statistik', 
                  'Import', 'Export', 'BibTex', 'Hilfe', 'Impressum']

class AppColors:
    """Farbschema der Anwendung"""
    SELECTION_BAR = '#eff5f6'
    TOP_FRAME = '#F5E1FD'
    SIDEBAR_FRAME = "#EEC6FF"
    SUBMENU_FRAME = "#F1D0FF"
    HEADER = '#53366b'
    CONTENT_FRAME = "#ffffff"
    KU_COLOR = '#232F66'
    HOVER = "#D9A7FC"