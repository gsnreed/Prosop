from abc import ABC, abstractmethod
import sys
import os
from typing import List, Any

# Projektwurzel (eine Ebene über dem Skriptverzeichnis)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.models.roman import Roman

class Command(ABC):
    """Basisklasse für alle Command-Objekte im Command-Pattern"""
    
    @abstractmethod
    def Execute(self) -> None:
        """Führt den Befehl aus"""
        pass
    
    @abstractmethod
    def Undo(self) -> None:
        """Macht den Befehl rückgängig"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Beschreibung des Befehls für Logging"""
        pass

class AddRomanCommand(Command):
    """Command zum Hinzufügen eines Romans"""
    
    def __init__(self, romans_list: List[Roman], roman: Roman):
        self.__romans_list = romans_list
        self.__roman = roman
        self.__index = None  # wird bei execute gesetzt
        
    def Execute(self) -> None:
        self.__romans_list.append(self.__roman)
        self.__index = len(self.__romans_list) - 1
        
    def Undo(self) -> None:
        if self.__index is not None and 0 <= self.__index < len(self.__romans_list):
            self.__romans_list.pop(self.__index)
            
    @property
    def description(self) -> str:
        return f"Roman hinzufügen: {self.__roman['Name']}"
    
class RemoveRomanCommand(Command):
    """Command zum Entfernen eines Romans"""
    
    def __init__(self, romans_list: List[Roman], index: int):
        self.__romans_list = romans_list
        self.__index = index
        self.__removed_roman = None  # wird bei execute gespeichert
        
    def Execute(self) -> None:
        # Roman-Objekt speichern, bevor es gelöscht wird
        if 0 <= self.__index < len(self.__romans_list):
            self.__removed_roman = self.__romans_list[self.__index]
            self.__romans_list.pop(self.__index)
        
    def Undo(self) -> None:
        if self.__removed_roman is not None:
            # Füge an der ursprünglichen Position wieder ein
            self.__romans_list.insert(self.__index, self.__removed_roman)
            
    @property
    def description(self) -> str:
        name = self.__removed_roman['Name'] if self.__removed_roman else "Unbekannt"
        return f"Roman entfernen: {name}"
    
class EditRomanCommand(Command):
    """Command zum Bearbeiten eines Romans"""
    
    def __init__(self, roman: Roman, properties: dict):
        self.__roman = roman
        self.__new_properties = properties
        self.__old_properties = None  # wird bei execute gespeichert
        
    def Execute(self) -> None:
        # Speichere den alten Wert für undo
        self.__old_properties = self.__roman.properties.copy()
        # Setze den neuen Wert
        self.__roman.properties= self.__new_properties
        
    def Undo(self) -> None:
        if self.__old_properties is not None:
            self.__roman.properties = self.__old_properties
                
    @property
    def description(self) -> str:
        return f"Roman bearbeiten: {self.__roman['Name']}"
    
class ReplaceRomanCommand(Command):
    """Command zum Ersetzen eines Romans durch eine neue Version"""
    
    def __init__(self, old_roman: Roman, new_roman: Roman):
        self.__old_roman = old_roman
        self.__new_roman = new_roman
        self.__old_properties = None
        
    def Execute(self) -> None:
        # Speichere die alten Eigenschaften
        self.__old_properties = self.__old_roman.properties.copy()
        
        # Ersetze die Eigenschaften des alten Römers mit denen des neuen
        self.__old_roman.properties = self.__new_roman.properties.copy()
        
    def Undo(self) -> None:
        if self.__old_properties is not None:
            # Stelle die alten Eigenschaften wieder her
            self.__old_roman.properties = self.__old_properties
                
    @property
    def description(self) -> str:
        return f"Roman ersetzen: {self.__old_roman['Name']}"