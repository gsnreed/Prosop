import tkinter as tk
from tkinter import filedialog, messagebox
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
from Objects.Romans import Roman, load_romans_from_json, save_romans_to_json
from Objects.Command import *
from Objects.LoadingScreen import LoadingScreen

class MainApp(tk.Tk):
    """
    Hauptanwendungsklasse für Prosop.
    """
    
    def __init__(self) -> None:
        super().__init__()

        # Dateiverwaltungsattribute hinzufügen
        self.current_file = None # Pfad zur aktuell geöffneten Datei
        self.file_modified = False  # Zeigt an, ob ungespeicherte Änderungen vorliegen
        self.romans = []    # Liste für alle Römereinträge

        self.command_manager = CommandManager()

        # --- Fensterkonfiguration ---
        self.title(AppConfig.APP_TITLE)
        self.geometry(AppConfig.WINDOW_SIZE)
        self.resizable(True, True)
        self.config(bg=AppColors.SELECTION_BAR)
        
        # Icon einrichten
        self._SetupIcon()

        # Menüleiste einrichten
        self._SetupMenuBar()
        self._UpdateEditMenuState()
        
        # --- Grid-Layout für Hauptfenster ---
        self._ConfigureMainGrid()
        
        # --- UI-Komponenten erstellen ---
        self._CreateUiComponents()
        
        # Erstes Navigation-Element direkt auswählen
        if len(AppConfig.NAV_OPTIONS) > 0:
            self.navigation_frame.OnSelect(AppConfig.NAV_OPTIONS[0])
        
        # Anwendungsstart protokollieren
        logger.info("Anwendung gestartet")

    def _SetupMenuBar(self):
        # Hauptmenüleiste erstellen
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Dropdown-Menü "Datei" erstellen
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Neu", command=self._OnFileNew, accelerator="Ctrl+N")
        file_menu.add_command(label="Öffnen", command=self._OnFileOpen, accelerator="Ctrl+O")
        file_menu.add_command(label="Speichern", command=self._OnFileSave, accelerator="Ctrl+S")
        file_menu.add_command(label="Speichern unter", command=self._OnFileSaveAs, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self._OnExit)
        menubar.add_cascade(label="Datei", menu=file_menu)

        # Tastenkombinationen registrieren
        self.bind("<Control-s>", lambda event: self._OnFileSave())
        self.bind("<Control-S>", lambda event: self._OnFileSaveAs())  # Ctrl+Shift+S
        self.bind("<Control-o>", lambda event: self._OnFileOpen())
        self.bind("<Control-n>", lambda event: self._OnFileNew())
        
        # Dropdown-Menü "Bearbeiten" mit Untermenüs erstellen
        edit_menu = tk.Menu(menubar, tearoff=0)
        self.undo_menu_index = 0  # Erstes Element
        self.redo_menu_index = 1  # Zweites Element
        edit_menu.add_command(label="Rückgängig", command=self._OnEditUndo, accelerator='Ctrl+Z')
        edit_menu.add_command(label="Wiederherstellen", command=self._OnEditRedo, accelerator='Ctrl+Y')
        edit_menu.add_separator()

        self.bind("<Control-z>", lambda event: self._OnEditUndo())
        self.bind("<Control-y>", lambda event: self._OnEditRedo())
        
        # Untermenü für "Format" erstellen
        format_menu = tk.Menu(edit_menu, tearoff=0)
        format_menu.add_command(label="Fett", command=self._OnFormatBold)
        format_menu.add_command(label="Kursiv", command=self._OnFormatItalic)
        format_menu.add_command(label="Unterstrichen", command=self._OnFormatUnderline)
        edit_menu.add_cascade(label="Format", menu=format_menu)

        menubar.add_cascade(label="Bearbeiten", menu=edit_menu)
        
        # Dropdown-Menü "Hilfe" erstellen
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Dokumentation", command=self._OnHelpDocs)
        help_menu.add_command(label="Über", command=self._OnHelpAbout)
        menubar.add_cascade(label="Hilfe", menu=help_menu)

        self.edit_menu = edit_menu

    
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

    def _OnFileNew(self):
        logger.info("Datei -> Neu ausgewählt")

        if self.file_modified:
            if not self._CheckUnsavedChanges():
                return
            
        self.romans = []
        self.current_file = None
        self.file_modified = False

        self.command_manager.clear()

        self.title(AppConfig.APP_TITLE)
        self._UpdateEditMenuState()
    
    def _CheckUnsavedChanges(self):
        """Prüft auf ungespeicherte Änderungen"""
        if not self.file_modified:
            return True
        
        response = messagebox.askokcancel(
            'Ungespeicherte Änderungen',
            'Es gibt ungespeicherte Ändeurngen. Möchten Sie diese speichern?'
        )

        if response is None:    # Cancel
            return False
        elif response:          # Yes
            return self._OnFileSave()
        else:
            return True     # No
    
    def _OnFileOpen(self):
        logger.info("Datei -> Öffnen ausgewählt")
        
        if self.file_modified:
            if not self._CheckUnsavedChanges():
                return
            
        file_path = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[
                ('JSON-Dateien', '*.json'),
                ('Excel-Dateien', '*.xlsx')
            ],
            title='Datenbank öffnen'
        )

        if file_path:
            self._LoadFile(file_path)
        
    def _OnFileSave(self):
        """Speichert die aktuelle Datei oder ruft 'Speichern unter' auf, wenn noch keine Datei existiert"""
        logger.info("Datei -> Speichern ausgewählt")

        if self.current_file:
            self._SaveToFile(self.current_file)
        else:
            self._OnFileSaveAs()

    def _OnFileSaveAs(self):
        """Öffnet einen Dialog zum Speichern unter einem neuen Namen"""
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
            self._SaveToFile(file_path)
    
    def _SaveToFile(self, file_path):
        """Speicher die aktuellen Daten in die angegebene Datei"""
        from Objects.LoadingScreen import LoadingScreen
        
        try:
            # Ladebildschirm anzeigen
            loading_screen = LoadingScreen(self, f"Speichere Datei {os.path.basename(file_path)}...")
            self.update()  # UI aktualisieren
            
            # Speicherlogik
            success = save_romans_to_json(self.romans, file_path)

            if not success:
                loading_screen.finish()
                raise Exception('Fehler beim Speichern der Daten')

            # Dateiinfos aktualisieren
            self.current_file = file_path
            self.file_modified = False

            # Titel aktualisieren
            file_name = os.path.basename(file_path).split('.')[0]
            self.title(f"{AppConfig.APP_TITLE} - {file_name}")
            
            # Ladebildschirm schließen
            loading_screen.finish()
            
            logger.info(f'Datei erfolgreich gespeichert: {file_path}')
        
        except Exception as e:
            try:
                loading_screen.finish()
            except:
                pass
            messagebox.showerror("Fehler beim Speichern", f"Die Datei konnte nicht gespeichert werden:\n{str(e)}")
            logger.error(f"Fehler beim Speichern der Datei {file_path}: {e}")

        
    def _OnEditUndo(self):
        logger.info("Bearbeiten -> Rückgängig ausgewählt")
        
        if self.command_manager.undo():
            # UI aktualisieren
            self.SetModified(True)
            self.content_frame.UpdateContent(self.content_frame.current_option)
            self._UpdateEditMenuState()
        
    def _OnEditRedo(self):
        logger.info("Bearbeiten -> Wiederherstellen ausgewählt")
        
        if self.command_manager.redo():
            # UI aktualisieren
            self.SetModified(True)
            self.content_frame.UpdateContent(self.content_frame.current_option)
            self._UpdateEditMenuState()
        
    def _UpdateEditMenuState(self):
        """Aktualisiert den Zustand der Bearbeiten-Menüeinträge"""
        try:
            if self.command_manager.can_undo():
                self.edit_menu.entryconfig(self.undo_menu_index, state=tk.NORMAL)
            else:
                self.edit_menu.entryconfig(self.undo_menu_index, state=tk.DISABLED)
                
            if self.command_manager.can_redo():
                self.edit_menu.entryconfig(self.redo_menu_index, state=tk.NORMAL)
            else:
                self.edit_menu.entryconfig(self.redo_menu_index, state=tk.DISABLED)
        except Exception as e:
            logger.error(f"Fehler beim Aktualisieren des Menüstatus: {e}")

    def _OnFormatBold(self):
        logger.info("Bearbeiten -> Format -> Fett ausgewählt")
        # Implementiere Funktionalität hier
        
    def _OnFormatItalic(self):
        logger.info("Bearbeiten -> Format -> Kursiv ausgewählt")
        # Implementiere Funktionalität hier
        
    def _OnFormatUnderline(self):
        logger.info("Bearbeiten -> Format -> Unterstrichen ausgewählt")
        # Implementiere Funktionalität hier
        
    def _OnHelpDocs(self):
        logger.info("Hilfe -> Dokumentation ausgewählt")
        # Implementiere Funktionalität hier
        
    def _OnHelpAbout(self):
        logger.info("Hilfe -> Über ausgewählt")
        # Implementiere Funktionalität hier

    def _OnExit(self):
        logger.info("Anwendung wird beendet")

        if self.file_modified:
            if not self._CheckUnsavedChanges():
                return  # Beenden abbrechen

        self.quit()      # Beendet die Ereignisschleife
        self.destroy()   # Zerstört alle Widgets und gibt Ressourcen frei

    def _LoadFile(self, file_path):
        """Lädt den Inhalt der Datei mit Ladebildschirm"""
        # Aktuelle Navigation speichern
        current_navigation = None
        if hasattr(self.navigation_frame, 'selected_option'):
            current_navigation = self.navigation_frame.selected_option
        
        # Aktuelles Submenü speichern, falls vorhanden
        current_submenu_item = None
        if hasattr(self.submenu_frame, 'selected_submenu_item'):
            current_submenu_item = self.submenu_frame.selected_submenu_item
        
        try:
            # Ladebildschirm anzeigen
            loading_screen = LoadingScreen(self, f"Lade Datei {os.path.basename(file_path)}...")
            self.update_idletasks()  # UI aktualisieren
            
            # Dateierweiterung prüfen
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.json':
                loaded_romans = load_romans_from_json(file_path)
            elif ext == '.xlsx':
                # Excel-Unterstützung hier hinzufügen
                loading_screen.finish()
                messagebox.showerror("Fehler", "Excel-Unterstützung noch nicht implementiert.")
                return
            else:
                loading_screen.finish()
                messagebox.showerror("Fehler", f"Nicht unterstütztes Dateiformat: {ext}")
                return
                    
            if loaded_romans is None or not isinstance(loaded_romans, list):
                loading_screen.finish()
                raise Exception('Ungültiges Dateiformat oder keine Romans gefunden')
            
            self.romans = loaded_romans

            # Dateiinfos aktualisieren
            self.current_file = file_path
            self.file_modified = False

            self.command_manager.clear()

            # Titel aktualisieren
            file_name = os.path.basename(file_path).split('.')[0]
            self.title(f"{AppConfig.APP_TITLE} - {file_name}")
            
            # Menüs aktualisieren
            self._UpdateEditMenuState()
            
            # Schließen des Ladebildschirms
            loading_screen.finish()
            
            # Zur vorherigen Ansicht zurückkehren
            if current_navigation:
                self.navigation_frame.OnSelect(current_navigation)
                
                # Wenn ein Submenü-Item aktiv war, dieses wiederherstellen
                if current_navigation in self.navigation_frame.options_with_submenu and current_submenu_item:
                    # Warte kurz, bis die Navigation verarbeitet wurde
                    self.after(100, lambda: self.submenu_frame.OnSubMenuSelect(current_navigation, current_submenu_item))
            
            logger.info(f'Datei erfolgreich geladen: {file_path}')
        
        except Exception as e:
            try:
                # Sicherstellen, dass der Ladebildschirm geschlossen wird
                loading_screen.finish()
            except:
                pass
            messagebox.showerror("Fehler beim Öffnen", f"Die Datei konnte nicht geöffnet werden:\n{str(e)}")
            logger.error(f"Fehler beim Laden der Datei {file_path}: {e}")
    
    def _UpdateCurrentView(self):
        """Aktualisiert die aktuelle Ansicht"""
        # Aktuelle Navigation ermitteln
        current_nav = None
        if hasattr(self.navigation_frame, 'selected_option'):
            current_nav = self.navigation_frame.selected_option
        
        # Falls keine aktuelle Navigation vorhanden, erste Option nehmen
        if not current_nav and len(AppConfig.NAV_OPTIONS) > 0:
            current_nav = AppConfig.NAV_OPTIONS[0]
        
        # Inhalte aktualisieren
        if current_nav:
            # Simuliere eine Auswahl des aktuellen Elements
            self.navigation_frame.OnSelect(current_nav)
        
    def SetModified(self, modified=True):
        """Setzt den Änderungsstatus und aktualisiert die UI entsprechend"""
        self.file_modified = modified
        
        # Titel anpassen
        if self.current_file:
            file_name = os.path.basename(self.current_file).split('.')[0]
            marker = "*" if modified else ""
            self.title(f"{AppConfig.APP_TITLE} - {marker}{file_name}")
        else:
            self.title(f"{AppConfig.APP_TITLE}{' *' if modified else ''}")

    def AddRoman(self, roman):
        """Fügt einen neuen Roman zur Liste hinzu und markiert Änderungen"""
        if isinstance(roman, Roman):
            command = AddRomanCommand(self.romans, roman)
            self.command_manager.execute_command(command)
            self.SetModified(True)
            self._UpdateEditMenuState()
            logger.info(f"Roman '{roman['Name']}' hinzugefügt")
        else:
            logger.error("Versuch, ein Nicht-Roman-Objekt hinzuzufügen")

    def RemoveRoman(self, index):
        """Entfernt einen Roman aus der Liste"""
        if 0 <= index < len(self.romans):
            command = RemoveRomanCommand(self.romans, index)
            self.command_manager.execute_command(command)
            self.SetModified(True)
            self._UpdateEditMenuState()
            logger.info(f"Roman an Position {index} entfernt")
        else:
            logger.error(f"Ungültiger Index beim Entfernen: {index}")

    def EditRomanProperty(self, roman, property_name, new_value):
        """Bearbeitet eine Eigenschaft eines Romans"""
        if isinstance(roman, Roman) and property_name:
            command = EditRomanCommand(roman, property_name, new_value)
            self.command_manager.execute_command(command)
            self.SetModified(True)
            self._UpdateEditMenuState()
            logger.info(f"Eigenschaft '{property_name}' von Roman '{roman['Name']}' bearbeitet")
        else:
            logger.error("Ungültige Parameter für Roman-Bearbeitung")            

if __name__ == '__main__':
    # Anwendung erstellen und starten
    app = MainApp()
    app.mainloop()