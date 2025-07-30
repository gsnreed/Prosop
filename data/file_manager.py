from tkinter import messagebox
import os
import sys

# Projektwurzel (eine Ebene über dem Skriptverzeichnis)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppConfig
from utils.logger import logger
from ui.dialogs.loading_screen import LoadingScreen
from data.models.roman import load_romans_from_json, save_romans_to_json

class FileManager:
    """Führt alle Dateioperationen aus"""
    
    def __init__(self, app):
        """
        FileManager initialisieren.
        
        Args:
            app: Referenz zur Hauptapp
        """
        self.__app = app
    
    def LoadFile(self, file_path: str) -> bool:
        """
        Daten von einer Datei laden.
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            bool: True wenn laden erfolgreich war
        """
        # Aktuelle Navigationsoption merken
        current_navigation = None
        if hasattr(self.__app.navigation_frame, 'selected_option'):
            current_navigation = self.__app.navigation_frame.selected_option
        
        # Submenu Zustand merken
        current_submenu_item = None
        if hasattr(self.__app.submenu_frame, 'selected_submenu_item'):
            current_submenu_item = self.__app.submenu_frame.selected_submenu_item
        
        try:
            # Ladescreen anzeigen
            loading_screen = LoadingScreen(self.__app, f"Lade Datei {os.path.basename(file_path)}...")
            self.__app.update_idletasks()
            
            # Dateiformat speichern
            ext = os.path.splitext(file_path)[1].lower()
            
            # Daten laden abhängig vom Dateityp
            if ext == '.json':
                loaded_romans = load_romans_from_json(file_path)
            elif ext == '.xlsx':
                # Excel
                loading_screen.Finish()
                messagebox.showerror("Fehler", "Excel-Unterstützung noch nicht implementiert.")
                return False
            else:
                loading_screen.Finish()
                messagebox.showerror("Fehler", f"Nicht unterstütztes Dateiformat: {ext}")
                return False
            
            # Daten validieren
            if loaded_romans is None or not isinstance(loaded_romans, list):
                loading_screen.Finish()
                raise ValueError('Ungültiges Dateiformat oder keine Romans gefunden')
            
            # App Status updaten
            self.__app.romans = loaded_romans
            self.__app.current_file = file_path
            self.__app.file_modified = False
            self.__app.command_manager.Clear()
            
            # Ansicht Updaten
            file_name = os.path.basename(file_path).split('.')[0]
            self.__app.title(f"{AppConfig.APP_TITLE} - {file_name}")
            
            # Ladescreen schließen
            loading_screen.Finish()
            
            # Zu letzter Position zurückkehren
            if current_navigation:
                self.__app.navigation_frame.OnSelect(current_navigation)
                
                # Submenü wiederherstellen
                if (hasattr(self.__app.navigation_frame, 'options_with_submenu') and
                    current_navigation in self.__app.navigation_frame.options_with_submenu and 
                    current_submenu_item):
                    # Warten auf Navigation
                    self.__app.after(100, lambda: self.__app.submenu_frame.OnSubMenuSelect(
                        current_navigation, current_submenu_item))
            
            logger.info(f'Datei erfolgreich geladen: {file_path}')
            return True
            
        except Exception as e:
            try:
                # Ladescreen schließen
                loading_screen.Finish()
            except:
                pass
            messagebox.showerror("Fehler beim Öffnen", 
                               f"Die Datei konnte nicht geöffnet werden:\n{str(e)}")
            logger.error(f"Fehler beim Laden der Datei {file_path}: {e}")
            return False
    
    def SaveToFile(self, file_path: str) -> bool:
        """
        Daten speichern
        
        Args:
            file_path: Dateipfad
            
        Returns:
            bool: True wenn Speichern erfolgreich war
        """
        try:
            # Ladescreen anzeigen
            loading_screen = LoadingScreen(
                self.__app, f"Speichere Datei {os.path.basename(file_path)}...")
            self.__app.update()
            
            # Speichern
            success = save_romans_to_json(self.__app.romans, file_path)

            if not success:
                loading_screen.Finish()
                raise Exception('Fehler beim Speichern der Daten')
            
            # Appstatus aktualisieren
            self.__app.current_file = file_path
            self.__app.file_modified = False
            
            # Fenster aktualisiern
            file_name = os.path.basename(file_path).split('.')[0]
            self.__app.title(f"{AppConfig.APP_TITLE} - {file_name}")
            
            # Ladescreen schließen
            loading_screen.Finish()
            
            logger.info(f'Datei erfolgreich gespeichert: {file_path}')
            return True
            
        except Exception as e:
            try:
                loading_screen.Finish()
            except:
                pass
            messagebox.showerror("Fehler beim Speichern", 
                               f"Die Datei konnte nicht gespeichert werden:\n{str(e)}")
            logger.error(f"Fehler beim Speichern der Datei {file_path}: {e}")
            return False