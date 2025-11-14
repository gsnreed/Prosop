import sys
import os
import tkinter as tk

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ui.frames.content.start import StartseiteFrame
from ui.frames.content.default import DefaultContentFrame
from ui.frames.content.create import CreateFrame
from ui.frames.content.timeline import TimelineFrame

class ContentManager:
    """Verwaltet die verschiedenen Content-Frames"""
    
    def __init__(self, parent) -> None:
        self.__parent = parent
        self.__current_frame = None
        
        # Frame-Mapping für alle Navigation-Optionen und ihre Submenu-Items
        self.__frames = {
            # Hauptnavigation
            'Startseite': StartseiteFrame,
            
            # Ansicht Submenu
            'Ansicht - Tabelle': DefaultContentFrame,
            'Ansicht - Karte': DefaultContentFrame,
            'Ansicht - Zeitstrahl \n- Überblick': TimelineFrame,
            
            # Erstellung Submenu
            'Erstellung': CreateFrame,
            
            # Literatur Submenu
            'Literatur - Hinzufügen': DefaultContentFrame,
            'Literatur - Verwalten': DefaultContentFrame,

            'Schlagwörter - On-Stage': DefaultContentFrame,
            'Schlagwörter - Off-Stage': DefaultContentFrame,
            'Schlagwörter - Normen &\nRollen': DefaultContentFrame,
            'Schlagwörter - Grenzüberschreitung': DefaultContentFrame,
            
            'Begriffsdefinitionen - Geschlecht': DefaultContentFrame,
            'Begriffsdefinitionen - Normen': DefaultContentFrame,
            'Begriffsdefinitionen - Frauenmacht': DefaultContentFrame
        }
    
    def ShowContent(self, option: str) -> None:
        """Zeigt den Content für die gewählte Option an"""
        # Entferne alten Frame
        if self.__current_frame:
            self.__current_frame.pack_forget()
            self.__current_frame.destroy()
        
        # Bestimme den korrekten Frame-Typ
        if option in self.__frames:
            frame_class = self.__frames[option]
            
            # Unterscheide zwischen Klassen und Dummy-Frames
            if frame_class == DefaultContentFrame:
                self.__current_frame = DefaultContentFrame(self.__parent, option)
            else:
                self.__current_frame = frame_class(self.__parent)
        else:
            # Fallback auf einen generischen Frame
            self.__current_frame = DefaultContentFrame(self.__parent, option)
        
        # Zeige den Frame an
        self.__current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bei Bedarf Daten aktualisieren
        if hasattr(self.__current_frame, 'UpdateData'):
            self.__current_frame.UpdateData()

    @property
    def parent(self):
        return self.__parent
    
    @property
    def current_frame(self):
        return self.__current_frame