import tkinter as tk
import logging
import time
from datetime import datetime
import os

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
    HEADER = '#53366b'
    CONTENT_FRAME = "#ffffff"
    KU_COLOR = '#232F66'
    HOVER = "#D9A7FC"

# --- Logging-Konfiguration ---
def setup_logging():
    """Richtet das Logging-System ein"""
    # Stelle sicher, dass das Log-Verzeichnis existiert
    os.makedirs(AppConfig.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        filename=AppConfig.LOG_FILE,
        level=logging.NOTSET,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )
    return logging.getLogger(__name__)

# Logger initialisieren
logger = setup_logging()

# --- UI-Komponenten ---
class TopFrame(tk.Frame):
    """
    Oberer Rahmen der Anwendung mit Logo, Titel und Uhr.
    """
    
    def __init__(self, parent):
        """Initialisiere den oberen Rahmen"""
        super().__init__(parent, bg=AppColors.TOP_FRAME)
        
        # Grid-Layout konfigurieren
        self.columnconfigure(0, weight=0)  # Logo-Spalte (feste Größe)
        self.columnconfigure(1, weight=1)  # Titel-Spalte (dehnbar)
        self.columnconfigure(2, weight=0)  # Uhr-Spalte (feste Größe)
        
        # Erstelle UI-Komponenten
        self._CreateLogo()
        self._CreateTitle()
        self._CreateClock()
    
    def _CreateLogo(self):
        """Erstellt und platziert das Universitätslogo"""
        self.uni_logo = tk.PhotoImage(file=AppConfig.UNIVERSITY_LOGO).subsample(15)
        logo_label = tk.Label(self, image=self.uni_logo, bg=AppColors.TOP_FRAME)
        logo_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    
    def _CreateTitle(self):
        """Erstellt und platziert den Anwendungstitel"""
        self.title_label = tk.Label(
            self,
            font=('Helvetica', 15, 'bold'),
            bg=AppColors.TOP_FRAME,
            fg=AppColors.KU_COLOR,
            text=AppConfig.MAIN_TITLE
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')
    
    def _CreateClock(self):
        """Erstellt und platziert die Uhr"""
        self.time_label = tk.Label(
            self,
            font=('Helvetica', 15),
            bg=AppColors.TOP_FRAME,
            fg=AppColors.KU_COLOR
        )
        self.time_label.grid(row=0, column=2, padx=20, pady=10, sticky='e')
        self.UpdateClock()
    
    def UpdateClock(self):
        """Aktualisiert das Zeit-Label mit der aktuellen Uhrzeit"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        # Aktualisiere die Uhr jede Sekunde
        self.after(1000, self.UpdateClock)

class NavigationFrame(tk.Frame):
    """
    Seitenleiste mit Navigationsoptionen.
    """
    
    def __init__(self, parent, content_updater):
        """
        Initialisiere die Navigationsleiste
        
        Args:
            parent: Das Elternelement
            content_updater: Objekt mit update_content-Methode zur Aktualisierung des Inhalts
        """
        super().__init__(parent, bg=AppColors.SIDEBAR_FRAME)
        self.content_updater = content_updater
        self.nav_labels = {}
        self.selected_option = None
        
        self._CreateHeader()
        self._CreateNavigationOptions()
    
    def _CreateHeader(self):
        """Erstellt die Navigationsüberschrift"""
        self.navigation_header = tk.Label(
            self,
            font=('Helvetica', 15, 'bold'),
            bg=AppColors.SIDEBAR_FRAME,
            fg=AppColors.KU_COLOR,
            text=AppConfig.NAVIGATION_TITLE
        )
        self.navigation_header.pack(side='top', padx=20, pady=10)
    
    def _CreateNavigationOptions(self):
        """Erstellt alle Navigationsoptionen"""
        options_frame = tk.Frame(self, bg=AppColors.SIDEBAR_FRAME)
        options_frame.pack(fill=tk.X, pady=2)
        
        # Erstelle für jede Option ein Label
        for option in AppConfig.NAV_OPTIONS:
            self._CreateNavOption(options_frame, option)  # Korrigierter Methodenname
        
        # Wähle die erste Option standardmäßig aus
        if AppConfig.NAV_OPTIONS:
            self.OnSelect(AppConfig.NAV_OPTIONS[0])
    
    def _CreateNavOption(self, parent, option):  # Korrigierter Methodenname
        """
        Erstellt eine einzelne Navigationsoption
        
        Args:
            parent: Das Elternelement für das Label
            option: Der Text der Navigationsoption
        """
        label = tk.Label(
            parent,
            text=option,
            font=('Helvetica', 12),
            bg=AppColors.SIDEBAR_FRAME,
            fg=AppColors.KU_COLOR,
            padx=20,
            pady=5,
            cursor="hand2",  # Zeigt einen Hand-Cursor beim Hover
            anchor='w'       # Linksbündiger Text
        )
        label.pack(fill=tk.X, pady=2)
        
        # Event-Binding für das Label
        label.bind("<Enter>", lambda e, opt=option: self.OnHover(opt, True))
        label.bind("<Leave>", lambda e, opt=option: self.OnHover(opt, False))
        label.bind("<Button-1>", lambda e, opt=option: self.OnSelect(opt))
        
        # Label im Dictionary speichern
        self.nav_labels[option] = label
    
    def OnHover(self, option, is_hover):
        """
        Behandelt Hover-Events für Navigationsoptionen
        
        Args:
            option: Die Navigationsoption, über die gehovert wird
            is_hover: True bei MouseEnter, False bei MouseLeave
        """
        label = self.nav_labels[option]
        # Nur hervorheben, wenn nicht ausgewählt
        if option != self.selected_option:
            if is_hover:
                label.configure(bg=AppColors.HOVER)
            else:
                label.configure(bg=AppColors.SIDEBAR_FRAME)
    
    def OnSelect(self, option):
        """
        Behandelt die Auswahl einer Navigationsoption
        
        Args:
            option: Die ausgewählte Navigationsoption
        """
        # Zurücksetzen der vorherigen Auswahl
        if self.selected_option:
            old_label = self.nav_labels[self.selected_option]
            old_label.configure(
                bg=AppColors.SIDEBAR_FRAME,
                font=('Helvetica', 12)  # Normale Schrift
            )
        
        # Neue Auswahl setzen
        self.selected_option = option
        selected_label = self.nav_labels[option]
        selected_label.configure(
            bg=AppColors.HOVER,
            font=('Helvetica', 12, 'bold')  # Fettschrift
        )
        
        # Inhalt aktualisieren
        self.content_updater.UpdateContent(option)
        
        # Ereignis protokollieren
        logger.info(f"Navigation: Option '{option}' ausgewählt")

class ContentFrame(tk.Frame):
    """
    Hauptinhaltsfläche für den ausgewählten Navigationsbereich.
    """
    
    def __init__(self, parent):
        """Initialisiere den Inhaltsrahmen"""
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
    
    def UpdateContent(self, option):
        """
        Aktualisiert den Inhalt basierend auf der ausgewählten Navigation
        
        Args:
            option: Die ausgewählte Navigationsoption
        """
        # Bestehenden Inhalt entfernen
        for widget in self.winfo_children():
            widget.destroy()
        
        # Neuen Inhalt anzeigen (hier nur ein Beispiellabel)
        label = tk.Label(
            self,
            text=f"Inhalt von {option}",
            font=('Helvetica', 18, 'bold'),
            bg=AppColors.CONTENT_FRAME
        )
        label.pack(padx=50, pady=50)

class MainApp(tk.Tk):
    """
    Hauptanwendungsklasse für Prosop.
    
    Verantwortlich für die Erstellung und Organisation aller UI-Komponenten
    und die Steuerung des Anwendungsflusses.
    """
    
    def __init__(self):
        """Initialisiert die Hauptanwendung und alle Komponenten"""
        super().__init__()
        
        # --- Fensterkonfiguration ---
        self.title(AppConfig.APP_TITLE)
        self.geometry(AppConfig.WINDOW_SIZE)
        self.resizable(True, True)
        self.config(bg=AppColors.SELECTION_BAR)
        
        # Icon einrichten
        self._SetupIcon()
        
        # --- Grid-Layout für Hauptfenster ---
        self._ConfigureMainGrid()
        
        # --- UI-Komponenten erstellen ---
        self._CreateUiComponents()
        
        # Anwendungsstart protokollieren
        logger.info("Anwendung gestartet")
    
    def _SetupIcon(self):
        """Richtet das Anwendungsicon ein"""
        try:
            self.icon = tk.PhotoImage(file=AppConfig.APP_ICON)
            self.iconphoto(True, self.icon)
        except Exception as e:
            logger.error(f"Fehler beim Laden des Icons: {e}")
    
    def _ConfigureMainGrid(self):
        """Konfiguriert das Grid-Layout des Hauptfensters"""
        self.columnconfigure(0, weight=0)  # Navigationsspalte (feste Breite)
        self.columnconfigure(1, weight=1)  # Inhaltsspalte (dehnbar)
        self.rowconfigure(0, weight=0)     # Obere Zeile (feste Höhe)
        self.rowconfigure(1, weight=1)     # Inhaltszeile (dehnbar)
    
    def _CreateUiComponents(self):
        """Erstellt alle UI-Komponenten der Anwendung"""
        # Oberen Rahmen erstellen
        self.top_frame = TopFrame(self)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        # Inhaltsrahmen erstellen (vor der Navigation, damit er referenziert werden kann)
        self.content_frame = ContentFrame(self)
        self.content_frame.grid(row=1, column=1, sticky='nsew')
        
        # Navigationsrahmen erstellen und mit dem Inhaltsrahmen verbinden
        self.navigation_frame = NavigationFrame(self, self)
        self.navigation_frame.grid(row=1, column=0, sticky='nsew')
    
    def UpdateContent(self, option):
        """
        Aktualisiert den Inhaltsbereich basierend auf der Navigationsoption
        
        Args:
            option: Die ausgewählte Navigationsoption
        """
        self.content_frame.UpdateContent(option)  # Auch hier konsistente Benennung

if __name__ == '__main__':
    # Anwendung erstellen und starten
    app = MainApp()
    app.mainloop()