import tkinter as tk
from tkinter import ttk
import os
import sys

# Projektverzeichnis zum Suchpfad hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Absolute Importe
from Objects.Config import AppColors, AppConfig

class ContentManager:
    """Verwaltet die verschiedenen Content-Frames"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_frame = None
        
        # Frame-Mapping
        self.frames = {
            'Startseite': StartSeiteFrame,
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

class StartSeiteFrame(BaseContentFrame):
    def __init__(self, parent):
        super().__init__(parent)

class ListenViewFrame(BaseContentFrame):
    def __init__(self, parent):
        super().__init__(parent)

class ErstellungPersonFrame(BaseContentFrame):
    def __init__(self, parent):
        super().__init__(parent)

