import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
import webbrowser
import re
import math
import random

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.commands import AddRomanCommand, EditRomanCommand, RemoveRomanCommand
from utils.config import AppColors, Fonts, UIConstants, Icons, Messages
from ui.frames.content.base_content import BaseContentFrame
from data.models.roman import Roman
from utils.logger import logger

class TimelineFrame(BaseContentFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__app = self.master.master
        self.__filtered_romans = self.process_romans_for_timeline(self.__app.romans)
        self.start_year = -100
        self.end_year = 100
        self.CreateUi()
    
    def CreateUi(self):
        # Hauptcontainer Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hauptcontainer für bessere Trennung
        main_container = tk.Frame(self, bg=AppColors.BACKGROUND)
        main_container.grid(row=0, column=0, sticky=tk.NSEW)
        main_container.rowconfigure(0, weight=0)  # Header
        main_container.rowconfigure(1, weight=0)  # Timeline
        main_container.columnconfigure(0, weight=1)

        # ========== HEADER ==========
        top_container = tk.Frame(main_container, bg=AppColors.BACKGROUND)
        top_container.grid(row=0, column=0, sticky=tk.NSEW, padx=20, pady=(20, 10))
        
        top_frame = tk.Frame(top_container, bg=AppColors.CONTENT_FRAME, relief=tk.RAISED, bd=1)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(top_frame, bg=AppColors.KU_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=AppColors.KU_COLOR)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_frame = tk.Frame(header_content, bg=AppColors.KU_COLOR)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        header_label = tk.Label(
            title_frame, 
            text=f'{Icons.TIMELINE} Zeitstrahl', 
            font=Fonts.HEADER_LARGE, 
            bg=AppColors.KU_COLOR, 
            fg=AppColors.BUTTON_PRIMARY_FG
        )
        header_label.pack(side=tk.LEFT)

        # ========== YEAR RANGE CONTROLS IN HEADER ==========
        range_container = tk.Frame(header_content, bg=AppColors.KU_COLOR)
        range_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Von Jahr
        start_frame = tk.Frame(range_container, bg=AppColors.SEARCH_BG, relief=tk.RIDGE, bd=1)
        start_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        start_label = tk.Label(
            start_frame,
            text="Von:",
            bg=AppColors.SEARCH_BG,
            fg=AppColors.SEARCH_FG,
            font=Fonts.INPUT
        )
        start_label.pack(side=tk.LEFT, padx=(UIConstants.PADDING_SMALL, 2))
        
        self.start_var = tk.StringVar(value=str(self.start_year))
        start_entry = tk.Entry(
            start_frame,
            textvariable=self.start_var,
            width=8,
            font=Fonts.INPUT,
            fg=AppColors.SEARCH_FG,
            bg=AppColors.SEARCH_BG,
            bd=0,
            insertbackground=AppColors.SEARCH_FG
        )
        start_entry.pack(side=tk.LEFT, padx=(0, UIConstants.PADDING_SMALL))
        start_entry.bind("<KeyRelease>", self.update_range)
        
        # Bis Jahr
        end_frame = tk.Frame(range_container, bg=AppColors.SEARCH_BG, relief=tk.RIDGE, bd=1)
        end_frame.pack(side=tk.LEFT)
        
        end_label = tk.Label(
            end_frame,
            text="Bis:",
            bg=AppColors.SEARCH_BG,
            fg=AppColors.SEARCH_FG,
            font=Fonts.INPUT
        )
        end_label.pack(side=tk.LEFT, padx=(UIConstants.PADDING_SMALL, 2))
        
        self.end_var = tk.StringVar(value=str(self.end_year))
        end_entry = tk.Entry(
            end_frame,
            textvariable=self.end_var,
            width=8,
            font=Fonts.INPUT,
            fg=AppColors.SEARCH_FG,
            bg=AppColors.SEARCH_BG,
            bd=0,
            insertbackground=AppColors.SEARCH_FG
        )
        end_entry.pack(side=tk.LEFT, padx=(0, UIConstants.PADDING_SMALL))
        end_entry.bind("<KeyRelease>", self.update_range)
        
        # ========== TIMELINE BEREICH ==========
        timeline_container = tk.Frame(main_container, bg=AppColors.BACKGROUND)
        timeline_container.grid(row=1, column=0, sticky=tk.EW, padx=20, pady=10)
        
        timeline_frame = tk.Frame(timeline_container, bg=AppColors.CONTENT_FRAME, relief=tk.RAISED, bd=1)
        timeline_frame.pack(fill=tk.X)
        
        # Timeline erstellen (kompakter)
        self.timeline = ModernTimeline(timeline_frame, self.start_year, self.end_year)

        # ========== SPACER FÜR ABSTAND ==========
        spacer = tk.Frame(main_container, bg=AppColors.BACKGROUND, height=30)
        spacer.grid(row=2, column=0, sticky=tk.EW)
        spacer.pack_propagate(False)

        # ========== CONTENT BEREICH (RÖMER) ==========
        content_container = tk.Frame(main_container, bg=AppColors.BACKGROUND)
        content_container.grid(row=3, column=0, sticky=tk.NSEW, padx=20, pady=(0, 20))
        content_container.rowconfigure(0, weight=1)
        content_container.columnconfigure(0, weight=1)
        
        # Content Frame
        content_frame = tk.Frame(content_container, bg=AppColors.CONTENT_FRAME, relief=tk.RAISED, bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Beispiel-Events hinzufügen
        self.add_sample_events(True)
    
    
    def add_sample_events(self, drawEvents = True):
        # Beispiel-
        """ 🏛️ Politisch (rot/orange): Kriege, Machtwechsel, Krisen
            👑 Herrschaft (blau/lila): Kaiser, wichtige Regenten
            ⚔️ Militär (grün): Siege, Eroberungen, Schlachten
            🏗️ Kultur (gelb): Bauwerke, Gesetze, Religion
            📉 Niedergang (grau): Krisen, Fall des Reichs
        """
        events = [
            # Frühe Römische Geschichte
            (-753, "Gründung Roms", "#E74C3C", 1),
            (-509, "Römische Republik", "#3498DB", 2),
            (-390, "Gallier erobern Rom", "#E67E22", 1),
            
            # Expansion und Kriege
            (-264, "1. Punischer Krieg", "#9B59B6", 3),
            (-218, "Hannibal überquert Alpen", "#E67E22", 1),
            (-202, "Schlacht von Zama", "#27AE60", 2),
            (-146, "Zerstörung Karthagos", "#E74C3C", 1),
            (-133, "Gracchen-Krise", "#F39C12", 3),
            
            # Späte Republik
            (-107, "Marius Heeresreform", "#3498DB", 2),
            (-88, "Sullas Marsch auf Rom", "#E74C3C", 1),
            (-73, "Spartacus-Aufstand", "#E67E22", 3),
            (-60, "1. Triumvirat", "#9B59B6", 2),
            (-58, "Caesar in Gallien", "#27AE60", 1),
            (-49, "Caesar überschreitet Rubikon", "#E74C3C", 3),
            (-44, "Caesar ermordet", "#FF6B6B", 1),
            (-31, "Schlacht bei Actium", "#27AE60", 2),
            
            # Kaiserzeit - Früh
            (-27, "Augustus wird Kaiser", "#F39C12", 1),
            (-9, "Varusschlacht", "#E74C3C", 3),
            (0, "Christi Geburt", "#F39C12", 2),
            (14, "Tod des Augustus", "#95A5A6", 2),
            (37, "Caligula Kaiser", "#E67E22", 1),
            (41, "Claudius Kaiser", "#3498DB", 3),
            (54, "Nero Kaiser", "#9B59B6", 2),
            (64, "Brand von Rom", "#E74C3C", 1),
            (69, "Vierkaiserjahr", "#E67E22", 3),
            (79, "Vesuvausbruch", "#E74C3C", 2),
            (80, "Kolosseum eröffnet", "#F39C12", 1),
            
            # Goldenes Zeitalter
            (98, "Trajan Kaiser", "#2ECC71", 2),
            (101, "1. Dakerkrieg", "#27AE60", 1),
            (117, "Hadrian Kaiser", "#3498DB", 3),
            (122, "Hadrianswall", "#27AE60", 2),
            (138, "Antoninus Pius", "#2ECC71", 1),
            (161, "Mark Aurel Kaiser", "#9B59B6", 3),
            
            # Krise und Spätzeit
            (212, "Constitutio Antoniniana", "#F39C12", 2),
            (235, "Soldatenkaiserzeit", "#E67E22", 1),
            (284, "Diokletian Kaiser", "#3498DB", 3),
            (303, "Christenverfolgung", "#E74C3C", 2),
            (306, "Konstantin Kaiser", "#27AE60", 1),
            (313, "Mailänder Edikt", "#2ECC71", 3),
            (330, "Konstantinopel gegründet", "#F39C12", 2),
            (378, "Schlacht von Adrianopel", "#E74C3C", 1),
            (395, "Reichsteilung", "#E67E22", 3),
            (410, "Westgoten erobern Rom", "#E74C3C", 2),
            (455, "Vandalen plündern Rom", "#E67E22", 1),
            (476, "Fall Westroms", "#95A5A6", 3),
            (527, "Justinian Kaiser", "#3498DB", 2),
            (1453, "Fall Konstantinopels", "#E74C3C", 1)
        ]
        
        for year, title, color, height in events:
            if self.start_year <= year <= self.end_year and drawEvents:
                self.timeline.add_event(year, title, color, height)
    
    def update_range(self, event=None):
        try:
            start_text = self.start_var.get().strip()
            end_text = self.end_var.get().strip()
            
            # Leere Felder ignorieren
            if not start_text or not end_text:
                return
            
            # Nur Zahlen und Minus erlauben
            if not start_text.lstrip('-').isdigit() or not end_text.lstrip('-').isdigit():
                return
                
            start_year = int(start_text)
            end_year = int(end_text)
            
            # Sinnvolle Grenzen prüfen
            if start_year < -5000 or start_year > 3000:
                return
            if end_year < -5000 or end_year > 3000:
                return
            if start_year >= end_year:
                return
            
            # Alles OK - Werte übernehmen
            self.start_year = start_year
            self.end_year = end_year
            print(f"Neuer Bereich: {self.start_year} bis {self.end_year}")

            # Timeline aktualisieren
            if hasattr(self, 'timeline'):
                self.timeline.start_year = self.start_year
                self.timeline.end_year = self.end_year
                self.timeline.events = []  # Events zurücksetzen
                self.timeline.draw_timeline()
                self.add_sample_events()  # Events neu hinzufügen
            
        except:
            # Bei jedem Fehler einfach ignorieren
            pass
    
    def parse_year_to_integer(self, year_string):
        """
        Konvertiert verschiedene Jahresformate zu Integer-Werten.
        
        Args:
            year_string (str): Jahr als String (z.B. "34 v. Chr.", "80 n. Chr.", "um 70 v. Chr.")
        
        Returns:
            int or None: Jahr als Integer (negative Werte für v.Chr.) oder None falls nicht parsbar
        
        Examples:
            "34 v. Chr." -> -34
            "80 n. Chr." -> 80
            "um 70 v. Chr." -> -70
            "vor dem Jahr 54 v. Chr." -> -54
            "" -> None
            "unbekannt" -> None
        """
        if not year_string or not isinstance(year_string, str):
            return None
        
        # String bereinigen und normalisieren
        year_string = year_string.strip().lower()
        
        if not year_string or year_string in ['unbekannt', 'unknown', '']:
            return None
        
        try:
            # Verschiedene Muster für Jahresangaben
            patterns = [
                # Standard Formate
                r'(\d+)\s*v\.?\s*chr\.?',           # "34 v. Chr.", "34 v.Chr.", "34 vChr"
                r'(\d+)\s*n\.?\s*chr\.?',           # "80 n. Chr.", "80 n.Chr.", "80 nChr"
                r'(\d+)\s*v\.?\s*c\.?',             # "34 v. C.", "34 vC"
                r'(\d+)\s*a\.?\s*d\.?',             # "80 A.D.", "80 AD"
                r'(\d+)\s*b\.?\s*c\.?',             # "34 B.C.", "34 BC"
                
                # Mit Präfixen
                r'um\s+(\d+)\s*v\.?\s*chr\.?',      # "um 70 v. Chr."
                r'ca\.?\s*(\d+)\s*v\.?\s*chr\.?',   # "ca. 70 v. Chr."
                r'etwa\s+(\d+)\s*v\.?\s*chr\.?',    # "etwa 70 v. Chr."
                r'vor\s+dem\s+jahr\s+(\d+)\s*v\.?\s*chr\.?',  # "vor dem Jahr 54 v. Chr."
                r'nach\s+(\d+)\s*v\.?\s*chr\.?',    # "nach 54 v. Chr."
                
                r'um\s+(\d+)\s*n\.?\s*chr\.?',      # "um 70 n. Chr."
                r'ca\.?\s*(\d+)\s*n\.?\s*chr\.?',   # "ca. 70 n. Chr."
                r'etwa\s+(\d+)\s*n\.?\s*chr\.?',    # "etwa 70 n. Chr."
                r'nach\s+(\d+)\s*n\.?\s*chr\.?',    # "nach 70 n. Chr."
                
                # Nur Zahlen (Heuristik anwenden)
                r'^(\d+)$'                          # "70" (wird als v.Chr. interpretiert wenn < 100)
            ]
            
            # Durch alle Muster iterieren
            for pattern in patterns:
                match = re.search(pattern, year_string)
                if match:
                    year_num = int(match.group(1))
                    
                    # Bestimmen ob v.Chr. oder n.Chr.
                    if any(indicator in year_string for indicator in ['v.chr', 'v. chr', 'b.c', 'bc']):
                        return -year_num  # v.Chr. = negative Zahl
                    elif any(indicator in year_string for indicator in ['n.chr', 'n. chr', 'a.d', 'ad']):
                        return year_num   # n.Chr. = positive Zahl
                    else:
                        # Heuristik für reine Zahlen
                        # Für römische Zeit: Zahlen < 100 meist v.Chr., >= 100 meist n.Chr.
                        if year_num < 100:
                            return -year_num  # Wahrscheinlich v.Chr.
                        else:
                            return year_num   # Wahrscheinlich n.Chr.
            
            # Spezielle Behandlung für Bereiche
            range_patterns = [
                r'(\d+)\s*-\s*(\d+)\s*v\.?\s*chr\.?',  # "50-40 v. Chr."
                r'(\d+)\s*-\s*(\d+)\s*n\.?\s*chr\.?',  # "50-60 n. Chr."
                r'zwischen\s+(\d+).*?(\d+)\s*v\.?\s*chr\.?',  # "zwischen 50 und 40 v. Chr."
            ]
            
            for pattern in range_patterns:
                match = re.search(pattern, year_string)
                if match:
                    year1, year2 = int(match.group(1)), int(match.group(2))
                    avg_year = (year1 + year2) // 2  # Durchschnitt nehmen
                    
                    if any(indicator in year_string for indicator in ['v.chr', 'v. chr', 'b.c', 'bc']):
                        return -avg_year
                    else:
                        return avg_year
            
        except (ValueError, AttributeError):
            pass
        
        return None

    def extract_birth_death_years(self, roman_data):
        """
        Extrahiert und konvertiert Geburts- und Sterbejahre aus römischen Personendaten.
        
        Args:
            roman_data (dict): Dictionary mit Personendaten
        
        Returns:
            tuple: (birth_year: int|None, death_year: int|None)
        """
        birth_year = self.parse_year_to_integer(roman_data.get("Geburtsdatum", ""))
        death_year = self.parse_year_to_integer(roman_data.get("Sterbedatum", ""))
        
        return birth_year, death_year

    def process_romans_for_timeline(self, romans_list):
        """
        Verarbeitet eine Liste von römischen Personen für den Zeitstrahl.
        Filtert Personen ohne gültige Geburtsdaten heraus.
        
        Args:
            romans_list (list): Liste von Personendictionaries
        
        Returns:
            list: Liste von verarbeiteten Personen mit gültigen Jahresdaten
        """
        processed_romans = []
        skipped_count = 0
        
        for roman_data in romans_list:
            birth_year, death_year = self.extract_birth_death_years(roman_data)
            
            # Nur Personen mit mindestens Geburtsjahr verarbeiten
            if birth_year is not None:
                # Geschätztes Sterbejahr falls nicht vorhanden
                if death_year is None:
                    # Durchschnittliche Lebenserwartung in der Antike: 50-60 Jahre
                    death_year = birth_year + 55
                    estimated_death = True
                else:
                    estimated_death = False
                
                # Validierung: Sterbejahr muss nach Geburtsjahr liegen
                if death_year <= birth_year:
                    death_year = birth_year + 55
                    estimated_death = True
                
                processed_person = {
                    'name': roman_data.get('Name', 'Unbekannt'),
                    'birth_year': birth_year,
                    'death_year': death_year,
                    'estimated_death': estimated_death,
                    'original_birth_string': roman_data.get("Geburtsdatum", ""),
                    'original_death_string': roman_data.get("Sterbedatum", ""),
                    'description': roman_data.get("Beschreibung", ""),
                    'raw_data': roman_data
                }
                
                processed_romans.append(processed_person)
            else:
                skipped_count += 1
                print(f"Übersprungen - {roman_data.get('Name', 'Unbekannt')}: "
                    f"Geburtsdatum '{roman_data.get('Geburtsdatum', '')}' nicht parsbar")
        
        print(f"Verarbeitet: {len(processed_romans)} Personen, Übersprungen: {skipped_count}")
        return processed_romans
    
class ModernTimeline:
    def __init__(self, parent, start_year, end_year):
        self.parent = parent
        self.start_year = start_year
        self.end_year = end_year
        self.events = []
        self.persons = []
        
        self.create_timeline()
    
    def create_timeline(self):
        # Canvas für Timeline (kompakter)
        self.canvas = tk.Canvas(
            self.parent,
            bg=AppColors.CONTENT_FRAME,
            highlightthickness=0,
            height=150  # Kleiner als vorher
        )
        self.canvas.pack(fill=tk.X, padx=20, pady=15)
        
        # Horizontale Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.canvas.configure(xscrollcommand=scrollbar.set)
        
        self.draw_timeline()
    
    def draw_timeline(self):
        self.canvas.delete("all")
        
        canvas_height = 150
        timeline_y = canvas_height // 2
        
        # Timeline-Linie
        total_years = self.end_year - self.start_year
        pixels_per_year = max(30, 1500 / total_years)
        timeline_width = total_years * pixels_per_year
        
        # Hauptlinie
        self.canvas.create_line(
            50, timeline_y, timeline_width + 50, timeline_y,
            fill=AppColors.KU_COLOR, width=3
        )
        
        # Jahr-Markierungen
        year_step = 1
        
        for year in range(self.start_year, self.end_year + 1, year_step):
            x = 50 + (year - self.start_year) * pixels_per_year

            if year % 5 == 0:
                # Markierung
                self.canvas.create_line(
                    x, timeline_y - 10, x, timeline_y + 10,
                    fill=AppColors.KU_COLOR, width=2
                )
                
                # Jahr-Label
                self.canvas.create_text(
                    x, timeline_y + 25,
                    text=str(year),
                    font=Fonts.STANDARD,
                    fill=AppColors.KU_COLOR
                )
            else:
                x = 50 + (year - self.start_year) * pixels_per_year

                # Markierung
                self.canvas.create_line(
                    x, timeline_y - 5, x, timeline_y + 5,
                    fill=AppColors.KU_COLOR, width=1
                )
        
        # Events zeichnen
        self.draw_events(pixels_per_year, timeline_y)
        
        # Scroll-Region setzen
        self.canvas.configure(scrollregion=(0, 0, timeline_width + 100, canvas_height))
    
    def draw_events(self, pixels_per_year, timeline_y):
        for i, event in enumerate(self.events):
            x = 50 + (event['year'] - self.start_year) * pixels_per_year
            
            # Event-Punkt (kleiner)
            radius = 6
            self.canvas.create_oval(
                x - radius, timeline_y - radius,
                x + radius, timeline_y + radius,
                fill=event.get('color', AppColors.ACCENT),
                outline=AppColors.BACKGROUND,
                width=2
            )
            
            # Event-Label (kompakter)
            y_offset = -60
            label_y = timeline_y + y_offset
            
            # Event-Linie
            self.canvas.create_line(
                x, timeline_y + (radius if y_offset > 0 else -radius),
                x, label_y + event['height'] * 15,
                fill=event.get('color', AppColors.ACCENT),
                width=1
            )
            
            # Event-Text
            self.canvas.create_text(
                x, label_y + event['height'] * 15 - 10,
                text=event['title'],
                font=Fonts.STANDARD,
                fill=AppColors.KU_COLOR,
                justify=tk.CENTER
            )
    
    def add_event(self, year, title, color=None, height=1):
        self.events.append({
            'year': year,
            'title': title,
            'color': color or AppColors.ACCENT,
            'height': height
        })
        self.draw_timeline()
    
    def load_women_from_list(self, women_list):
        """Frauen aus deiner Liste laden - angepasst für deine Datenstruktur"""
        for woman in women_list:
            # Die wichtigen Daten extrahieren
            name = woman.get('name', '')
            birth_year = woman.get('birth_year', '')
            death_year = woman.get('death_year', '')
            description = woman.get('description', '')
            
            # Falls description leer ist, aus raw_data nehmen
            if not description and 'raw_data' in woman:
                raw_desc = woman['raw_data'].get('Beschreibung', '')
                if raw_desc:
                    description = raw_desc
                else:
                    # Fallback: Familienbemerkungen verwenden
                    description = woman['raw_data'].get('Familienbemerkungen', 'Römische Frau')
            
            # Random helle Farbe
            color = self.get_random_bright_color()
            
            # Nur hinzufügen wenn Name und Jahre vorhanden und im Zeitbereich
            if (name and birth_year is not None and death_year is not None and 
                death_year >= self.start_year and birth_year <= self.end_year):
                
                # Zusätzliche Info für Tooltip
                extra_info = self.extract_extra_info(woman)
                
                self.add_person(name, birth_year, death_year, color, description, extra_info)

    def extract_extra_info(self, woman):
        """Zusätzliche interessante Infos extrahieren"""
        info = {}
        
        if 'raw_data' in woman:
            raw = woman['raw_data']
            
            # Geschätzte Todesdaten markieren
            if woman.get('estimated_death', ''):
                info['estimated_death'] = True
            
            # Original Datumsstrings
            if woman.get('original_birth_string', ''):
                info['birth_string'] = woman['original_birth_string']
            if woman.get('original_death_string', ''):
                info['death_string'] = woman['original_death_string']
            
            # Familie
            if raw.get('Familienbemerkungen', ''):
                info['family'] = raw['Familienbemerkungen']
            
            # Ehen
            if raw.get('Anzahl Ehen', ''):
                info['marriages'] = raw['Anzahl Ehen']
            
            # Kinder
            if raw.get('Anzahl Kinder', ''):
                info['children'] = raw['Anzahl Kinder']
            
            # Augusta-Titel
            if raw.get('Ehrungen', {}).get('Augusta-Titel-Status', '') == 'Ja':
                info['augusta'] = True
        
        return info

    def add_person(self, name, birth_year, death_year, color, description="", extra_info=None):
        """Person hinzufügen - erweitert"""
        self.persons.append({
            'name': name,
            'birth': birth_year,
            'death': death_year,
            'color': color,
            'description': description,
            'extra_info': extra_info or {}
        })
        self.draw_timeline()

    def show_woman_tooltip(self, event, woman):
        """Erweiterte Tooltips mit deinen Daten"""
        # Basis-Info
        name = woman['name']
        birth = woman['birth']
        death = woman['death']
        lifespan = death - birth
        description = woman['description']
        extra = woman.get('extra_info', {})
        
        # Tooltip-Text zusammenbauen
        tooltip_lines = [f"👩 {name}"]
        
        # Geburt/Tod mit Original-Strings falls vorhanden
        if extra.get('birth_string', ''):
            tooltip_lines.append(f"📅 {extra['birth_string']} - {death}")
        else:
            tooltip_lines.append(f"📅 {birth} - {death}")
        
        tooltip_lines.append(f"⏳ {lifespan} Jahre")
        
        # Geschätzter Tod markieren
        if extra.get('estimated_death', ''):
            tooltip_lines.append("⚠️ Sterbedatum geschätzt")
        
        # Familie
        if extra.get('family', ''):
            family_text = extra['family'][:60] + "..." if len(extra['family']) > 60 else extra['family']
            tooltip_lines.append(f"👨‍👩‍👧‍👦 {family_text}")
        
        # Ehen und Kinder
        if extra.get('marriages', ''):
            tooltip_lines.append(f"💒 {extra['marriages']}")
        if extra.get('children', ''):
            tooltip_lines.append(f"👶 {extra['children']}")
        
        # Augusta-Titel
        if extra.get('augusta', ''):
            tooltip_lines.append("👑 Augusta-Titel")
        
        # Beschreibung (falls vorhanden)
        if description and description != 'Römische Frau':
            desc_text = description[:80] + "..." if len(description) > 80 else description
            tooltip_lines.append(f"📝 {desc_text}")
        
        tooltip_text = "\n".join(tooltip_lines)
        
        # Tooltip positionieren
        tooltip_x = min(event.x + 15, self.canvas.winfo_width() - 250)
        tooltip_y = max(event.y - 50, 10)
        
        self.tooltip = self.canvas.create_text(
            tooltip_x, tooltip_y,
            text=tooltip_text,
            font=("Arial", 9),
            fill="#2C3E50",
            anchor="nw",
            width=240
        )
        
        # Schöner Hintergrund
        bbox = self.canvas.bbox(self.tooltip)
        if bbox:
            self.tooltip_bg = self.canvas.create_rectangle(
                bbox[0] - 10, bbox[1] - 8,
                bbox[2] + 10, bbox[3] + 8,
                fill="#FFFFFF",
                outline=woman['color'],
                width=3
            )
            self.canvas.tag_lower(self.tooltip_bg)

    def draw_persons(self, pixels_per_year, start_y):
        """Frauen zeichnen - mit Spezial-Markierungen"""
        sorted_women = sorted(self.persons, key=lambda x: x['birth'])
        
        row_height = 22
        row_spacing = 3
        max_rows = 8
        current_row = 0
        
        # Label
        self.canvas.create_text(
            15, start_y - 10,
            text="👩 Römische Frauen",
            font=("Arial", 10, "bold"),
            fill=AppColors.TEXT_PRIMARY,
            anchor="e"
        )
        
        for woman in sorted_women:
            if (woman['death'] >= self.start_year and 
                woman['birth'] <= self.end_year):
                
                current_y = start_y + (current_row * (row_height + row_spacing))
                
                # X-Koordinaten
                birth_x = 50 + max(0, (woman['birth'] - self.start_year)) * pixels_per_year
                death_x = 50 + min(self.timeline_width, (woman['death'] - self.start_year)) * pixels_per_year
                
                # Balken
                rect_id = self.canvas.create_rectangle(
                    birth_x, current_y + 2,
                    death_x, current_y + row_height - 2,
                    fill=woman['color'],
                    outline="white",
                    width=1
                )
                
                # Spezial-Markierungen
                extra = woman.get('extra_info', {})
                
                # Augusta-Titel: Krone-Symbol
                if extra.get('augusta', ''):
                    self.canvas.create_text(
                        birth_x - 15, current_y + row_height//2,
                        text="👑",
                        font=("Arial", 10),
                        anchor="center"
                    )
                
                # Geschätzter Tod: gestrichelte Linie am Ende
                if extra.get('estimated_death', ''):
                    for i in range(0, row_height-4, 3):
                        self.canvas.create_line(
                            death_x - 5, current_y + 2 + i,
                            death_x - 5, current_y + 2 + i + 1,
                            fill="white", width=2
                        )
                
                # Hover-Effekte
                self.canvas.tag_bind(rect_id, "<Enter>", 
                    lambda e, w=woman: self.show_woman_tooltip(e, w))
                self.canvas.tag_bind(rect_id, "<Leave>", 
                    lambda e: self.hide_tooltip())
                
                # Name auf Balken
                text_x = (birth_x + death_x) / 2
                if death_x - birth_x > 70:
                    self.canvas.create_text(
                        text_x, current_y + row_height//2,
                        text=woman['name'],
                        font=("Arial", 8, "bold"),
                        fill="white",
                        justify=tk.CENTER
                    )
                
                current_row = (current_row + 1) % max_rows
    
    def get_random_bright_color(self):
        """Zufällige helle Komplementärfarbe"""
        bright_colors = [
            "#FF6B9D",  # Helles Pink
            "#4ECDC4",  # Türkis
            "#45B7D1",  # Himmelblau
            "#96CEB4",  # Mintgrün
            "#FFEAA7",  # Helles Gelb
            "#DDA0DD",  # Plum
            "#98D8C8",  # Aquamarin
            "#F7DC6F",  # Pastellgelb
            "#BB8FCE",  # Lavendel
            "#85C1E9",  # Babyblau
            "#F8C471",  # Pfirsich
            "#82E0AA",  # Hellgrün
            "#F1948A",  # Lachs
            "#AED6F1",  # Pulverblau
            "#D7BDE2",  # Flieder
            "#A9DFBF",  # Salbeigrün
            "#FAD7A0",  # Champagner
            "#D5A6BD",  # Dusty Rose
            "#A3E4D7",  # Seafoam
            "#F9E79F"   # Vanille
        ]
        return random.choice(bright_colors)