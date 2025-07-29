import os
import sys
import json

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.logger import logger

class Roman:
    def __init__(self, name: str, **kwargs: dict) -> None:
        logger.info(f"Erstelle neues Roman-Objekt mit Name '{name}'.")
        self.__properties = {}
        self.__properties["Name"] = name
        
        # Restliche Eigenschaften übernehmen
        for key, value in kwargs.items():
            self.__properties[key] = value

        for key, value in kwargs.items():
            self.__properties[key] = value 
        
        logger.debug(f"Roman-Objekt mit dem Namen '{self.__properties['Name']}' erstellt.")

    def __getitem__(self, item: str):
        logger.debug(f"Lese Eigenschaft '{item}' aus Roman-Objekt '{self.__properties['Name']}'.")
        return self.__properties[item]
    
    def get(self, item: str, default: any) -> any:
        logger.debug(f"Lese Eigenschaft '{item}' aus Roman-Objekt '{self.__properties['Name']}' mit Defaultwert '{default}'.")
        return self.__properties.get(item, default)
    
    @property
    def properties(self) -> dict[str, any]:
        logger.debug(f"Lese alle Eigenschaften aus Roman-Objekt '{self.__properties['Name']}'.")
        return self.__properties
    
    def __delitem__(self, item: str) -> None:
        logger.info(f"Lösche Eigenschaft '{item}' aus Roman-Objekt '{self.__properties['Name']}'.")
        del self.__properties[item]

    def __repr__(self) -> str:
        logger.debug(f"Erstelle Repräsentation von Roman-Objekt '{self.__properties['Name']}'.")
        return str(self.__properties)

    def __str__(self) -> str:
        logger.debug(f"Erstelle Zeichenkette von Roman-Objekt '{self.__properties['Name']}'.")
        s = ''
        for key, value in self.__properties.items():
            s += f'{key}: {value}\n'
        return s[:-1:]

    def RomanToDict(self) -> dict[str, any]:
        """Konvertiert ein Roman-Objekt in ein Dictionary."""
        logger.info(f"Konvertiere Roman-Objekt '{self.__properties['Name']}' zu Dictionary")
        return self.__properties.copy()

    @staticmethod
    def DictToRoman(data: dict[str, any]) -> 'Roman':
        """Konvertiert ein Dictionary in ein Roman-Objekt."""
        logger.info(f"Konvertiere Dictionary zu Roman-Objekt")
        if "Name" not in data:
            raise ValueError("Das Dictionary muss einen 'Name'-Schlüssel enthalten.")
        
        name = data.pop("Name")
        return Roman(name, **data)


def load_romans_from_json(file_path: str) -> list[Roman]:
    """Lädt römische Persönlichkeiten aus einer JSON-Datei und konvertiert sie in Roman-Objekte."""
    logger.info(f"Lade römische Persönlichkeiten aus JSON-Datei: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        romans = []
        for roman_data in data.get("Römer", []):
            romans.append(Roman.DictToRoman(roman_data))
            
        logger.info(f"Erfolgreich {len(romans)} römische Persönlichkeiten geladen.")
        return romans
    
    except FileNotFoundError:
        logger.error(f"Die Datei {file_path} wurde nicht gefunden.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Fehler beim Parsen der JSON-Datei: {e}")
        return []
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim Laden der römischen Persönlichkeiten: {e}")
        return []


def save_romans_to_json(romans: list[Roman], file_path: str) -> bool:
    """Speichert eine Liste von Roman-Objekten in einer JSON-Datei."""
    logger.info(f"Speichere {len(romans)} römische Persönlichkeiten in JSON-Datei: {file_path}")
    
    try:
        data = {"Römer": [roman.RomanToDict() for roman in romans]}
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        logger.info(f"Römische Persönlichkeiten erfolgreich gespeichert.")
        return True
    
    except Exception as e:
        logger.error(f"Fehler beim Speichern der römischen Persönlichkeiten: {e}")
        return False