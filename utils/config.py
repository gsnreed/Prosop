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
    LOG_FILE = './utils/log.log'
    
    # Anwendungstexte
    MAIN_TITLE = 'Prosopographie der Julisch-Claudischen Kaiserzeit'
    NAVIGATION_TITLE = 'Navigation'
    NAV_OPTIONS = ['Startseite', 'Ansicht', 'Erstellung', 'Statistik',
                    'BibTex', 'Hilfe', 'Impressum']
    SUBMENUS = {
            'Ansicht': ['Tabelle', 'Karte', 'Zeitstrahl'],
            'BibTex': ['Literatur hinzufügen', 'Zitieren', 'Verwalten']
        }

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

class Fonts:
    """Schriftgrößen/-arten"""
    LOADING_SCREEN = ("Helvetica", 12)
    STANDARD = ("Helvetica", 12)
    STANDARD_BOLD = ("Helvetica", 12, 'bold')
    HEADER = ('Helvetica', 15, 'bold')
    CLOCK = ('Helvetica', 15)
    SUBMENU = ("Helvetica", 11)
    SUBMENU_BOLD = ("Helvetica", 11, 'bold')
    DEFAULT_FRAME = ('Helvetica', 18, 'bold')