import logging
logging.basicConfig(filename='log.log', 
                    level=logging.NOTSET,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S'
                    )
logger = logging.getLogger(__name__)

class Roman:
    def __init__(self, name: str, **kwargs: dict) -> None:
        logger.info(f"Erstelle neues Roman-Objekt mit Name '{name}'.")
        self.__properties = {}
        self.__properties["Name"] = name

        for key, value in kwargs.items():
            self.__properties[key] = value 

    def __getitem__(self, item: str):
        logger.debug(f"Lese Eigenschaft '{item}' aus Roman-Objekt '{self.__properties['Name']}'.")
        return self.__properties[item]
    
    def get(self, item: str, default: str):
        logger.debug(f"Lese Eigenschaft '{item}' aus Roman-Objekt '{self.__properties['Name']}' mit Defaultwert '{default}'.")
        return self.__properties.get(item, default)
    
    @property
    def properties(self):
        logger.debug(f"Lese alle Eigenschaften aus Roman-Objekt '{self.__properties['Name']}'.")
        return self.__properties
    
    def __delitem__(self, item: str):
        logger.info(f"Lösche Eigenschaft '{item}' aus Roman-Objekt '{self.__properties['Name']}'.")
        del self.__properties[item]

    def __repr__(self):
        logger.debug(f"Erstelle Repräsentation von Roman-Objekt '{self.__properties['Name']}'.")
        return str(self.__properties)

    def __str__(self):
        logger.debug(f"Erstelle Zeichenkette von Roman-Objekt '{self.__properties['Name']}'.")
        s = ''
        for key, value in self.__properties.items():
            s += f'{key}: {value}\n'
        return s[:-1:]

    def roman_to_dict(self):
        logger.info(f"Konvertiere Roman-Objekt '{self.__properties['Name']}' zu Dictionary")
        # Implementierung fehlt noch
        pass

    @staticmethod
    def dict_to_roman():
        logger.info(f"Konvertiere Dictionary zu Roman-Objekt ")
        # Implementierung fehlt noch
        pass

if __name__ == '__main__':
    r = Roman('Test', fhsdj = 'fsdf', tt = 5)
    print(repr(r))