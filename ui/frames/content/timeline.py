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
        main_container.rowconfigure(1, weight=1)  # Timeline + Romans
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
        
        # ========== TIMELINE + ROMANS BEREICH ==========
        timeline_container = tk.Frame(main_container, bg=AppColors.BACKGROUND)
        timeline_container.grid(row=1, column=0, sticky=tk.NSEW, padx=20, pady=10)
        timeline_container.rowconfigure(0, weight=1)
        timeline_container.columnconfigure(0, weight=1)
        
        timeline_frame = tk.Frame(timeline_container, bg=AppColors.CONTENT_FRAME, relief=tk.RAISED, bd=1)
        timeline_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timeline erstellen (erweitert für Römer)
        self.timeline = ModernTimeline(timeline_frame, self.start_year, self.end_year)
        
        # Gefilterte Römer zur Timeline hinzufügen
        self.timeline.load_romans_from_list(self.__filtered_romans)
        
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
                self.timeline.romans = []  # Römer zurücksetzen
                self.timeline.draw_timeline()
                self.timeline.load_romans_from_list(self.__filtered_romans)  # Römer neu laden
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
                    """ else:
                        # Heuristik für reine Zahlen
                        # Für römische Zeit: Zahlen < 100 meist v.Chr., >= 100 meist n.Chr.
                        if year_num < 100:
                            return -year_num  # Wahrscheinlich v.Chr.
                        else:
                            return year_num   # Wahrscheinlich n.Chr. """
            
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
            # DEBUG
            if roman_data.get('Name', '') == 'Tesz':
                pass
            
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
                
                """ # Validierung: Sterbejahr muss nach Geburtsjahr liegen
                if death_year <= birth_year:
                    death_year = birth_year + 55
                    estimated_death = True """
                
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
        self.romans = []
        self.tooltip = None
        self.tooltip_bg = None
        
        self.create_timeline()
    
    def create_timeline(self):
        # Canvas für Timeline + Römer (erweiterte Höhe)
        self.canvas = tk.Canvas(
            self.parent,
            bg=AppColors.CONTENT_FRAME,
            highlightthickness=0,
            height=500  # Größer für Römer-Bereich
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Horizontale Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.canvas.configure(xscrollcommand=scrollbar.set)
        
        self.draw_timeline()
    
    def draw_timeline(self):
        self.canvas.delete("all")
        
        canvas_height = 500
        timeline_y = 80  # Timeline weiter oben
        
        # Timeline-Linie
        total_years = self.end_year - self.start_year
        pixels_per_year = max(30, 1500 / total_years)
        timeline_width = total_years * pixels_per_year
        self.timeline_width = timeline_width
        self.pixels_per_year = pixels_per_year
        
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
        
        # Römer zeichnen
        self.draw_romans(pixels_per_year, timeline_y + 60)
        
        # Scroll-Region setzen
        self.canvas.configure(scrollregion=(0, 0, timeline_width + 100, canvas_height))
    
    def draw_events(self, pixels_per_year, timeline_y):
        for i, event in enumerate(self.events):
            x = 50 + (event['year'] - self.start_year) * pixels_per_year
            
            # Event-Punkt
            radius = 6
            self.canvas.create_oval(
                x - radius, timeline_y - radius,
                x + radius, timeline_y + radius,
                fill=event.get('color', AppColors.ACCENT),
                outline=AppColors.BACKGROUND,
                width=2
            )
            
            # Event-Label (nach oben)
            y_offset = -10
            label_y = timeline_y + y_offset - (event['height'] * 15)
            
            # Event-Linie
            self.canvas.create_line(
                x, timeline_y - radius,
                x, label_y + 10,
                fill=event.get('color', AppColors.ACCENT),
                width=1
            )
            
            # Event-Text
            self.canvas.create_text(
                x, label_y,
                text=event['title'],
                font=Fonts.STANDARD,
                fill=AppColors.KU_COLOR,
                justify=tk.CENTER
            )
    
    def draw_romans(self, pixels_per_year, start_y):
        """Römer als Rechtecke mit mehreren Ebenen zeichnen"""
        if not self.romans:
            return
        
        # Römer nach Geburtsjahr sortieren
        sorted_romans = sorted(self.romans, key=lambda x: x['birth_year'])
        
        # Ebenen-System für Überlappungsvermeidung
        levels = []
        level_height = 25
        level_spacing = 5
        max_levels = 12
        
        for roman in sorted_romans:
            # Nur Römer im sichtbaren Zeitbereich
            if (roman['death_year'] >= self.start_year and 
                roman['birth_year'] <= self.end_year):
                
                # X-Koordinaten berechnen
                birth_x = 50 + max(0, (roman['birth_year'] - self.start_year)) * pixels_per_year
                death_x = 50 + min(self.timeline_width, (roman['death_year'] - self.start_year)) * pixels_per_year
                
                # Passende Ebene finden
                level = self.find_available_level(levels, roman['birth_year'], roman['death_year'])
                if level >= max_levels:
                    continue  # Zu viele Ebenen, überspringen
                
                # Y-Position berechnen
                current_y = start_y + 30 + (level * (level_height + level_spacing))
                
                # Rechteck zeichnen
                rect_id = self.canvas.create_rectangle(
                    birth_x, current_y,
                    death_x, current_y + level_height,
                    fill=roman['color'],
                    outline="white",
                    width=2
                )
                
                # Name in Rechteck (falls genug Platz)
                rect_width = death_x - birth_x
                if rect_width > 80:
                    # Vollständiger Name
                    name_text = roman['name']
                elif rect_width > 40:
                    # Abgekürzter Name
                    name_parts = roman['name'].split()
                    if len(name_parts) > 1:
                        name_text = f"{name_parts[0]} {name_parts[-1][0]}."
                    else:
                        name_text = roman['name'][:8] + "..."
                else:
                    # Nur Initialen
                    name_parts = roman['name'].split()
                    if len(name_parts) > 1:
                        name_text = f"{name_parts[0][0]}.{name_parts[-1][0]}."
                    else:
                        name_text = roman['name'][:3]
                
                if rect_width > 25:  # Mindestbreite für Text
                    text_x = (birth_x + death_x) / 2
                    self.canvas.create_text(
                        text_x, current_y + level_height // 2,
                        text=name_text,
                        font=Fonts.STANDARD_BOLD,
                        fill="white",
                        justify=tk.CENTER
                    )
                
                # Tooltip-Events
                self.canvas.tag_bind(rect_id, "<Enter>", 
                    lambda e, r=roman: self.show_roman_tooltip(e, r))
                self.canvas.tag_bind(rect_id, "<Leave>", 
                    lambda e: self.hide_tooltip()),
                self.canvas.tag_bind(rect_id, "<Motion>", 
                                     lambda e: self.update_tooltip_position(e))
                
                # Ebene als belegt markieren
                while len(levels) <= level:
                    levels.append([])
                levels[level].append((roman['birth_year'], roman['death_year']))
    
    def find_available_level(self, levels, birth_year, death_year):
        """Findet die erste verfügbare Ebene ohne Überlappung"""
        for level_idx, level_ranges in enumerate(levels):
            overlaps = False
            for existing_birth, existing_death in level_ranges:
                # Prüfe auf Überlappung
                if not (death_year <= existing_birth or birth_year >= existing_death):
                    overlaps = True
                    break
            
            if not overlaps:
                return level_idx
        
        # Neue Ebene erstellen
        return len(levels)
    
    def show_roman_tooltip(self, event, roman):
        """Tooltip mit canvasx - folgt der Maus"""
        self.hide_tooltip()
        
        # Tooltip-Daten speichern für Mouse-Follow
        self.current_roman = roman
        
        # Tooltip erstellen
        self.update_tooltip_position(event)

    def update_tooltip_position(self, event):
        """Tooltip-Position aktualisieren"""
        if not hasattr(self, 'current_roman') or not self.current_roman:
            return
        
        roman = self.current_roman
        
        # Tooltip-Text
        name = roman['name']
        birth = roman['birth_year']
        death = roman['death_year']
        lifespan = death - birth
        
        tooltip_lines = [f"👤 {name}"]
        tooltip_lines.append(f"{Icons.BIRTH} {abs(birth)}" + (' v. Chr' if birth <= 0 else ' n. Chr'))
        tooltip_lines.append(f"{Icons.DEATH} {abs(death)}" + (' v. Chr' if death <= 0 else ' n. Chr'))
        tooltip_lines.append(f"⏳ {lifespan} Jahre")
        
        if roman.get('estimated_death', False):
            tooltip_lines.append("⚠️ Sterbedatum geschätzt")
        
        tooltip_text = "\n".join(tooltip_lines)
        
        # Alten Tooltip löschen
        if hasattr(self, 'tooltip') and self.tooltip:
            self.canvas.delete(self.tooltip)
        if hasattr(self, 'tooltip_bg') and self.tooltip_bg:
            self.canvas.delete(self.tooltip_bg)
        
        # Neue Position
        canvas_x = self.canvas.canvasx(event.x) + 50
        canvas_y = self.canvas.canvasy(event.y) - 30
        
        # Neuen Tooltip erstellen
        self.tooltip = self.canvas.create_text(
            canvas_x + 15, canvas_y - 15,
            text=tooltip_text,
            font=Fonts.STANDARD,
            fill=AppColors.KU_COLOR,
            anchor=tk.NW,
            width=280
        )
        
        # Hintergrund
        bbox = self.canvas.bbox(self.tooltip)
        if bbox:
            padding = 8
            self.tooltip_bg = self.canvas.create_rectangle(
                bbox[0] - padding, bbox[1] - padding,
                bbox[2] + padding, bbox[3] + padding,
                fill="#FFFFFF",
                outline=roman['color'],
                width=2
            )
            self.canvas.tag_lower(self.tooltip_bg)

        self.canvas.tag_raise(self.tooltip_bg)  # Hintergrund nach vorne
        self.canvas.tag_raise(self.tooltip)     # Text ganz nach vorne
    
    def hide_tooltip(self):
        """Tooltip verstecken"""
        if self.tooltip:
            self.canvas.delete(self.tooltip)
            self.tooltip = None
        if self.tooltip_bg:
            self.canvas.delete(self.tooltip_bg)
            self.tooltip_bg = None
    
    def add_event(self, year, title, color=None, height=1):
        self.events.append({
            'year': year,
            'title': title,
            'color': color or AppColors.ACCENT,
            'height': height
        })
        self.draw_timeline()
    
    def load_romans_from_list(self, romans_list):
        """Römer aus der Liste laden"""
        self.romans = []
        
        for roman in romans_list:
            # Nur Römer im Zeitbereich
            if (roman['death_year'] >= self.start_year and 
                roman['birth_year'] <= self.end_year):
                
                # Zufällige Farbe generieren
                color = self.get_random_bright_color()
                
                roman_data = {
                    'name': roman['name'],
                    'birth_year': roman['birth_year'],
                    'death_year': roman['death_year'],
                    'color': color,
                    'estimated_death': roman.get('estimated_death', False),
                    'original_birth_string': roman.get('original_birth_string', ''),
                    'original_death_string': roman.get('original_death_string', ''),
                    'description': roman.get('description', ''),
                    'raw_data': roman.get('raw_data', {})
                }
                
                self.romans.append(roman_data)
        
        print(f"Timeline: {len(self.romans)} Römer im Zeitbereich {self.start_year}-{self.end_year} geladen")
        self.draw_timeline()
    
    def get_random_bright_color(self):
        """Zufällige helle Farbe für Römer"""
        bright_colors = [ 
        "#8B0000",  # Dunkelrot
        "#2F4F4F",  # Dunkles Schiefergrau
        "#191970",  # Mitternachtsblau
        "#006400",  # Dunkelgrün
        "#8B4513",  # Sattelbraun
        "#4B0082",  # Indigo
        "#2E8B57",  # Meeresgrün
        "#B8860B",  # Dunkles Goldgelb
        "#9932CC",  # Dunkles Orchidee
        "#1E90FF",  # Dodgerblau
        "#DC143C",  # Karmesinrot
        "#00CED1",  # Dunkles Türkis
        "#FF8C00",  # Dunkles Orange
        "#9400D3",  # Violett
        "#228B22",  # Waldgrün
        "#FF1493",  # Tiefes Pink
        "#00008B",  # Dunkelblau
        "#8B008B",  # Dunkles Magenta
        "#556B2F",  # Dunkles Olivgrün
        "#800080",  # Purpur
        "#CD853F",  # Peru
        "#4682B4",  # Stahlblau
        "#D2691E",  # Schokolade
        "#6B8E23",  # Olivgrau
        "#A0522D",  # Sienna
        "#483D8B",  # Dunkles Schieferblau
        "#B22222",  # Feuerziegelrot
        "#5F9EA0",  # Cadetblau
        "#D2B48C",  # Tan (etwas heller aber noch dunkel genug)
        "#708090"   # Schiefergrau
    ]
        return random.choice(bright_colors)