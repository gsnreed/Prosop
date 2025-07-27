from abc import ABC, abstractmethod
import sys
import os
from typing import List, Any

# Projektverzeichnis zum Suchpfad hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from Objects.Logger import logger
from Objects.Romans import Roman

class Command(ABC):
    """Basisklasse für alle Command-Objekte im Command-Pattern"""
    
    @abstractmethod
    def execute(self) -> None:
        """Führt den Befehl aus"""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Macht den Befehl rückgängig"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Beschreibung des Befehls für Logging"""
        pass

class CommandManager:
    """Verwaltet die Command-History für Undo/Redo-Operationen"""
    
    def __init__(self):
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
        
    def execute_command(self, command: Command) -> None:
        """Führt einen Befehl aus und fügt ihn zur History hinzu"""
        command.execute()
        self.undo_stack.append(command)
        # Nach Ausführung eines neuen Befehls wird der Redo-Stack geleert
        self.redo_stack.clear()
        logger.info(f"Befehl ausgeführt: {command.description}")
        
    def undo(self) -> bool:
        """Macht den letzten Befehl rückgängig"""
        if not self.can_undo():
            logger.info("Nichts zum Rückgängigmachen vorhanden")
            return False
            
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        logger.info(f"Befehl rückgängig gemacht: {command.description}")
        return True
        
    def redo(self) -> bool:
        """Stellt den letzten rückgängig gemachten Befehl wieder her"""
        if not self.can_redo():
            logger.info("Nichts zum Wiederherstellen vorhanden")
            return False
            
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        logger.info(f"Befehl wiederhergestellt: {command.description}")
        return True
        
    def can_undo(self) -> bool:
        """Prüft, ob es Befehle zum Rückgängigmachen gibt"""
        return len(self.undo_stack) > 0
        
    def can_redo(self) -> bool:
        """Prüft, ob es Befehle zum Wiederherstellen gibt"""
        return len(self.redo_stack) > 0
        
    def clear(self) -> None:
        """Löscht alle gespeicherten Befehle"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        logger.info("Command-History gelöscht")

class AddRomanCommand(Command):
    """Command zum Hinzufügen eines Romans"""
    
    def __init__(self, romans_list: List[Roman], roman: Roman):
        self.romans_list = romans_list
        self.roman = roman
        self.index = None  # wird bei execute gesetzt
        
    def execute(self) -> None:
        self.romans_list.append(self.roman)
        self.index = len(self.romans_list) - 1
        
    def undo(self) -> None:
        if self.index is not None and 0 <= self.index < len(self.romans_list):
            self.romans_list.pop(self.index)
            
    @property
    def description(self) -> str:
        return f"Roman hinzufügen: {self.roman['Name']}"


class RemoveRomanCommand(Command):
    """Command zum Entfernen eines Romans"""
    
    def __init__(self, romans_list: List[Roman], index: int):
        self.romans_list = romans_list
        self.index = index
        self.removed_roman = None  # wird bei execute gespeichert
        
    def execute(self) -> None:
        if 0 <= self.index < len(self.romans_list):
            self.removed_roman = self.romans_list[self.index]
            self.romans_list.pop(self.index)
        
    def undo(self) -> None:
        if self.removed_roman is not None:
            # Füge an der ursprünglichen Position wieder ein
            self.romans_list.insert(self.index, self.removed_roman)
            
    @property
    def description(self) -> str:
        name = self.removed_roman['Name'] if self.removed_roman else "Unbekannt"
        return f"Roman entfernen: {name}"


class EditRomanCommand(Command):
    """Command zum Bearbeiten eines Romans"""
    
    def __init__(self, roman: Roman, property_name: str, new_value: Any):
        self.roman = roman
        self.property_name = property_name
        self.new_value = new_value
        self.old_value = None  # wird bei execute gespeichert
        
    def execute(self) -> None:
        # Speichere den alten Wert für undo
        self.old_value = self.roman.get(self.property_name, None)
        # Setze den neuen Wert
        self.roman.properties[self.property_name] = self.new_value
        
    def undo(self) -> None:
        if self.old_value is not None:
            self.roman.properties[self.property_name] = self.old_value
        else:
            # Wenn es den Wert vorher nicht gab, lösche ihn
            if self.property_name in self.roman.properties:
                del self.roman.properties[self.property_name]
                
    @property
    def description(self) -> str:
        return f"Roman bearbeiten: {self.roman['Name']} - {self.property_name}"