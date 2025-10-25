import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Konstanten und Konfiguration ---
class AppConfig:
    """Zentrale Konfigurationsklasse für die Anwendung"""
    # Fensterkonfiguration
    APP_TITLE = 'Prosop'
    WINDOW_SIZE = "1200x800"
    MIN_WINDOW_SIZE = "1000x600"
    
    # Dateipfade
    APP_ICON = resource_path('KULogo.png')
    UNIVERSITY_LOGO = resource_path('KU.png')
    LOG_DIR = resource_path('Log')
    LOG_FILE = resource_path('utils/log.log')
    
    # Anwendungstexte
    MAIN_TITLE = 'Prosopographie der Julisch-Claudischen Kaiserzeit'
    NAVIGATION_TITLE = 'Navigation'
    NAV_OPTIONS = ['Startseite', 'Ansicht', 'Erstellung', 'Statistik',
                    'BibTex', 'Hilfe', 'Impressum']
    SUBMENUS = {
        'Ansicht': ['Tabelle', 'Karte', 'Zeitstrahl \n- Überblick', 'Zeitstrahl \n- Detail'],
        'BibTex': ['Literatur hinzufügen', 'Zitieren', 'Verwalten']
    }
    
    # UI-Konfiguration
    ANIMATION_DURATION = 200  # ms
    TOOLTIP_DELAY = 500  # ms
    AUTOSAVE_INTERVAL = 300000  # 5 Minuten
    SEARCH_DELAY = 300  # ms für Live-Suche

class TimelineConfig:
    """Timeline-spezifische Konfigurationen"""
    # Standard-Zeitbereiche
    DEFAULT_START_YEAR = -100
    DEFAULT_END_YEAR = 500
    MIN_YEAR = -500  # 100 v.Chr.
    MAX_YEAR = 600   # 600 n.Chr.
    
    # Zoom-Einstellungen
    MIN_ZOOM_SPAN = 1     # Minimum: 1 Jahr
    MAX_ZOOM_SPAN = 1000  # Maximum: 1000 Jahre
    DEFAULT_ZOOM_SPAN = 100
    ZOOM_FACTOR = 1.5
    ZOOM_SENSITIVITY = 0.1
    PAN_SENSITIVITY = 10
    SMOOTH_SCROLL_STEPS = 5
    
    # Visualisierung
    PERSON_HEIGHT = 35
    TIMELINE_MARGIN = 20
    SCALE_HEIGHT = 50
    MIN_PERSON_WIDTH = 200
    PERSON_ENTRY_HEIGHT = 35
    SCALE_LABEL_WIDTH = 80
    
    # Performance
    MAX_VISIBLE_PERSONS = 1000
    LAZY_LOAD_THRESHOLD = 100
    UPDATE_DEBOUNCE_MS = 300
    
    # Intervalle für Zeitskala
    SCALE_INTERVALS = {
        (1, 10): 1,
        (11, 50): 5,
        (51, 100): 10,
        (101, 200): 25,
        (201, 500): 50,
        (501, 1000): 100
    }

class ViewModes:
    """Verschiedene Ansichtsmodi für Timeline"""
    
    COMPACT = {
        'person_height': 25,
        'show_details': False,
        'max_name_length': 20,
        'show_portraits': False
    }
    
    NORMAL = {
        'person_height': 35,
        'show_details': True,
        'max_name_length': 30,
        'show_portraits': False
    }
    
    DETAILED = {
        'person_height': 50,
        'show_details': True,
        'max_name_length': 50,
        'show_portraits': True
    }

class AppColors:
    """Erweitertes Farbschema der Anwendung"""
    # Basis-Farben (Original)
    SELECTION_BAR = '#eff5f6'
    TOP_FRAME = '#F5E1FD'
    SIDEBAR_FRAME = "#EEC6FF"
    SUBMENU_FRAME = "#F1D0FF"
    HEADER = '#53366b'
    CONTENT_FRAME = "#ffffff"
    KU_COLOR = '#232F66'
    HOVER = "#D9A7FC"
    HIGHLIGHT = "#D9A7FC"
    
    # Hintergründe
    BACKGROUND = "#f8f9fa"
    BACKGROUND_DARK = "#e9ecef"
    HEADER_BG = "#ffffff"
    HEADER_FG = '#232F66'
    DETAIL_HEADER_BG = "#f8f9fa"
    DETAIL_HEADER_FG = '#232F66'
    
    # Suchfeld
    SEARCH_BG = "#f1f3f5"
    SEARCH_FG = '#495057'
    SEARCH_PLACEHOLDER = '#adb5bd'
    SEARCH_FOCUS_BG = "#ffffff"
    SEARCH_FOCUS_BORDER = "#232F66"
    
    # Tabelle
    TABLE_BG = "#ffffff"
    TABLE_FG = '#212529'
    TABLE_HEADER_BG = "#232F66"
    TABLE_HEADER_FG = "#ffffff"
    TABLE_SELECTED_BG = "#D9A7FC"
    TABLE_SELECTED_FG = '#232F66'
    TABLE_HOVER_BG = "#f1f3f5"
    TABLE_ALTERNATE_BG = "#f8f9fa"
    TABLE_BORDER = "#dee2e6"
    
    # Buttons
    BUTTON_PRIMARY = "#232F66"
    BUTTON_PRIMARY_BG = "#232F66"
    BUTTON_PRIMARY_FG = "#ffffff"
    BUTTON_PRIMARY_HOVER = "#1a2451"
    BUTTON_PRIMARY_ACTIVE = "#141b3d"
    
    BUTTON_SECONDARY_BG = "#6c757d"
    BUTTON_SECONDARY_FG = "#ffffff"
    BUTTON_SECONDARY_HOVER = "#5a6268"
    BUTTON_SECONDARY_ACTIVE = "#545b62"
    
    BUTTON_SUCCESS_BG = "#28a745"
    BUTTON_SUCCESS_FG = "#ffffff"
    BUTTON_SUCCESS_HOVER = "#218838"
    BUTTON_SUCCESS_ACTIVE = "#1e7e34"
    
    BUTTON_DANGER_BG = "#dc3545"
    BUTTON_DANGER_FG = "#ffffff"
    BUTTON_DANGER_HOVER = "#c82333"
    BUTTON_DANGER_ACTIVE = "#bd2130"
    
    BUTTON_INFO_BG = "#17a2b8"
    BUTTON_INFO_FG = "#ffffff"
    BUTTON_INFO_HOVER = "#138496"
    BUTTON_INFO_ACTIVE = "#117a8b"
    
    BUTTON_WARNING_BG = "#ffc107"
    BUTTON_WARNING_FG = "#212529"
    BUTTON_WARNING_HOVER = "#e0a800"
    BUTTON_WARNING_ACTIVE = "#d39e00"
    
    BUTTON_LIGHT_BG = "#f8f9fa"
    BUTTON_LIGHT_FG = "#212529"
    BUTTON_LIGHT_HOVER = "#e2e6ea"
    BUTTON_LIGHT_ACTIVE = "#dae0e5"
    
    BUTTON_DISABLED_BG = "#e9ecef"
    BUTTON_DISABLED_FG = "#6c757d"
    
    # Tabs
    TAB_BG = "#ffffff"
    TAB_FG = "#495057"
    TAB_ACTIVE_BG = "#232F66"
    TAB_ACTIVE_FG = "#ffffff"
    TAB_HOVER_BG = "#e9ecef"
    TAB_BORDER = "#dee2e6"
    
    # Status & Nachrichten
    STATUS_FG = "#6c757d"
    SUCCESS = "#28a745"
    STATUS_SUCCESS = "#28a745"
    WARNING = "#ffc107"
    STATUS_WARNING = "#ffc107"
    ERROR = "#dc3545"
    STATUS_ERROR = "#dc3545"
    INFO = "#17a2b8"
    STATUS_INFO = "#17a2b8"
    ACCENT = "#232F66"
    
    # Formulare
    INPUT_BG = "#ffffff"
    INPUT_FG = "#495057"
    INPUT_BORDER = "#ced4da"
    INPUT_FOCUS_BORDER = "#232F66"
    INPUT_DISABLED_BG = "#e9ecef"
    INPUT_DISABLED_FG = "#6c757d"
    INPUT_ERROR_BORDER = "#dc3545"
    
    # Tooltips
    TOOLTIP_BG = "#212529"
    TOOLTIP_FG = "#ffffff"
    TOOLTIP_BORDER = "#343a40"
    
    # Schatten & Effekte
    SHADOW_LIGHT = "#00000010"
    SHADOW_MEDIUM = "#00000020"
    SHADOW_DARK = "#00000030"
    
    # Scrollbar
    SCROLLBAR_BG = "#f8f9fa"
    SCROLLBAR_THUMB = "#adb5bd"
    SCROLLBAR_THUMB_HOVER = "#6c757d"
    
    # Divider & Borders
    DIVIDER = "#dee2e6"
    BORDER_LIGHT = "#e9ecef"
    BORDER_MEDIUM = "#dee2e6"
    BORDER_DARK = "#adb5bd"
    
    # Prosopografie-spezifische Farben
    # Dynastien
    DYNASTY_JULIO_CLAUDIAN = "#8B4513"  # Braun
    DYNASTY_FLAVIAN = "#FF8C00"         # Orange
    DYNASTY_ANTONINE = "#9370DB"        # Violett
    DYNASTY_SEVERAN = "#DC143C"         # Rot
    DYNASTY_UNKNOWN = "#808080"         # Grau
    
    # Ämter und Status
    EMPEROR = "#FFD700"      # Gold
    CONSUL = "#4169E1"       # Blau
    SENATOR = "#32CD32"      # Grün
    GENERAL = "#B22222"      # Rot
    CITIZEN = "#808080"      # Grau
    NOBILITY = "#9370DB"     # Violett
    PLEBEIAN = "#8FBC8F"     # Hellgrün
    
    # Geschlecht
    MALE = "#4169E1"         # Blau
    FEMALE = "#FF1493"       # Pink
    UNKNOWN_GENDER = "#808080" # Grau
    
    # Lebensphasen
    CHILDHOOD = "#98FB98"    # Hellgrün
    YOUTH = "#87CEEB"        # Himmelblau
    ADULTHOOD = "#DDA0DD"    # Pflaume
    OLD_AGE = "#F0E68C"      # Khaki
    
    # Datensicherheit
    CERTAIN = "#228B22"      # Grün
    PROBABLE = "#FFD700"     # Gold
    POSSIBLE = "#FF8C00"     # Orange
    UNCERTAIN = "#DC143C"    # Rot
    
    # Timeline-spezifische Farben
    LIFE_LINE_COLOR = "#232F66"
    BIRTH_MARKER_COLOR = "#28a745"
    DEATH_MARKER_COLOR = "#dc3545"
    REIGN_COLOR = "#ffc107"
    UNCERTAINTY_COLOR = "#ff8c00"
    TIMELINE_GRID = "#e9ecef"
    TIMELINE_SCALE = "#6c757d"

class Fonts:
    """Erweiterte Schriftarten und -größen"""
    # System-Schriftarten
    FONT_FAMILY = "Segoe UI" if sys.platform == "win32" else "Helvetica"
    FONT_FAMILY_MONO = "Consolas" if sys.platform == "win32" else "Courier"
    
    # Original Fonts
    LOADING_SCREEN = (FONT_FAMILY, 12)
    STANDARD = (FONT_FAMILY, 11)
    STANDARD_BOLD = (FONT_FAMILY, 11, 'bold')
    STANDARD_ITALIC = (FONT_FAMILY, 11, 'italic')
    HEADER = (FONT_FAMILY, 16, 'bold')
    CLOCK = (FONT_FAMILY, 14)
    SUBMENU = (FONT_FAMILY, 10)
    SUBMENU_BOLD = (FONT_FAMILY, 10, 'bold')
    DEFAULT_FRAME = (FONT_FAMILY, 18, 'bold')
    
    # Neue Fonts
    HEADER_LARGE = (FONT_FAMILY, 18, 'bold')
    HEADER_MEDIUM = (FONT_FAMILY, 14, 'bold')
    HEADER_SMALL = (FONT_FAMILY, 12, 'bold')
    
    SUBHEADER = (FONT_FAMILY, 13, 'bold')
    SUBHEADER_SMALL = (FONT_FAMILY, 11, 'bold')
    
    # Text-Größen
    TEXT_LARGE = (FONT_FAMILY, 13)
    TEXT_MEDIUM = (FONT_FAMILY, 11)
    TEXT_SMALL = (FONT_FAMILY, 10)
    TEXT_TINY = (FONT_FAMILY, 9)
    
    # Tabellen
    TABLE = (FONT_FAMILY, 10)
    TABLE_HEADER = (FONT_FAMILY, 10, 'bold')
    TABLE_SMALL = (FONT_FAMILY, 9)
    
    # Buttons
    BUTTON = (FONT_FAMILY, 11, 'bold')
    BUTTON_SMALL = (FONT_FAMILY, 10)
    BUTTON_LARGE = (FONT_FAMILY, 12, 'bold')
    
    # Tabs
    TAB = (FONT_FAMILY, 11)
    TAB_ACTIVE = (FONT_FAMILY, 11, 'bold')
    
    # Formulare
    LABEL = (FONT_FAMILY, 10)
    LABEL_BOLD = (FONT_FAMILY, 10, 'bold')
    INPUT = (FONT_FAMILY, 11)
    INPUT_SMALL = (FONT_FAMILY, 10)
    
    # Status & Nachrichten
    STATUS = (FONT_FAMILY, 10)
    STATUS_BOLD = (FONT_FAMILY, 10, 'bold')
    TOOLTIP = (FONT_FAMILY, 9)
    
    # Icons (für Emoji/Symbol-Unterstützung)
    ICON = (FONT_FAMILY, 14)
    ICON_SMALL = (FONT_FAMILY, 12)
    ICON_LARGE = (FONT_FAMILY, 16)
    
    # Spezielle Fonts
    MONO = (FONT_FAMILY_MONO, 10)
    MONO_SMALL = (FONT_FAMILY_MONO, 9)
    CAPTION = (FONT_FAMILY, 9)
    CAPTION_ITALIC = (FONT_FAMILY, 9, 'italic')

class UIConstants:
    """UI-spezifische Konstanten"""
    # Padding & Margins
    PADDING_SMALL = 3
    PADDING_MEDIUM = 6
    PADDING_LARGE = 10
    PADDING_XLARGE = 15
    
    # Border Radius (für Canvas-basierte Widgets)
    RADIUS_SMALL = 4
    RADIUS_MEDIUM = 6
    RADIUS_LARGE = 8
    
    # Button Größen
    BUTTON_HEIGHT = 36
    BUTTON_HEIGHT_SMALL = 28
    BUTTON_HEIGHT_LARGE = 44
    
    # Input Größen
    INPUT_HEIGHT = 32
    INPUT_HEIGHT_SMALL = 28
    INPUT_HEIGHT_LARGE = 40
    
    # Icon Größen
    ICON_SIZE_SMALL = 16
    ICON_SIZE_MEDIUM = 20
    ICON_SIZE_LARGE = 24
    
    # Animationen
    FADE_STEPS = 10
    SLIDE_STEPS = 15
    
    # Z-Index Ebenen
    Z_BACKGROUND = 0
    Z_CONTENT = 10
    Z_OVERLAY = 100
    Z_MODAL = 1000
    Z_TOOLTIP = 10000
    
    # Timeline-spezifische Konstanten
    TIMELINE_MIN_HEIGHT = 400
    TIMELINE_MAX_HEIGHT = 800
    TOOLTIP_MAX_WIDTH = 300

class Icons:
    """Unicode-Icons für die Anwendung"""
    # Navigation
    HOME = "🏠"
    BACK = "◀"
    FORWARD = "▶"
    UP = "▲"
    DOWN = "▼"
    
    # Aktionen
    ADD = "➕"
    DELETE = "🗑️"
    EDIT = "✏️"
    SAVE = "💾"
    CANCEL = "❌"
    SEARCH = "🔍"
    FILTER = "🔽"
    SORT = "↕️"
    REFRESH = "🔄"
    
    # Status
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    LOADING = "⏳"
    
    # Dateien
    FILE = "📄"
    FOLDER = "📁"
    EXPORT = "📤"
    IMPORT = "📥"
    
    # Personen
    PERSON = "👤"
    PEOPLE = "👥"
    FAMILY = "👨‍👩‍👧‍👦"
    MARRIAGE = "💑"
    CHILD = "👶"
    
    # Sonstiges
    CALENDAR = "📅"
    CLOCK = "🕐"
    LOCATION = "📍"
    BOOK = "📚"
    DOCUMENT = "📋"
    STAR = "⭐"
    TROPHY = "🏆"
    SCROLL = "📜"
    SCENE = '📸'
    
    # Timeline-spezifische Icons
    TIMELINE = "📊"
    BIRTH = "🌱"
    DEATH = "⚰️"
    REIGN = "👑"
    BATTLE = "⚔️"
    ZOOM_IN = "🔍+"
    ZOOM_OUT = "🔍-"
    DYNASTY = "🏛️"
    EMPEROR = "👑"
    CONSUL = "⚖️"
    SENATOR = "🏛️"
    GENERAL = "🛡️"
    
    # Unsicherheit
    UNCERTAIN = "❓"
    APPROXIMATE = "≈"
    BEFORE = "≤"
    AFTER = "≥"

class Messages:
    """Standardnachrichten der Anwendung"""
    # Erfolg
    SAVE_SUCCESS = "Änderungen erfolgreich gespeichert"
    DELETE_SUCCESS = "Eintrag erfolgreich gelöscht"
    CREATE_SUCCESS = "Neuer Eintrag erfolgreich erstellt"
    
    # Fehler
    SAVE_ERROR = "Fehler beim Speichern der Änderungen"
    DELETE_ERROR = "Fehler beim Löschen des Eintrags"
    LOAD_ERROR = "Fehler beim Laden der Daten"
    
    # Bestätigungen
    DELETE_CONFIRM = "Möchten Sie diesen Eintrag wirklich löschen?"
    UNSAVED_CHANGES = "Es gibt ungespeicherte Änderungen. Möchten Sie fortfahren?"
    
    # Platzhalter
    SEARCH_PLACEHOLDER = "Suchen..."
    NO_SELECTION = "Kein Eintrag ausgewählt"
    NO_DATA = "Keine Daten vorhanden"
    
    # Timeline-spezifische Nachrichten
    TIMELINE_LOADING = "Lade Timeline-Daten..."
    TIMELINE_NO_DATA = "Keine Personen im ausgewählten Zeitraum"
    TIMELINE_ERROR = "Fehler beim Laden der Timeline"
    YEAR_RANGE_INVALID = "Ungültiger Jahresbereich"

class DataValidation:
    """Validierungsregeln für prosopografische Daten"""
    
    # Jahr-Validierung
    @staticmethod
    def is_valid_year(year):
        """Prüft ob Jahr im gültigen Bereich liegt"""
        if year is None:
            return True
        return TimelineConfig.MIN_YEAR <= year <= TimelineConfig.MAX_YEAR
    
    @staticmethod
    def is_valid_date_range(start_year, end_year):
        """Prüft ob Datumsbereich gültig ist"""
        if start_year is None or end_year is None:
            return True
        return start_year <= end_year
    
    # Name-Validierung
    @staticmethod
    def is_valid_name(name):
        """Prüft ob Name gültig ist"""
        return name and len(name.strip()) > 0
    
    # Status-Validierung
    VALID_TITLES = [
        'Kaiser', 'Augustus', 'Caesar', 'Consul', 'Senator', 
        'Praetor', 'Quaestor', 'Aedil', 'Tribun', 'Legat',
        'Imperator', 'Princeps', 'Pontifex Maximus'
    ]
    
    VALID_DYNASTIES = [
        'Julisch-Claudisch', 'Flavisch', 'Antoninisch', 
        'Severisch', 'Soldatenkaiser', 'Tetrarchie'
    ]
    
    VALID_GENDERS = ['männlich', 'weiblich', 'unbekannt']
    
    VALID_STATUS = ['Kaiser', 'Adel', 'Bürger', 'Freigelassener', 'Sklave']

class Localization:
    """Lokalisierungsstrings"""
    
    GERMAN = {
        'timeline_title': 'Zeitstrahl Überblick',
        'birth': 'Geburt',
        'death': 'Tod',
        'reign': 'Regierungszeit',
        'dynasty': 'Dynastie',
        'year_ad': 'n.Chr.',
        'year_bc': 'v.Chr.',
        'loading': 'Lade Daten...',
        'no_data': 'Keine Daten verfügbar',
        'zoom_in': 'Vergrößern',
        'zoom_out': 'Verkleinern',
        'from_year': 'Von Jahr:',
        'to_year': 'Bis Jahr:',
        'update': 'Aktualisieren',
        'filter_options': 'Filter & Anzeige',
        'show_birth': 'Geburt anzeigen',
        'show_death': 'Tod anzeigen',
        'show_reign': 'Regierungszeit anzeigen',
        'persons_loaded': 'Personen geladen',
        'no_persons_in_range': 'Keine Personen im Zeitraum'
    }
    
    ENGLISH = {
        'timeline_title': 'Timeline Overview',
        'birth': 'Birth',
        'death': 'Death',
        'reign': 'Reign',
        'dynasty': 'Dynasty',
        'year_ad': 'AD',
        'year_bc': 'BC',
        'loading': 'Loading data...',
        'no_data': 'No data available',
        'zoom_in': 'Zoom In',
        'zoom_out': 'Zoom Out',
        'from_year': 'From Year:',
        'to_year': 'To Year:',
        'update': 'Update',
        'filter_options': 'Filter & Display',
        'show_birth': 'Show Birth',
        'show_death': 'Show Death',
        'show_reign': 'Show Reign',
        'persons_loaded': 'persons loaded',
        'no_persons_in_range': 'No persons in time range'
    }
    
    CURRENT = GERMAN  # Standard-Sprache