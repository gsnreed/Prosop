from typing import List
import os
import sys

# Projektwurzel (eine Ebene über dem Skriptverzeichnis)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.logger import logger
from data.commands import Command

class CommandManager:
    """Verwaltet die Command-History für Undo/Redo-Operationen"""
    
    def __init__(self):
        self.__undo_stack: List[Command] = []
        self.__redo_stack: List[Command] = []
        
    def ExecuteCommand(self, command: Command) -> None:
        """Führt einen Befehl aus und fügt ihn zur History hinzu"""
        command.Execute()
        self.__undo_stack.append(command)
        # Nach Ausführung eines neuen Befehls wird der Redo-Stack geleert
        self.__redo_stack.clear()
        logger.info(f"Befehl ausgeführt: {command.description}")
        
    def Undo(self) -> bool:
        """Macht den letzten Befehl rückgängig"""
        ret = None  # Return value
        if not self.CanUndo():
            logger.info("Nichts zum Rückgängigmachen vorhanden")
            ret = False
        else:
            command = self.__undo_stack.pop()
            command.Undo()
            self.__redo_stack.append(command)
            logger.info(f"Befehl rückgängig gemacht: {command.description}")
            ret = True
        return ret
        
    def Redo(self) -> bool:
        """Stellt den letzten rückgängig gemachten Befehl wieder her"""
        ret = None  # Return value
        if not self.CanRedo():
            logger.info("Nichts zum Wiederherstellen vorhanden")
            ret = False
        else:
            command = self.__redo_stack.pop()
            command.Execute()
            self.__undo_stack.append(command)
            logger.info(f"Befehl wiederhergestellt: {command.description}")
            ret = True
        return ret
        
    def CanUndo(self) -> bool:
        """Prüft, ob es Befehle zum Rückgängigmachen gibt"""
        return len(self.__undo_stack) > 0
        
    def CanRedo(self) -> bool:
        """Prüft, ob es Befehle zum Wiederherstellen gibt"""
        return len(self.__redo_stack) > 0
        
    def Clear(self) -> None:
        """Löscht alle gespeicherten Befehle"""
        self.__undo_stack.clear()
        self.__redo_stack.clear()
        logger.info("Command-History gelöscht")