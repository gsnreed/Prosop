import json
import pandas as pd
import re
from pathlib import Path
from typing import List, Dict, Any
from Romans import Roman
import openpyxl

if __name__ == '__main__':
    wb = openpyxl.load_workbook('Prosopographischer Katalog.xlsx')

    sheet = wb['Tabelle1']

    data = []
    for row in sheet.rows:
        row_data = []
        for cell in row:
            row_data.append(cell.value.replace('\n', '') if cell.value != None else '')
        data.append(row_data)
    
    result = {"Römer": []}
    for row in data[1:]:
        if row[0] != '':
            person = {
                "Name": row[0],
                "Geburtsdatum": row[1],
                "Sterbedatum": row[2],
                "Todesursache": row[3],
                "Familie": row[4],
                "Vorfahren": row[5],
                "Verlobung": row[6],
                "Häufigkeit Heirat": row[7],
                "Männer": [row[8],
                           row[9],
                           row[10],
                           row[11],
                           row[12]],
                "Anzahl Kinder": row[13],
                "Kinder": [row[14],
                           row[15],
                           row[16],
                           row[17],
                           row[18],
                           row[19]],
                "Individuelle Besonderheiten": {
                    "Auftreten": row[20],
                    "Kleidung": row[21],
                    "Schmuck": ""
                },
                "Inszenierung": {
                    "Öffentlich": row[22],
                    "Privat": row[23]
                },
                "Ehrungen": {
                    "Augusta-Titel": row[24],
                    "Carpentum-Recht": row[25],
                    "Weitere": row[26]
                },
                "Quellen": {
                    "Divinisierung": row[27],
                    "Bestattung": row[28],
                    "Archäologische Quellen": row[29],
                    "Münzen": row[30],
                    "Inschriften": row[31],
                    "Literarische Quellen": {
                        "Autor": row[32],
                        "Werk": row[33]
                    }
                }
            }
            result["Römer"].append(person)
    
    with open('./romans.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)