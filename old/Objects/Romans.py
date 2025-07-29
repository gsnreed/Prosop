import os
import sys
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from Objects.Logger import *

class Roman:
    def __init__(self, name: str, **kwargs: dict) -> None:
        logger.info(f"Erstelle neues Roman-Objekt mit Name '{name}'.")
        self.__properties = {}
        self.__properties["Name"] = name

        # Verarbeite zuerst die Anzahl der Heiraten und Kinder
        anzahl_heirat = 0
        if "Häufigkeit Heirat" in kwargs:
            häufigkeit = kwargs.get("Häufigkeit Heirat", "")
            if "x Verheiratet" in häufigkeit:
                try:
                    # Extrahiere die Zahl aus z.B. "2x Verheiratet"
                    anzahl_heirat = int(häufigkeit.split("x")[0])
                except ValueError:
                    logger.warning(f"Konnte Häufigkeit der Heirat nicht parsen: {häufigkeit}")
        
        anzahl_kinder = 0
        if "Anzahl Kinder" in kwargs:
            anzahl_kinder_str = kwargs.get("Anzahl Kinder", "")
            if "Kinder" in anzahl_kinder_str:
                try:
                    # Extrahiere die Zahl aus z.B. "2 Kinder"
                    anzahl_kinder = int(anzahl_kinder_str.split()[0])
                except ValueError:
                    logger.warning(f"Konnte Anzahl der Kinder nicht parsen: {anzahl_kinder_str}")
        
        # Verarbeite Männer basierend auf der Anzahl der Heiraten
        if "Männer" in kwargs:
            männer = kwargs.pop("Männer", [])
            if isinstance(männer, list):
                # Kürze die Liste auf die angegebene Anzahl der Heiraten, behalte leere Einträge
                if anzahl_heirat > 0 and len(männer) > anzahl_heirat:
                    logger.info(f"Kürze Männerliste von {len(männer)} auf {anzahl_heirat} Einträge für {name}")
                    männer = männer[:anzahl_heirat]
                
                self.__properties["Männer"] = männer
            elif isinstance(männer, str):
                self.__properties["Männer"] = [männer]
        
        # Verarbeite Kinder basierend auf der Anzahl der Kinder
        if "Kinder" in kwargs:
            kinder = kwargs.pop("Kinder", [])
            if isinstance(kinder, list):
                # Kürze die Liste auf die angegebene Anzahl der Kinder, behalte leere Einträge
                if anzahl_kinder > 0 and len(kinder) > anzahl_kinder:
                    logger.info(f"Kürze Kinderliste von {len(kinder)} auf {anzahl_kinder} Einträge für {name}")
                    kinder = kinder[:anzahl_kinder]
                
                self.__properties["Kinder"] = kinder
            elif isinstance(kinder, str):
                self.__properties["Kinder"] = [kinder]
        
        # Restliche Eigenschaften übernehmen
        for key, value in kwargs.items():
            self.__properties[key] = value

        for key, value in kwargs.items():
            self.__properties[key] = value 

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

if __name__ == '__main__':
    # Pfad zur JSON-Datei
    json_file = "./Datenbank/Romans.json"
    
    if not os.path.exists(json_file):
        print(f"Die Datei {json_file} wurde nicht gefunden.")
        exit(1)
    
    # Lade römische Persönlichkeiten
    romans = load_romans_from_json(json_file)
    
    print(romans)