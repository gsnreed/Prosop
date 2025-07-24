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
    SUBMENU_FRAME = "#F1D0FF"
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

class SubMenuFrame(tk.Frame):
    """
    Rahmen für Submenü-Optionen, erscheint rechts neben dem Navigation Frame.
    """
    
    def __init__(self, parent):
        super().__init__(parent, bg=AppColors.SUBMENU_FRAME)
        self.parent = parent
        self.selected_submenu_item = None
        self.submenu_labels = {}  # Speichert alle Submenu-Labels
        
        # Submenü-Header erstellen
        self.submenu_header = tk.Label(
            self,
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.SUBMENU_FRAME,
            fg=AppColors.KU_COLOR,
            text="Unterkategorien"
        )
        self.submenu_header.pack(side='top', fill='x', padx=10, pady=(10,5))
        
        # Frame für Submenü-Optionen
        self.options_frame = tk.Frame(self, bg=AppColors.SUBMENU_FRAME)
        self.options_frame.pack(fill='both', expand=True, padx=5)
        
        # Definiere verfügbare Submenüs
        self.submenus = {
            'Ansicht': ['Liste', 'Karte', 'Tabelle', 'Zeitstrahl'],
            'Erstellung': ['Person', 'Ort', 'Ereignis', 'Quelle'],
            'Export': ['PDF', 'CSV', 'Excel', 'XML'],
            'Import': ['CSV-Import', 'XML-Import', 'Datenbank-Import'],
            'BibTex': ['Literatur hinzufügen', 'Zitieren', 'Verwalten']
        }
    
    def UpdateSubmenu(self, option):
        """Aktualisiert die Submenüoptionen für die gewählte Hauptoption"""
        # Bestehende Optionen entfernen
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Zurücksetzen der Label-Sammlung
        self.submenu_labels = {}
        self.selected_submenu_item = None
        
        # Header aktualisieren
        self.submenu_header.config(text=f"{option}")
        
        # Neue Optionen hinzufügen
        if option in self.submenus:
            submenu_items = self.submenus[option]
            for sub_option in submenu_items:
                label = tk.Label(
                    self.options_frame,
                    text=sub_option,
                    font=('Helvetica', 11),
                    bg=AppColors.SUBMENU_FRAME,
                    fg=AppColors.KU_COLOR,
                    padx=15,
                    pady=4,
                    cursor="hand2",
                    anchor='w'  # Linksbündiger Text
                )
                label.pack(fill='x', pady=1)
                
                # Event-Binding für das Label
                label.bind("<Enter>", lambda e, l=label: self.OnSubMenuHover(l, True))
                label.bind("<Leave>", lambda e, l=label: self.OnSubMenuHover(l, False))
                label.bind("<Button-1>", lambda e, o=option, s=sub_option: self.OnSubMenuSelect(o, s))
                
                # Label speichern
                self.submenu_labels[sub_option] = label
            
            # Automatisch das erste Element auswählen
            if submenu_items:
                first_option = submenu_items[0]
                self.OnSubMenuSelect(option, first_option)
    
    def OnSubMenuHover(self, label, is_hover):
        """Behandelt Hover-Events für Submenüoptionen"""
        sub_option = label.cget("text")
        # Nur hervorheben, wenn nicht ausgewählt
        if sub_option != self.selected_submenu_item:
            if is_hover:
                label.configure(bg=AppColors.HOVER)
            else:
                label.configure(bg=AppColors.SUBMENU_FRAME)
    
    def OnSubMenuSelect(self, option, sub_option):
        """Behandelt die Auswahl einer Submenüoption"""
        # Zurücksetzen der vorherigen Auswahl
        if self.selected_submenu_item and self.selected_submenu_item in self.submenu_labels:
            old_label = self.submenu_labels[self.selected_submenu_item]
            old_label.configure(
                bg=AppColors.SUBMENU_FRAME,
                font=('Helvetica', 11),  # Normale Schrift
                fg=AppColors.KU_COLOR
            )
        
        # Neue Auswahl setzen
        self.selected_submenu_item = sub_option
        if sub_option in self.submenu_labels:
            selected_label = self.submenu_labels[sub_option]
            selected_label.configure(
                bg=AppColors.HOVER,
                font=('Helvetica', 11, 'bold'),  # Fettschrift
                
            )
        
        # Inhalt aktualisieren
        self.parent.HandleSubmenuSelect(option, sub_option)

class ContentManager:
    """Verwaltet die verschiedenen Content-Frames"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_frame = None
        
        # Frame-Mapping
        self.frames = {
            'Startseite': StartseiteFrame,
            'Ansicht - Liste': ListenViewFrame,
            'Erstellung - Person': ErstellungPersonFrame,
            # Weitere Frames hier hinzufügen
        }
    
    def ShowContent(self, option):
        """Zeigt den Content für die gewählte Option an"""
        # Entferne alten Frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Bestimme den korrekten Frame-Typ
        frame_class = None
        
        if option in self.frames:
            frame_class = self.frames[option]
        elif ' - ' in option:
            # Bei Unteroptionen wie "Ansicht - Liste" prüfen
            frame_class = self.frames.get(option, None)
        
        if not frame_class:
            # Fallback auf einen generischen Frame
            self.current_frame = BaseContentFrame(self.parent)
            label = tk.Label(
                self.current_frame, 
                text=f"Inhalt für '{option}' noch nicht implementiert",
                font=('Helvetica', 18, 'bold'),
                bg=AppColors.CONTENT_FRAME,
                fg=AppColors.KU_COLOR
            )
            label.pack(padx=50, pady=50)
        else:
            # Erstelle den neuen Frame
            self.current_frame = frame_class(self.parent)
        
        # Zeige den Frame an
        self.current_frame.pack(fill='both', expand=True)
        
        # Bei Bedarf Daten aktualisieren
        if hasattr(self.current_frame, 'UpdateData'):
            self.current_frame.UpdateData()

class BaseContentFrame(tk.Frame):
    """Basisklasse für alle Content-Frames"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
        self._CreateUi()
    
    def _CreateUi(self):
        """Erstellt die UI-Komponenten (von Unterklassen zu überschreiben)"""
        pass
    
    def UpdateData(self, data=None):
        """Aktualisiert die Daten im Frame (von Unterklassen zu überschreiben)"""
        pass

class ContentFrame(tk.Frame):
    """
    Hauptinhaltsfläche für den ausgewählten Navigationsbereich.
    """
    
    def __init__(self, parent):
        """Initialisiere den Inhaltsrahmen"""
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
        self.content_manager = ContentManager(self)
    
    def UpdateContent(self, option):
        """Aktualisiert den Inhalt basierend auf der ausgewählten Navigation."""
        self.content_manager.ShowContent(option)

class NavigationFrame(tk.Frame):
    """
    Seitenleiste mit Navigationsoptionen.
    """
    
    def __init__(self, parent, content_updater):
        super().__init__(parent, bg=AppColors.SIDEBAR_FRAME)
        self.content_updater = content_updater
        self.nav_labels = {}
        self.selected_option = None
        
        # Definiere, welche Optionen Submenus haben
        self.options_with_submenu = ['Ansicht', 'Erstellung', 'Export', 'Import', 'BibTex']
        
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
        self.navigation_header.pack(side='top', padx=10, pady=10)  # Padding hinzugefügt
    
    def _CreateNavigationOptions(self):
        """Erstellt alle Navigationsoptionen"""
        # Container-Frame mit Padding
        container_frame = tk.Frame(self, bg=AppColors.SIDEBAR_FRAME)
        container_frame.pack(fill=tk.X, padx=5)  # Padding links und rechts
        
        options_frame = tk.Frame(container_frame, bg=AppColors.SIDEBAR_FRAME)
        options_frame.pack(fill=tk.X, pady=2)
        
        # Erstelle für jede Option ein Label
        for option in AppConfig.NAV_OPTIONS:
            # Markiere Optionen mit Submenü
            has_submenu = option in self.options_with_submenu
            prefix = "» " if has_submenu else "  "
            
            label = tk.Label(
                options_frame,
                text=prefix + option,
                font=('Helvetica', 12),
                bg=AppColors.SIDEBAR_FRAME,
                fg=AppColors.KU_COLOR,
                padx=15,  # Reduziert von 20 auf 15 für konsistenteres Aussehen
                pady=5,
                cursor="hand2",
                anchor='w'
            )
            label.pack(fill=tk.X, pady=2)
            
            # Event-Binding für das Label
            label.bind("<Enter>", lambda e, opt=option: self.OnHover(opt, True))
            label.bind("<Leave>", lambda e, opt=option: self.OnHover(opt, False))
            label.bind("<Button-1>", lambda e, opt=option: self.OnSelect(opt))
            
            # Label im Dictionary speichern
            self.nav_labels[option] = label
    
    def HasSubmenu(self, option):
        """Prüft, ob eine Option ein Submenü hat"""
        return option in self.options_with_submenu
    
    def OnHover(self, option, is_hover):
        """Behandelt Hover-Events für Navigationsoptionen"""
        label = self.nav_labels[option]
        # Nur hervorheben, wenn nicht ausgewählt
        if option != self.selected_option:
            if is_hover:
                label.configure(bg=AppColors.HOVER)
            else:
                label.configure(bg=AppColors.SIDEBAR_FRAME)
    
    def OnSelect(self, option):
        """Behandelt die Auswahl einer Navigationsoption"""
        # Zurücksetzen der vorherigen Auswahl
        if self.selected_option:
            old_label = self.nav_labels[self.selected_option]
            prefix = "» " if self.HasSubmenu(self.selected_option) else "  "
            old_label.configure(
                bg=AppColors.SIDEBAR_FRAME,
                fg=AppColors.KU_COLOR,
                font=('Helvetica', 12),
                text=prefix + self.selected_option
            )
        
        # Neue Auswahl setzen
        self.selected_option = option
        selected_label = self.nav_labels[option]
        prefix = "» " if self.HasSubmenu(option) else "  "
        selected_label.configure(
            bg=AppColors.HOVER,
            fg=AppColors.KU_COLOR,
            font=('Helvetica', 12, 'bold'),
            text=prefix + option
        )
        
        # Inhalt aktualisieren
        self.content_updater.UpdateContent(option)
        
        # Ereignis protokollieren
        logger.info(f"Navigation: Option '{option}' ausgewählt")


class MainApp(tk.Tk):
    """
    Hauptanwendungsklasse für Prosop.
    """
    
    def __init__(self):
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
        
        # Erstes Navigation-Element direkt auswählen
        if len(AppConfig.NAV_OPTIONS) > 0:
            self.navigation_frame.OnSelect(AppConfig.NAV_OPTIONS[0])
        
        # Anwendungsstart protokollieren
        logger.info("Anwendung gestartet")
    
    def _SelectInitialNavigation(self):
        """Wählt das erste Navigationselement aus"""
        if len(AppConfig.NAV_OPTIONS) > 0:
            logger.info(f"Automatische Auswahl des ersten Elements: {AppConfig.NAV_OPTIONS[0]}")
            self.navigation_frame.OnSelect(AppConfig.NAV_OPTIONS[0])
    
    def _SetupIcon(self):
        try:
            self.icon = tk.PhotoImage(file=AppConfig.APP_ICON)
            self.iconphoto(True, self.icon)
        except Exception as e:
            logger.error(f"Fehler beim Laden des Icons: {e}")
    
    def _ConfigureMainGrid(self):
        """Konfiguriert das Grid-Layout des Hauptfensters"""
        self.columnconfigure(0, weight=0)   # Navigationsspalte (feste Breite)
        self.columnconfigure(1, weight=0)   # Submenüspalte (passt sich an Inhalt an)
        self.columnconfigure(2, weight=1)   # Inhaltsspalte (dehnbar)
        self.rowconfigure(0, weight=0)      # Obere Zeile (feste Höhe)
        self.rowconfigure(1, weight=1)      # Inhaltszeile (dehnbar)
    
    def _CreateUiComponents(self):
        """Erstellt alle UI-Komponenten der Anwendung"""
        # Oberen Rahmen erstellen
        self.top_frame = TopFrame(self)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
        
        # Inhaltsrahmen erstellen
        self.content_frame = ContentFrame(self)
        self.content_frame.grid(row=1, column=2, sticky='nsew', padx=(5, 5), pady=(5, 5))
        
        # Submenü-Rahmen erstellen
        self.submenu_frame = SubMenuFrame(self)
        # Nicht direkt anzeigen bis ein Element mit Submenü ausgewählt wird
        
        # Navigationsrahmen erstellen und mit dem Inhaltsrahmen verbinden
        self.navigation_frame = NavigationFrame(self, self)
        self.navigation_frame.grid(row=1, column=0, sticky='nsew')
    
    def UpdateContent(self, option):
        """Aktualisiert den Inhaltsbereich basierend auf der Navigationsoption"""
        # Prüfe, ob die Option ein Submenü hat
        if self.navigation_frame.HasSubmenu(option):
            # Zeige Submenü an
            self.submenu_frame.grid(row=1, column=1, sticky='nsew')
            self.submenu_frame.UpdateSubmenu(option)
            # Kein rechter Rand für das Navigationsmenu nötig, wenn Submenu angezeigt wird
            self.navigation_frame.grid_configure(padx=(0, 0))
        else:
            # Verstecke Submenü
            self.submenu_frame.grid_forget()
            # Aktualisiere den Inhalt direkt
            self.content_frame.UpdateContent(option)
    
    def HandleSubmenuSelect(self, main_option, submenu_option):
        """Behandelt die Auswahl einer Submenüoption"""
        # Verstecke das Submenü nicht, damit es sichtbar bleibt
        # Aktualisiere nur den Inhalt
        self.content_frame.UpdateContent(f"{main_option} - {submenu_option}")

if __name__ == '__main__':
    # Anwendung erstellen und starten
    app = MainApp()
    app.mainloop()