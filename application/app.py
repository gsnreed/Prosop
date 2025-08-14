import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Projektwurzel (eine Ebene über dem Skriptverzeichnis)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.commands import AddRomanCommand, EditRomanCommand, RemoveRomanCommand
from data.models.roman import Roman
from utils.config import AppConfig, AppColors
from application.command_manager import CommandManager
from ui.menu_manager import MenuManager
from data.file_manager import FileManager
from ui.dialogs.loading_screen import LoadingScreen
from utils.logger import logger
from ui.frames.content_frame import ContentFrame
from ui.frames.navigation_frame import NavigationFrame
from ui.frames.submenu_frame import SubMenuFrame
from ui.frames.top_frame import TopFrame

class MainApp(tk.Tk):
    """Hauptanwendungsklasse für Prosop."""
    
    def __init__(self) -> None:
        super().__init__()

        # App Variablen
        self.__current_file = None
        self.__file_modified = False
        self.__romans = []
        self.__icon = None

        self.__top_frame = None
        self.__navigation_frame = None
        self.__submenu_frame = None
        self.__content_frame = None
        
        # Command Manager initialisieren
        self.__command_manager = CommandManager()

        # Andere Manager initialisieren
        self.__menu_manager = MenuManager(self)
        self.__file_manager = FileManager(self)
        
        # Fensterkonfiguration
        self.SetupWindow()
        
        # Interfacekomponenten initalisieren
        self.ConfigureMainGrid()
        self.CreateUiComponents()
        
        # Erstes Navigationsitem auswählen
        self.SelectInitialNavigation()

        self.__menu_manager.UpdateEditMenuState()
        
        logger.info("Anwendung gestartet")

    # Properties für private Variablen
    @property
    def current_file(self):
        return self.__current_file
    
    @current_file.setter
    def current_file(self, value):
        self.__current_file = value
    
    @property
    def file_modified(self):
        return self.__file_modified
    
    @file_modified.setter
    def file_modified(self, value):
        self.__file_modified = value
        
        # Titel anpassen
        if self.__current_file:
            file_name = os.path.basename(self.__current_file).split('.')[0]
            marker = "*" if value else ""
            self.title(f"{AppConfig.APP_TITLE} - {marker}{file_name}")
        else:
            self.title(f"{AppConfig.APP_TITLE}{' *' if value else ''}")
    
    @property
    def romans(self):
        return self.__romans
    
    @romans.setter
    def romans(self, value):
        self.__romans = value
    
    @property
    def command_manager(self):
        return self.__command_manager
    
    @property
    def navigation_frame(self):
        return self.__navigation_frame
    
    @property
    def submenu_frame(self):
        return self.__submenu_frame
    
    @property
    def content_frame(self):
        return self.__content_frame
    
    @property
    def menu_manager(self):
        return self.__menu_manager
    
    def SetupWindow(self) -> None:
        """Fenster Konfiguration"""
        self.title(AppConfig.APP_TITLE)
        self.geometry(AppConfig.WINDOW_SIZE)
        self.resizable(True, True)
        self.config(bg=AppColors.SELECTION_BAR)
        self.SetupIcon()
        self.SetupKeyboardShortcuts()
    
    def CreateUiComponents(self) -> None:
        """Erstellt alle UI-Komponenten der Anwendung"""
        # Oberen Rahmen erstellen
        self.__top_frame = TopFrame(self)
        self.__top_frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

        # Navigationsrahmen erstellen und mit dem Inhaltsrahmen verbinden
        self.__navigation_frame = NavigationFrame(self, self)
        self.__navigation_frame.grid(row=1, column=0, sticky=tk.NSEW)

        # Submenü-Rahmen erstellen (nicht direkt anzeigen)
        self.__submenu_frame = SubMenuFrame(self)
        
        # Inhaltsrahmen erstellen
        self.__content_frame = ContentFrame(self)
        self.__content_frame.grid(row=1, column=2, sticky=tk.NSEW, padx=(5, 5), pady=(5, 5))
    
    def ConfigureMainGrid(self) -> None:
        """Konfiguriert das Grid-Layout des Hauptfensters"""
        self.columnconfigure(0, weight=0)   # Navigationsspalte (feste Breite)
        self.columnconfigure(1, weight=0)   # Submenüspalte (passt sich an Inhalt an)
        self.columnconfigure(2, weight=1)   # Inhaltsspalte (dehnbar)
        self.rowconfigure(0, weight=0)      # Obere Zeile (feste Höhe)
        self.rowconfigure(1, weight=1)      # Inhaltszeile (dehnbar)

    def SelectInitialNavigation(self) -> None:
        """Wählt das erste Navigationselement aus"""
        if len(AppConfig.NAV_OPTIONS) > 0:
            logger.info(f"Automatische Auswahl des ersten Elements: {AppConfig.NAV_OPTIONS[0]}")
            self.__navigation_frame.OnSelect(AppConfig.NAV_OPTIONS[0])

    def SetupIcon(self) -> None:
        """Anpassung des Icons"""
        try:
            self.__icon = tk.PhotoImage(file=AppConfig.APP_ICON)
            self.iconphoto(True, self.__icon)
        except Exception as e:
            logger.error(f"Fehler beim Laden des Icons: {e}")

    def SetupKeyboardShortcuts(self):
        # Tastenkombinationen
        self.bind('<Control-s>', lambda event: self.OnFileSave())
        self.bind('<Control-S>', lambda event: self.OnFileSaveAs())
        self.bind('<Control-o>', lambda event: self.OnFileOpen())
        self.bind('<Control-n>', lambda event: self.OnFileNew())
        self.bind('<Control-z>', lambda event: self.OnEditUndo())
        self.bind('<Control-y>', lambda event: self.OnEditRedo())
    
    def UpdateContent(self, option: str) -> None:
        """Aktualisiert den Inhaltsbereich basierend auf der Navigationsoption"""
        # Prüfe, ob die Option ein Submenü hat
        if self.__navigation_frame.HasSubmenu(option):
            # Zeige Submenü an
            self.__submenu_frame.grid(row=1, column=1, sticky='nsew')
            self.__submenu_frame.UpdateSubmenu(option)
        else:
            # Verstecke Submenü
            self.__submenu_frame.grid_forget()
            # Aktualisiere den Inhalt direkt
            self.__content_frame.UpdateContent(option)
    
    def HandleSubmenuSelect(self, main_option: str, submenu_option: str):
        """Behandelt die Auswahl einer Submenüoption"""
        # Aktualisiere nur den Inhalt
        self.__content_frame.UpdateContent(f"{main_option} - {submenu_option}")
    
    # Methode für Dateioperation
    def OnFileNew(self) -> None:
        """Neue Datei erzeugen"""
        logger.info("Datei -> Neu ausgewählt")
        
        if not self.__file_modified or self.CheckUnsavedChanges(): 
            self.romans = []                    # Romans löschen
            self.current_file = None            # Referenz zur aktuellen Speicherdatei löschen
            self.__file_modified = False          # Modifiedbit zurücksetzen
            self.__command_manager.Clear()      # Befehle löschen
            self.title(AppConfig.APP_TITLE)     # Titel anpassen
            self.__menu_manager.UpdateEditMenuState()   # Rücksetzen/Wiederholen aktualisieren
            self.__content_frame.UpdateContent(self.__content_frame.current_option)
    
    def OnFileOpen(self) -> None:
        logger.info("Datei -> Öffnen ausgewählt")
        
        if not self.__file_modified or self.CheckUnsavedChanges():
            file_path = filedialog.askopenfilename(
                defaultextension='.json',
                filetypes=[
                    ('JSON-Dateien', '*.json'),
                    ('Excel-Dateien', '*.xlsx')
                ],
                title='Datenbank öffnen'
            )

            if file_path:
                self.__file_manager.LoadFile(file_path)
                self.__content_frame.UpdateContent(self.__content_frame.current_option)
    
    def OnFileSave(self) -> bool:
        """Speichert die aktuelle Datei oder ruft 'Speichern unter' auf, wenn noch keine Datei existiert"""
        logger.info("Datei -> Speichern ausgewählt")

        if self.__current_file:
            ret = self.__file_manager.SaveToFile(self.current_file)
        else:
            ret = self.OnFileSaveAs()
        return ret

    def OnFileSaveAs(self) -> bool:
        """Öffnet einen Dialog zum Speichern unter einem neuen Namen"""
        ret = False # Return value
        logger.info("Datei -> Speichern unter ausgewählt")
        file_path = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[
                ('Json-Dateien', '*.json'),
                ('Excel-Dateien', '*.xlsx')
            ],
            title='Datei speichern unter'
        )

        if file_path:
            ret = self.__file_manager.SaveToFile(file_path)
        return ret
    
    def OnExit(self) -> None:
        """Beendet die Anwendung"""
        logger.info("Anwendung wird beendet")

        if not self.__file_modified or self.CheckUnsavedChanges():
            self.quit()      # Beendet die Ereignisschleife
            self.destroy()   # Zerstört alle Widgets und gibt Ressourcen frei

    def CheckUnsavedChanges(self) -> bool:
        """Prüft auf ungespeicherte Änderungen"""
        ret = True
        if self.__file_modified:
            response = messagebox.askyesno(
                'Ungespeicherte Änderungen',
                'Es gibt ungespeicherte Änderungen. Möchten Sie diese speichern?'
            )

            if response is None:    # Cancel
                ret = False
            elif response:          # Yes
                ret = self.OnFileSave()
        return ret
    
    # Editieroperationen
    def OnEditUndo(self) -> None:
        """Führt Undo-Operation aus"""
        logger.info("Bearbeiten -> Rückgängig ausgewählt")
        
        if self.__command_manager.Undo():
            # UI aktualisieren
            self.__file_modified = True
            self.__content_frame.UpdateContent(self.__content_frame.current_option)
            self.__menu_manager.UpdateEditMenuState()
    
    def OnEditRedo(self, event=None) -> None:
        """Führt Redo-Operation aus"""
        logger.info("Bearbeiten -> Wiederherstellen ausgewählt")
        
        if self.__command_manager.Redo():
            # UI aktualisieren
            self.__file_modified = True
            self.__content_frame.UpdateContent(self.__content_frame.current_option)
            self.__menu_manager.UpdateEditMenuState()

    # Roman Management
    def AddRoman(self, roman: Roman) -> None:
        """Fügt einen neuen Roman zur Liste hinzu"""
        if isinstance(roman, Roman):
            command = AddRomanCommand(self.__romans, roman)
            self.__command_manager.ExecuteCommand(command)
            self.__file_modified = True
            self.__menu_manager.UpdateEditMenuState()
            logger.info(f"Roman '{roman['Name']}' hinzugefügt")
        else:
            logger.error("Versuch, ein Nicht-Roman-Objekt hinzuzufügen")

    def RemoveRoman(self, index: int) -> None:
        """Entfernt einen Roman aus der Liste"""
        if 0 <= index < len(self.__romans):
            command = RemoveRomanCommand(self.__romans, index)
            self.__command_manager.ExecuteCommand(command)
            self.__file_modified = True
            self.__menu_manager.UpdateEditMenuState()
            logger.info(f"Roman an Position {index} entfernt")
        else:
            logger.error(f"Ungültiger Index beim Entfernen: {index}")

    def EditRomanProperty(self, roman: Roman, property_name: str, new_value:str) -> None:
        """Bearbeitet eine Eigenschaft eines Romans"""
        if isinstance(roman, Roman) and property_name:
            command = EditRomanCommand(roman, property_name, new_value)
            self.__command_manager.ExecuteCommand(command)
            self.file_modified = True
            self.__menu_manager.UpdateEditMenuState()
            logger.info(f"Eigenschaft '{property_name}' von Roman '{roman['Name']}' bearbeitet")
        else:
            logger.error("Ungültige Parameter für Roman-Bearbeitung")
    
    def UpdateCurrentView(self) -> None:
        """Aktualisiert die aktuelle Ansicht"""
        # Aktuelle Navigation ermitteln
        current_nav = None
        if hasattr(self.__navigation_frame, 'selected_option'):
            current_nav = self.__navigation_frame.selected_option
        
        # Falls keine aktuelle Navigation vorhanden, erste Option nehmen
        if not current_nav and len(AppConfig.NAV_OPTIONS) > 0:
            current_nav = AppConfig.NAV_OPTIONS[0]
        
        # Inhalte aktualisieren
        if current_nav:
            # Simuliere eine Auswahl des aktuellen Elements
            self.__navigation_frame.OnSelect(current_nav)