import sys
import os
import tkinter as tk

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors
from utils.logger import logger
from ui.frames.content_manager import ContentManager

class ContentFrame(tk.Frame):
    """
    Hauptinhaltsfläche für den ausgewählten Navigationsbereich.
    """
    
    def __init__(self, parent) -> None:
        """Initialisiere den Inhaltsrahmen"""
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
        self.content_manager = ContentManager(self)
        self.current_option = None  # Attribut für die aktuelle Option hinzufügen
    
    def UpdateContent(self, option: str) -> None:
        """Aktualisiert den Inhalt basierend auf der ausgewählten Navigation."""
        self.current_option = option  # Aktualisiere das Attribut
        self.content_manager.ShowContent(option)

        # Ereignis protokollieren
        logger.info(f"Content der Option '{option}' wurde geladen.")