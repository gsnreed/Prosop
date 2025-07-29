import tkinter as tk
import os
import sys

# Projektwurzel (eine Ebene über dem Skriptverzeichnis)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.logger import logger

class MenuManager:
    '''Konfigurator für die Menüleiste'''
    def __init__(self, app):
        self.__app = app          # Referenz auf das Hauptframe
        self.__file_menu = None   # Referenz auf das Datei-Item im Menüframe
        self.__edit_menu = None   # Referenz auf das Bearbeiten-Item im Menüframe
        self.__undo_menu_index = None
        self.__redo_menu_index = None

        self.SetupMenuBar()
    
    def SetupMenuBar(self):
        # Hauptmenüleiste erstellen
        menubar = tk.Menu(self.__app)
        self.__app.config(menu=menubar)
        
        # Dropdown-Menü 'Datei' erstellen
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Neu', command=self.__app.OnFileNew, accelerator='Ctrl+N')
        file_menu.add_command(label='Öffnen', command=self.__app.OnFileOpen, accelerator='Ctrl+O')
        file_menu.add_command(label='Speichern', command=self.__app.OnFileSave, accelerator='Ctrl+S')
        file_menu.add_command(label='Speichern unter', command=self.__app.OnFileSaveAs, accelerator='Ctrl+Shift+S')
        file_menu.add_separator()  # Trennstrich
        file_menu.add_command(label='Beenden', command=self.__app.OnExit)

        # Dropdown-Menü 'Bearbeiten' erstellen
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label='Rückgängig', command=self.__app.OnEditUndo, accelerator='Ctrl+Z')
        edit_menu.add_command(label='Wiederherstellen', command=self.__app.OnEditRedo, accelerator='Ctrl+Y')

        # Indexeinträge speichern
        self.__undo_menu_index = 0
        self.__redo_menu_index = 1

        # Menüitems hinzufügen
        menubar.add_cascade(label='Datei', menu=file_menu)         # Dropdown-Menü Datei
        menubar.add_cascade(label='Bearbeiten', menu=edit_menu)    # Dropdown-Menü 'Bearbeiten'
        
        # Referenzen speichern
        self.__menubar = menubar
        self.__file_menu = file_menu
        self.__edit_menu = edit_menu

        logger.info('Menüleiste eingerichtet.')
    
    def UpdateEditMenuState(self):
        # Rückgängig/Wiederholen speichern
        can_undo = self.__app.command_manager.CanUndo()
        can_redo = self.__app.command_manager.CanRedo()
        
        # Menüeinträge blockieren, abhängig davon, ob was wiederholt ode rrückgängig gemacht werden kann
        self.__edit_menu.entryconfig(self.__undo_menu_index, 
                                  state=tk.NORMAL if can_undo else tk.DISABLED)
        self.__edit_menu.entryconfig(self.__redo_menu_index, 
                                  state=tk.NORMAL if can_redo else tk.DISABLED)