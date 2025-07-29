import sys
import os
import tkinter as tk
from datetime import datetime

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors, AppConfig, Fonts
from utils.logger import logger

class TopFrame(tk.Frame):
    """
    Oberer Rahmen der Anwendung mit Logo, Titel und Uhr.
    """
    
    def __init__(self, parent) -> None:
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
    
    def _CreateLogo(self) -> None:
        """Erstellt und platziert das Universitätslogo"""
        self.uni_logo = tk.PhotoImage(file=AppConfig.UNIVERSITY_LOGO).subsample(15)
        logo_label = tk.Label(self, image=self.uni_logo, bg=AppColors.TOP_FRAME)
        logo_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    
    def _CreateTitle(self) -> None:
        """Erstellt und platziert den Anwendungstitel"""
        self.title_label = tk.Label(
            self,
            font=Fonts.HEADER,
            bg=AppColors.TOP_FRAME,
            fg=AppColors.KU_COLOR,
            text=AppConfig.MAIN_TITLE
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')
    
    def _CreateClock(self) -> None:
        """Erstellt und platziert die Uhr"""
        self.time_label = tk.Label(
            self,
            font=Fonts.CLOCK,
            bg=AppColors.TOP_FRAME,
            fg=AppColors.KU_COLOR
        )
        self.time_label.grid(row=0, column=2, padx=20, pady=10, sticky='e')
        self.UpdateClock()
    
    def UpdateClock(self) -> None:
        """Aktualisiert das Zeit-Label mit der aktuellen Uhrzeit"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        # Aktualisiere die Uhr jede Sekunde
        self.after(1000, self.UpdateClock)