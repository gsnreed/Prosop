import tkinter as tk
import sys
import os

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors

class BaseContentFrame(tk.Frame):
    """Basisklasse für alle Content-Frames"""
    
    def __init__(self, parent) -> None:
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
        self.CreateUi()
    
    def CreateUi(self) -> None:
        """Erstellt die UI-Komponenten (von Unterklassen zu überschreiben)"""
        pass
    
    def UpdateData(self, data=None) -> None:
        """Aktualisiert die Daten im Frame (von Unterklassen zu überschreiben)"""
        pass
    