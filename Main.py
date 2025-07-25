import tkinter as tk
import os
import sys

# Aktuelles Verzeichnis zum Suchpfad hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Absolute Importe
from Objects.Config import AppConfig, AppColors
from Objects.Frames import TopFrame, NavigationFrame, SubMenuFrame, ContentFrame
from Objects.Logger import logger

class MainApp(tk.Tk):
    """
    Hauptanwendungsklasse für Prosop.
    """
    
    def __init__(self) -> None:
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
    
    def _SelectInitialNavigation(self) -> None:
        """Wählt das erste Navigationselement aus"""
        if len(AppConfig.NAV_OPTIONS) > 0:
            logger.info(f"Automatische Auswahl des ersten Elements: {AppConfig.NAV_OPTIONS[0]}")
            self.navigation_frame.OnSelect(AppConfig.NAV_OPTIONS[0])
    
    def _SetupIcon(self) -> None:
        try:
            self.icon = tk.PhotoImage(file=AppConfig.APP_ICON)
            self.iconphoto(True, self.icon)
        except Exception as e:
            logger.error(f"Fehler beim Laden des Icons: {e}")
    
    def _ConfigureMainGrid(self) -> None:
        """Konfiguriert das Grid-Layout des Hauptfensters"""
        self.columnconfigure(0, weight=0)   # Navigationsspalte (feste Breite)
        self.columnconfigure(1, weight=0)   # Submenüspalte (passt sich an Inhalt an)
        self.columnconfigure(2, weight=1)   # Inhaltsspalte (dehnbar)
        self.rowconfigure(0, weight=0)      # Obere Zeile (feste Höhe)
        self.rowconfigure(1, weight=1)      # Inhaltszeile (dehnbar)
    
    def _CreateUiComponents(self) -> None:
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
    
    def UpdateContent(self, option: str) -> None:
        """Aktualisiert den Inhaltsbereich basierend auf der Navigationsoption"""
        # Prüfe, ob die Option ein Submenü hat
        if self.navigation_frame.HasSubmenu(option):
            # Zeige Submenü an
            self.submenu_frame.grid(row=1, column=1, sticky='nsew')
            self.submenu_frame.UpdateSubmenu(option)
        else:
            # Verstecke Submenü
            self.submenu_frame.grid_forget()
            # Aktualisiere den Inhalt direkt
            self.content_frame.UpdateContent(option)
    
    def HandleSubmenuSelect(self, main_option: str, submenu_option: str):
        """Behandelt die Auswahl einer Submenüoption"""
        # Verstecke das Submenü nicht, damit es sichtbar bleibt
        # Aktualisiere nur den Inhalt
        self.content_frame.UpdateContent(f"{main_option} - {submenu_option}")

if __name__ == '__main__':
    # Anwendung erstellen und starten
    app = MainApp()
    app.mainloop()