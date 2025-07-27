# In Objects/Content.py

import tkinter as tk
from tkinter import ttk
import os
import sys

# Projektverzeichnis zum Suchpfad hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Absolute Importe
from Objects.Config import AppColors

class BaseContentFrame(tk.Frame):
    """Basisklasse für alle Content-Frames"""
    
    def __init__(self, parent) -> None:
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
        self._CreateUi()
    
    def _CreateUi(self) -> None:
        """Erstellt die UI-Komponenten (von Unterklassen zu überschreiben)"""
        pass
    
    def UpdateData(self, data=None) -> None:
        """Aktualisiert die Daten im Frame (von Unterklassen zu überschreiben)"""
        pass

# --- Startseite ---
class StartseiteFrame(BaseContentFrame):
    """Content-Frame für die Startseite"""
    
    def _CreateUi(self):
        # Header
        header = tk.Label(
            self, 
            text="Willkommen zur Prosopographie der Julisch-Claudischen Kaiserzeit",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Beschreibung
        description = tk.Label(
            self,
            text="Hier finden Sie Informationen zu Personen, Orten und Ereignissen der Julisch-Claudischen Epoche.",
            font=('Helvetica', 12),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=600,
            justify='left'
        )
        description.pack(pady=5, padx=20, anchor='w')

# --- Ansicht Submenu Frames ---
class AnsichtListeFrame(BaseContentFrame):
    def _CreateUi(self) -> None:
        header = tk.Label(
            self, 
            text="Personenliste",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Suchframe
        search_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="Suche:", bg=AppColors.CONTENT_FRAME).pack(side='left')
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        search_button = tk.Button(search_frame, text="Suchen")
        search_button.pack(side='left', padx=5)
        
        # Tabelle für Personen
        columns = ("id", "name", "geburt", "tod", "position")
        
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        # Spaltenüberschriften definieren
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("geburt", text="Geburtsdatum")
        self.tree.heading("tod", text="Todesdatum")
        self.tree.heading("position", text="Position")
        
        # Spaltenbreiten festlegen
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("geburt", width=100)
        self.tree.column("tod", width=100)
        self.tree.column("position", width=150)
        
        # Beispieldaten hinzufügen
        data = [
            (1, "Augustus", "63 v. Chr.", "14 n. Chr.", "Kaiser"),
            (2, "Tiberius", "42 v. Chr.", "37 n. Chr.", "Kaiser"),
            (3, "Caligula", "12 n. Chr.", "41 n. Chr.", "Kaiser"),
            (4, "Claudius", "10 v. Chr.", "54 n. Chr.", "Kaiser"),
            (5, "Nero", "37 n. Chr.", "68 n. Chr.", "Kaiser"),
        ]
        
        for item in data:
            self.tree.insert("", "end", values=item)
        
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)

class AnsichtKarteFrame(BaseContentFrame):
    def _CreateUi(self) -> None:
        header = tk.Label(
            self, 
            text="Kartenansicht",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Dummy-Karte (im realen Projekt durch echte Karte ersetzen)
        map_frame = tk.Frame(self, bg="#e0e0e0", width=600, height=400)
        map_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Platzhalter-Text
        tk.Label(
            map_frame, 
            text="Hier wird eine Karte des Römischen Reiches angezeigt", 
            bg="#e0e0e0"
        ).place(relx=0.5, rely=0.5, anchor='center')
        
        # Steuerelemente für die Karte
        controls_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(controls_frame, text="Vergrößern (+)").pack(side='left', padx=5)
        tk.Button(controls_frame, text="Verkleinern (-)").pack(side='left', padx=5)
        tk.Button(controls_frame, text="Zurücksetzen").pack(side='left', padx=5)

class AnsichtTabelleFrame(BaseContentFrame):
    def _CreateUi(self) -> None:
        header = tk.Label(
            self, 
            text="Tabellarische Ansicht",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Filteroption
        filter_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            filter_frame, 
            text="Filter anwenden:", 
            bg=AppColors.CONTENT_FRAME
        ).pack(side='left')
        
        filter_options = ["Alle Einträge", "Nur Kaiser", "Nur Senatoren", "Nur Frauen"]
        self.filter_var = tk.StringVar(value=filter_options[0])
        filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options)
        filter_menu.pack(side='left', padx=5)
        filter_menu.bind("<<ComboboxSelected>>", self.apply_filter)
        
        # Container für Tabelle und Scrollbars
        table_frame = tk.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Erweiterte Tabelle mit mehr Spalten
        self.columns = ("id", "name", "geburt", "tod", "position", "herkunft", "familie")
        
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show='headings')
        
        # Spaltenüberschriften definieren mit Sortierfunktion
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize(), 
                             command=lambda _col=col: self.sort_treeview(_col))
        
        # Spaltenbreiten festlegen
        self.tree.column("id", width=40)
        self.tree.column("name", width=150)
        self.tree.column("geburt", width=100)
        self.tree.column("tod", width=100)
        self.tree.column("position", width=100)
        self.tree.column("herkunft", width=100)
        self.tree.column("familie", width=150)
        
        # Scrollbars hinzufügen (vertikal und horizontal)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid-Layout für Tabelle und Scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Grid-Konfiguration für richtiges Verhalten beim Vergrößern
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Beispieldaten hinzufügen
        self.all_data = [
            (1, "Augustus", "63 v. Chr.", "14 n. Chr.", "Kaiser", "Rom", "Julisch-Claudisch"),
            (2, "Tiberius", "42 v. Chr.", "37 n. Chr.", "Kaiser", "Rom", "Julisch-Claudisch"),
            (3, "Caligula", "12 n. Chr.", "41 n. Chr.", "Kaiser", "Antium", "Julisch-Claudisch"),
            (4, "Claudius", "10 v. Chr.", "54 n. Chr.", "Kaiser", "Lugdunum", "Julisch-Claudisch"),
            (5, "Nero", "37 n. Chr.", "68 n. Chr.", "Kaiser", "Antium", "Julisch-Claudisch"),
            (6, "Livia Drusilla", "58 v. Chr.", "29 n. Chr.", "Kaiserin", "Rom", "Julisch-Claudisch"),
            (7, "Agrippina die Jüngere", "15 n. Chr.", "59 n. Chr.", "Kaiserin", "Köln", "Julisch-Claudisch"),
        ]
        
        self.populate_treeview(self.all_data)
        
        # Sortierrichtung für jede Spalte speichern
        self.sort_direction = {col: False for col in self.columns}  # False = aufsteigend
    
    def populate_treeview(self, data: list[tuple]) -> None:
        # Bestehende Einträge löschen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Neue Daten einfügen
        for item in data:
            self.tree.insert("", "end", values=item)
    
    def sort_treeview(self, col: int) -> None:
        # Sortierrichtung umkehren
        self.sort_direction[col] = not self.sort_direction[col]
        
        # Daten aus der Tabelle holen
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Prüfen ob numerisch oder alphabetisch sortiert werden soll
        try:
            # Versuchen, als Zahlen zu sortieren (für ID-Spalte)
            if col == "id":
                data.sort(key=lambda x: int(x[0]), reverse=self.sort_direction[col])
            else:
                # Alphabetisch sortieren
                data.sort(key=lambda x: x[0].lower(), reverse=self.sort_direction[col])
        except ValueError:
            # Wenn Konvertierung fehlschlägt, alphabetisch sortieren
            data.sort(key=lambda x: x[0].lower(), reverse=self.sort_direction[col])
        
        # Neuanordnung der Elemente
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)
    
    def apply_filter(self, event=None) -> None:
        filter_value = self.filter_var.get()
        
        if filter_value == "Alle Einträge":
            filtered_data = self.all_data
        elif filter_value == "Nur Kaiser":
            filtered_data = [item for item in self.all_data if item[4] == "Kaiser"]
        elif filter_value == "Nur Senatoren":
            filtered_data = [item for item in self.all_data if item[4] == "Senator"]
        elif filter_value == "Nur Frauen":
            filtered_data = [item for item in self.all_data if item[4] == "Kaiserin"]
        
        self.populate_treeview(filtered_data)

class AnsichtZeitstrahlFrame(BaseContentFrame):
    def _CreateUi(self) -> None:
        header = tk.Label(
            self, 
            text="Zeitstrahl-Ansicht",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Dummy-Zeitstrahl
        canvas = tk.Canvas(self, bg="white", height=200)
        canvas.pack(fill='x', padx=20, pady=20, expand=False)
        
        # Zeitlinien zeichnen
        canvas.create_line(50, 100, 750, 100, width=2)  # Hauptzeitlinie
        
        # Jahre markieren
        years = ["-50", "0", "50", "100"]
        positions = [50, 250, 450, 650]
        
        for i, (year, pos) in enumerate(zip(years, positions)):
            canvas.create_line(pos, 90, pos, 110, width=1)  # Markierung
            canvas.create_text(pos, 120, text=year, font=('Helvetica', 10))
        
        # Ereignisse eintragen
        events = [
            ("Augustus", 75, "14 n.Chr."),
            ("Tiberius", 150, "37 n.Chr."),
            ("Caligula", 200, "41 n.Chr."),
            ("Claudius", 250, "54 n.Chr."),
            ("Nero", 300, "68 n.Chr.")
        ]
        
        for name, pos, date in events:
            # Punkt auf Zeitlinie
            canvas.create_oval(pos-5, 100-5, pos+5, 100+5, fill="red", outline="")
            
            # Abwechselnd oben/unten platzieren für bessere Lesbarkeit
            if events.index((name, pos, date)) % 2 == 0:
                canvas.create_line(pos, 95, pos, 60, width=1)
                canvas.create_text(pos, 50, text=f"{name}\n{date}", font=('Helvetica', 9))
            else:
                canvas.create_line(pos, 105, pos, 140, width=1)
                canvas.create_text(pos, 150, text=f"{name}\n{date}", font=('Helvetica', 9))
        
        # Zoom-Controls
        controls_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(controls_frame, text="Zeitraum vergrößern").pack(side='left', padx=5)
        tk.Button(controls_frame, text="Zeitraum verkleinern").pack(side='left', padx=5)
        tk.Label(controls_frame, text="Zeitspanne:", bg=AppColors.CONTENT_FRAME).pack(side='left', padx=(20, 5))
        
        range_options = ["Alle", "27 v.Chr - 68 n.Chr", "27 v.Chr - 14 n.Chr", "14 n.Chr - 68 n.Chr"]
        range_var = tk.StringVar(value=range_options[0])
        range_menu = ttk.Combobox(controls_frame, textvariable=range_var, values=range_options)
        range_menu.pack(side='left', padx=5)

# --- Erstellung Submenu Frames ---
class ErstellungPersonFrame(BaseContentFrame):
    def _CreateUi(self) -> None:
        header = tk.Label(
            self, 
            text="Neue Person erstellen",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Formular erstellen
        form_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Grid für das Formular konfigurieren
        form_frame.columnconfigure(0, weight=0)  # Label-Spalte
        form_frame.columnconfigure(1, weight=1)  # Eingabefeld-Spalte
        
        # Felder definieren
        fields = [
            {"label": "Vorname:", "type": "entry"},
            {"label": "Nachname:", "type": "entry"},
            {"label": "Geburtsdatum:", "type": "entry"},
            {"label": "Geburtsort:", "type": "entry"},
            {"label": "Sterbedatum:", "type": "entry"},
            {"label": "Sterbeort:", "type": "entry"},
            {"label": "Position:", "type": "combobox", "values": [
                "Kaiser", "Kaiserin", "Senator", "Ritter", "Freigelassener", "Sklave"
            ]},
            {"label": "Familie:", "type": "entry"},
            {"label": "Beschreibung:", "type": "text"}
        ]
        
        # Felder erstellen
        row = 0
        for field in fields:
            # Label erstellen
            tk.Label(
                form_frame, 
                text=field["label"],
                bg=AppColors.CONTENT_FRAME,
                anchor='e'
            ).grid(row=row, column=0, sticky='e', padx=10, pady=5)
            
            # Eingabefeld erstellen
            if field["type"] == "entry":
                tk.Entry(form_frame, width=40).grid(row=row, column=1, sticky='w', padx=5, pady=5)
            elif field["type"] == "combobox":
                combo = ttk.Combobox(form_frame, values=field["values"], width=38)
                combo.grid(row=row, column=1, sticky='w', padx=5, pady=5)
            elif field["type"] == "text":
                text = tk.Text(form_frame, width=40, height=5)
                text.grid(row=row, column=1, sticky='w', padx=5, pady=5)
            
            row += 1
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Speichern").pack(side='left', padx=5)
        tk.Button(button_frame, text="Abbrechen").pack(side='left', padx=5)

# --- Weitere Frame-Definitionen für andere Submenu-Items ---
class ErstellungOrtFrame(BaseContentFrame):
    def _CreateUi(self) -> None:
        header = tk.Label(
            self, 
            text="Neuen Ort erstellen",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Formular mit spezifischen Feldern für Orte
        # (ähnlich wie bei ErstellungPersonFrame)

# Default Frame für noch nicht implementierte Inhalte
class DefaultContentFrame(BaseContentFrame):
    def __init__(self, parent, title: str) -> None:
        self.title = title
        super().__init__(parent)
    
    def _CreateUi(self) -> None:
        label = tk.Label(
            self,
            text=f"Inhalt von {self.title}",
            font=('Helvetica', 18, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        label.pack(padx=50, pady=50)

# ContentManager-Klasse anpassen, um alle spezialisierten Frames zu verwalten
class ContentManager:
    """Verwaltet die verschiedenen Content-Frames"""
    
    def __init__(self, parent) -> None:
        self.parent = parent
        self.current_frame = None
        
        # Frame-Mapping für alle Navigation-Optionen und ihre Submenu-Items
        self.frames = {
            # Hauptnavigation
            'Startseite': StartseiteFrame,
            'Statistik': DefaultContentFrame,  # Noch nicht implementiert
            'Hilfe': DefaultContentFrame,
            'Impressum': DefaultContentFrame,
            
            # Ansicht Submenu
            'Ansicht - Liste': AnsichtListeFrame,
            'Ansicht - Karte': AnsichtKarteFrame,
            'Ansicht - Tabelle': AnsichtTabelleFrame,
            'Ansicht - Zeitstrahl': AnsichtZeitstrahlFrame,
            
            # Erstellung Submenu
            'Erstellung - Person': ErstellungPersonFrame,
            'Erstellung - Ort': ErstellungOrtFrame,
            'Erstellung - Ereignis': DefaultContentFrame,  # Noch zu implementieren
            'Erstellung - Quelle': DefaultContentFrame,    # Noch zu implementieren
            
            # BibTex Submenu
            'BibTex - Literatur hinzufügen': DefaultContentFrame,
            'BibTex - Zitieren': DefaultContentFrame,
            'BibTex - Verwalten': DefaultContentFrame,
        }
    
    def ShowContent(self, option: str) -> None:
        """Zeigt den Content für die gewählte Option an"""
        # Entferne alten Frame
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.destroy()
        
        # Bestimme den korrekten Frame-Typ
        if option in self.frames:
            frame_class = self.frames[option]
            
            # Unterscheide zwischen Klassen und Dummy-Frames
            if frame_class == DefaultContentFrame:
                self.current_frame = DefaultContentFrame(self.parent, option)
            else:
                self.current_frame = frame_class(self.parent)
        else:
            # Fallback auf einen generischen Frame
            self.current_frame = DefaultContentFrame(self.parent, option)
        
        # Zeige den Frame an
        self.current_frame.pack(fill='both', expand=True)
        
        # Bei Bedarf Daten aktualisieren
        if hasattr(self.current_frame, 'update_data'):
            self.current_frame.update_data()