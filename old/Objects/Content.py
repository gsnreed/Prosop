# In Objects/Content.py

import tkinter as tk
from tkinter import ttk
import os
import sys
from tkinter import messagebox

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
            'Ansicht - Tabelle': DefaultContentFrame,
            'Ansicht - Karte': AnsichtKarteFrame,
            'Ansicht - Zeitstrahl': AnsichtZeitstrahlFrame,
            
            # Erstellung Submenu
            'Erstellung': ErstellungFrame,
            
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

# Tabellenansicht für Römer
class ErstellungFrame(BaseContentFrame):
    def __init__(self, parent) -> None:
        self.app = self._find_main_app(parent)
        self.current_roman = None
        super().__init__(parent)
    
    def _find_main_app(self, widget):
        """Findet die MainApp-Instanz in der Widget-Hierarchie"""
        if hasattr(widget, 'romans'):
            return widget
        elif widget.master:
            return self._find_main_app(widget.master)
        else:
            return None
    
    def _CreateUi(self) -> None:
        # Hauptcontainer mit Gewichtung
        self.columnconfigure(0, weight=3)  # Tabellenspalte
        self.columnconfigure(1, weight=0)  # Trennlinie
        self.columnconfigure(2, weight=2)  # Detailspalte
        self.rowconfigure(0, weight=1)
        
        # 1. Linke Seite: Header und Tabelle
        left_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Header mit Suchfeld
        header_frame = tk.Frame(left_frame, bg=AppColors.CONTENT_FRAME)
        header_frame.pack(fill="x", pady=(0, 10))
        
        header_label = tk.Label(
            header_frame, 
            text="Römer-Datenbank",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header_label.pack(side="left", padx=10)
        
        # Suchfeld
        search_frame = tk.Frame(header_frame, bg=AppColors.CONTENT_FRAME)
        search_frame.pack(side="right", padx=10)
        
        search_label = tk.Label(search_frame, text="Suche:", bg=AppColors.CONTENT_FRAME)
        search_label.pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", self._filter_table)
        
        # Tabelle mit Scrollbar
        table_frame = tk.Frame(left_frame, bg=AppColors.CONTENT_FRAME)
        table_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame)
        y_scrollbar.pack(side="right", fill="y")
        
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")
        
        # Treeview für Tabelle
        columns = ("name", "geburt", "tod", "familie")
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns,
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        
        # Scrollbars mit Treeview verbinden
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)
        
        # Spaltenüberschriften definieren
        self.tree.heading("name", text="Name")
        self.tree.heading("geburt", text="Geburt")
        self.tree.heading("tod", text="Tod")
        self.tree.heading("familie", text="Familie")
        
        # Spaltenbreiten festlegen
        self.tree.column("name", width=150)
        self.tree.column("geburt", width=150)
        self.tree.column("tod", width=150)
        self.tree.column("familie", width=200)
        
        self.tree.pack(fill="both", expand=True)
        
        # Event-Binding für Auswahl
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        # Aktionsbuttons unter der Tabelle
        action_frame = tk.Frame(left_frame, bg=AppColors.CONTENT_FRAME)
        action_frame.pack(fill="x", pady=10)
        
        add_button = ttk.Button(action_frame, text="Neu erstellen", command=self._create_roman)
        add_button.pack(side="left", padx=5)
        
        delete_button = ttk.Button(action_frame, text="Löschen", command=self._delete_roman)
        delete_button.pack(side="left", padx=5)
        
        # 2. Trennlinie
        separator = ttk.Separator(self, orient="vertical")
        separator.grid(row=0, column=1, sticky="ns", padx=5)
        
        # 3. Rechte Seite: Detailansicht
        right_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=10)
        
        # Header für Detailansicht
        detail_header = tk.Label(
            right_frame,
            text="Details",
            font=('Helvetica', 14, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        detail_header.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Notebook für Registerkarten
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Registerkarten erstellen
        self.tab_basic = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_marriage = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_children = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_family = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_special = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_honors = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_sources = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        
        self.notebook.add(self.tab_basic, text="Grunddaten")
        self.notebook.add(self.tab_marriage, text="Ehen")
        self.notebook.add(self.tab_children, text="Kinder")
        self.notebook.add(self.tab_family, text="Familie")
        self.notebook.add(self.tab_special, text="Besonderheiten")
        self.notebook.add(self.tab_honors, text="Ehrungen")
        self.notebook.add(self.tab_sources, text="Quellen")
        
        # Inhalt der Tabs erstellen
        self._create_basic_tab()
        self._create_marriage_tab()
        self._create_children_tab()
        self._create_family_tab()
        self._create_special_tab()
        self._create_honors_tab()
        self._create_sources_tab()
        
        # Zunächst leere Felder
        self._clear_details()
        
        # Tabelle mit Daten füllen
        self._load_data()
    
    def _create_basic_tab(self):
        """Erstellt die Grunddaten-Registerkarte"""
        form_frame = tk.Frame(self.tab_basic, bg=AppColors.CONTENT_FRAME)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Formularfelder für Grunddaten
        fields = [
            ("Name", "name"), 
            ("Geburtsdatum", "geburtsdatum"), 
            ("Sterbedatum", "sterbedatum"),
            ("Todesursache", "todesursache")
        ]
        
        self.basic_entries = {}
        
        for i, (label_text, field_key) in enumerate(fields):
            label = tk.Label(
                form_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            
            self.basic_entries[field_key] = entry
        
        # Speicher-Button
        save_frame = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        save_frame.grid(row=len(fields), column=0, columnspan=2, sticky="e", pady=10)
        
        save_button = ttk.Button(save_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("basic"))
        save_button.pack(side="right", padx=5)
        
        # Form-Frame dehnbar machen
        form_frame.columnconfigure(1, weight=1)
    
    def _create_marriage_tab(self):
        """Erstellt die Ehen-Registerkarte"""
        for widget in self.tab_marriage.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.tab_marriage, bg=AppColors.CONTENT_FRAME)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info-Label
        info_label = tk.Label(
            main_frame,
            text="Häufigkeit Heirat:",
            font=('Helvetica', 11, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            anchor="w"
        )
        info_label.pack(anchor="w", pady=(0, 5))
        
        # Häufigkeit Heirat
        self.marriage_frequency_var = tk.StringVar()
        frequency_entry = tk.Entry(main_frame, textvariable=self.marriage_frequency_var, width=40)
        frequency_entry.pack(anchor="w", fill="x", pady=(0, 10))
        
        # Liste der Ehepartner
        tk.Label(
            main_frame, 
            text="Ehepartner:", 
            font=('Helvetica', 11, 'bold'),
            bg=AppColors.CONTENT_FRAME, 
            anchor="w"
        ).pack(anchor="w", pady=(5, 5))
        
        # Frame für Ehepartner-Liste
        list_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        list_frame.pack(fill="both", expand=True)
        
        self.marriage_entries = []
        self.marriage_frames = []
        
        # Container für die Einträge
        entries_frame = tk.Frame(list_frame, bg=AppColors.CONTENT_FRAME)
        entries_frame.pack(fill="both", expand=True)
        
        # Erstelle 6 Felder für Ehepartner
        for i in range(6):
            entry_frame = tk.Frame(entries_frame, bg=AppColors.CONTENT_FRAME)
            entry_frame.pack(fill="x", pady=2)
            
            label = tk.Label(entry_frame, text=f"{i+1}:", width=2, bg=AppColors.CONTENT_FRAME)
            label.pack(side="left", padx=(0, 5))
            
            entry = tk.Entry(entry_frame, width=50)
            entry.pack(side="left", fill="x", expand=True)
            
            self.marriage_entries.append(entry)
            self.marriage_frames.append(entry_frame)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.pack(fill="x", pady=10)
        
        add_button = ttk.Button(button_frame, text="Feld hinzufügen", command=self._add_marriage_field)
        add_button.pack(side="left", padx=5)
        
        save_button = ttk.Button(button_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("marriage"))
        save_button.pack(side="right", padx=5)
    
    def _create_children_tab(self):
        """Erstellt die Kinder-Registerkarte"""
        for widget in self.tab_children.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.tab_children, bg=AppColors.CONTENT_FRAME)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info-Label
        info_label = tk.Label(
            main_frame,
            text="Anzahl Kinder:",
            font=('Helvetica', 11, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            anchor="w"
        )
        info_label.pack(anchor="w", pady=(0, 5))
        
        # Anzahl Kinder
        self.children_count_var = tk.StringVar()
        count_entry = tk.Entry(main_frame, textvariable=self.children_count_var, width=40)
        count_entry.pack(anchor="w", fill="x", pady=(0, 10))
        
        # Liste der Kinder
        tk.Label(
            main_frame, 
            text="Kinder:", 
            font=('Helvetica', 11, 'bold'),
            bg=AppColors.CONTENT_FRAME, 
            anchor="w"
        ).pack(anchor="w", pady=(5, 5))
        
        # Frame für Kinder-Liste
        list_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        list_frame.pack(fill="both", expand=True)
        
        self.children_entries = []
        self.children_frames = []
        
        # Container für die Einträge
        entries_frame = tk.Frame(list_frame, bg=AppColors.CONTENT_FRAME)
        entries_frame.pack(fill="both", expand=True)
        
        # Erstelle 6 Felder für Kinder
        for i in range(6):
            entry_frame = tk.Frame(entries_frame, bg=AppColors.CONTENT_FRAME)
            entry_frame.pack(fill="x", pady=2)
            
            label = tk.Label(entry_frame, text=f"{i+1}:", width=2, bg=AppColors.CONTENT_FRAME)
            label.pack(side="left", padx=(0, 5))
            
            entry = tk.Entry(entry_frame, width=50)
            entry.pack(side="left", fill="x", expand=True)
            
            self.children_entries.append(entry)
            self.children_frames.append(entry_frame)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.pack(fill="x", pady=10)
        
        add_button = ttk.Button(button_frame, text="Feld hinzufügen", command=self._add_child_field)
        add_button.pack(side="left", padx=5)
        
        save_button = ttk.Button(button_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("children"))
        save_button.pack(side="right", padx=5)
    
    def _create_family_tab(self):
        """Erstellt die Familie-Registerkarte"""
        for widget in self.tab_family.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.tab_family, bg=AppColors.CONTENT_FRAME)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Familie und Vorfahren
        fields = [
            ("Familie", "familie"),
            ("Vorfahren", "vorfahren"),
            ("Verlobung", "verlobung")
        ]
        
        self.family_entries = {}
        
        for i, (label_text, field_key) in enumerate(fields):
            label = tk.Label(
                main_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11, 'bold'),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.pack(anchor="w", pady=(10, 5))
            
            text_widget = tk.Text(main_frame, height=4, width=50)
            text_widget.pack(fill="x", expand=True)
            
            self.family_entries[field_key] = text_widget
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.pack(fill="x", pady=10)
        
        save_button = ttk.Button(button_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("family"))
        save_button.pack(side="right", padx=5)
    
    def _create_special_tab(self):
        """Erstellt die Besonderheiten-Registerkarte"""
        for widget in self.tab_special.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.tab_special, bg=AppColors.CONTENT_FRAME)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Besonderheiten
        tk.Label(
            main_frame,
            text="Individuelle Besonderheiten:",
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.CONTENT_FRAME
        ).pack(anchor="w", pady=(0, 5))
        
        special_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        special_frame.pack(fill="x", pady=5)
        
        special_fields = [
            ("Auftreten", "auftreten"),
            ("Kleidung", "kleidung"),
            ("Schmuck", "schmuck")
        ]
        
        self.special_entries = {}
        
        for i, (label_text, field_key) in enumerate(special_fields):
            label = tk.Label(
                special_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            text_widget = tk.Text(special_frame, height=2, width=40)
            text_widget.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            
            self.special_entries[field_key] = text_widget
        
        special_frame.columnconfigure(1, weight=1)
        
        # Inszenierung
        tk.Label(
            main_frame,
            text="Inszenierung:",
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.CONTENT_FRAME
        ).pack(anchor="w", pady=(15, 5))
        
        inszenierung_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        inszenierung_frame.pack(fill="x", pady=5)
        
        inszenierung_fields = [
            ("Öffentlich", "öffentlich"),
            ("Privat", "privat")
        ]
        
        self.inszenierung_entries = {}
        
        for i, (label_text, field_key) in enumerate(inszenierung_fields):
            label = tk.Label(
                inszenierung_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            text_widget = tk.Text(inszenierung_frame, height=2, width=40)
            text_widget.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            
            self.inszenierung_entries[field_key] = text_widget
        
        inszenierung_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.pack(fill="x", pady=10)
        
        save_button = ttk.Button(button_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("special"))
        save_button.pack(side="right", padx=5)
    
    def _create_honors_tab(self):
        """Erstellt die Ehrungen-Registerkarte"""
        for widget in self.tab_honors.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.tab_honors, bg=AppColors.CONTENT_FRAME)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Ehrungen
        tk.Label(
            main_frame,
            text="Ehrungen:",
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.CONTENT_FRAME
        ).pack(anchor="w", pady=(0, 5))
        
        honors_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        honors_frame.pack(fill="x", pady=5)
        
        honors_fields = [
            ("Augusta-Titel", "augusta_titel"),
            ("Carpentum-Recht", "carpentum_recht"),
            ("Weitere", "weitere")
        ]
        
        self.honors_entries = {}
        
        for i, (label_text, field_key) in enumerate(honors_fields):
            label = tk.Label(
                honors_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            text_widget = tk.Text(honors_frame, height=2, width=40)
            text_widget.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            
            self.honors_entries[field_key] = text_widget
        
        honors_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.pack(fill="x", pady=10)
        
        save_button = ttk.Button(button_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("honors"))
        save_button.pack(side="right", padx=5)
    
    def _create_sources_tab(self):
        """Erstellt die Quellen-Registerkarte"""
        for widget in self.tab_sources.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.tab_sources, bg=AppColors.CONTENT_FRAME)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Quellen
        tk.Label(
            main_frame,
            text="Quellen:",
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.CONTENT_FRAME
        ).pack(anchor="w", pady=(0, 5))
        
        # Verschiedene Quellentypen
        sources_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        sources_frame.pack(fill="x", pady=5)
        
        sources_fields = [
            ("Divinisierung", "divinisierung"),
            ("Bestattung", "bestattung"),
            ("Archäologische Quellen", "archäologische_quellen"),
            ("Münzen", "münzen"),
            ("Inschriften", "inschriften")
        ]
        
        self.sources_entries = {}
        
        for i, (label_text, field_key) in enumerate(sources_fields):
            label = tk.Label(
                sources_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            text_widget = tk.Text(sources_frame, height=2, width=40)
            text_widget.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            
            self.sources_entries[field_key] = text_widget
        
        sources_frame.columnconfigure(1, weight=1)
        
        # Literarische Quellen
        tk.Label(
            main_frame,
            text="Literarische Quellen:",
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.CONTENT_FRAME
        ).pack(anchor="w", pady=(15, 5))
        
        lit_sources_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        lit_sources_frame.pack(fill="x", pady=5)
        
        lit_sources_fields = [
            ("Autor", "autor"),
            ("Werk", "werk")
        ]
        
        self.lit_sources_entries = {}
        
        for i, (label_text, field_key) in enumerate(lit_sources_fields):
            label = tk.Label(
                lit_sources_frame,
                text=f"{label_text}:",
                font=('Helvetica', 11),
                bg=AppColors.CONTENT_FRAME,
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            text_widget = tk.Text(lit_sources_frame, height=2, width=40)
            text_widget.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            
            self.lit_sources_entries[field_key] = text_widget
        
        lit_sources_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=AppColors.CONTENT_FRAME)
        button_frame.pack(fill="x", pady=10)
        
        save_button = ttk.Button(button_frame, text="Änderungen speichern", command=lambda: self._save_roman_tab("sources"))
        save_button.pack(side="right", padx=5)
    
    def _add_marriage_field(self):
        """Fügt ein weiteres Feld für Ehepartner hinzu"""
        i = len(self.marriage_entries)
        
        entry_frame = tk.Frame(self.marriage_frames[0].master, bg=AppColors.CONTENT_FRAME)
        entry_frame.pack(fill="x", pady=2)
        
        label = tk.Label(entry_frame, text=f"{i+1}:", width=2, bg=AppColors.CONTENT_FRAME)
        label.pack(side="left", padx=(0, 5))
        
        entry = tk.Entry(entry_frame, width=50)
        entry.pack(side="left", fill="x", expand=True)
        
        self.marriage_entries.append(entry)
        self.marriage_frames.append(entry_frame)
    
    def _add_child_field(self):
        """Fügt ein weiteres Feld für Kinder hinzu"""
        i = len(self.children_entries)
        
        entry_frame = tk.Frame(self.children_frames[0].master, bg=AppColors.CONTENT_FRAME)
        entry_frame.pack(fill="x", pady=2)
        
        label = tk.Label(entry_frame, text=f"{i+1}:", width=2, bg=AppColors.CONTENT_FRAME)
        label.pack(side="left", padx=(0, 5))
        
        entry = tk.Entry(entry_frame, width=50)
        entry.pack(side="left", fill="x", expand=True)
        
        self.children_entries.append(entry)
        self.children_frames.append(entry_frame)
    
    def _load_data(self):
        """Lädt die Römerdaten in die Tabelle"""
        # Alle aktuellen Einträge entfernen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Wenn keine App-Instanz gefunden wurde oder keine Römer vorhanden sind
        if not self.app or not hasattr(self.app, 'romans'):
            return
                
        # Daten aus der Romans-Liste hinzufügen
        for roman in self.app.romans:
            name = roman.get("Name", "")
            geburt = roman.get("Geburtsdatum", "")
            tod = roman.get("Sterbedatum", "")
            familie = roman.get("Familie", "")
            
            self.tree.insert("", "end", values=(name, geburt, tod, familie))
    
    def _on_select(self, event):
        """Behandelt die Auswahl in der Tabelle"""
        selection = self.tree.selection()
        if not selection:
            return
            
        # Index des ausgewählten Elements
        item = self.tree.item(selection[0])
        values = item["values"]
        
        # Finde den ausgewählten Römer
        selected_roman = None
        for roman in self.app.romans:
            if roman.get("Name", "") == values[0]:
                selected_roman = roman
                break
        
        if selected_roman:
            # Details anzeigen
            self._display_roman(selected_roman)
    
    def _display_roman(self, roman):
        """Zeigt die Details eines Romans an"""
        self.current_roman = roman
        
        # Grunddaten anzeigen
        self.basic_entries["name"].delete(0, tk.END)
        self.basic_entries["name"].insert(0, roman.get("Name", ""))
        
        self.basic_entries["geburtsdatum"].delete(0, tk.END)
        self.basic_entries["geburtsdatum"].insert(0, roman.get("Geburtsdatum", ""))
        
        self.basic_entries["sterbedatum"].delete(0, tk.END)
        self.basic_entries["sterbedatum"].insert(0, roman.get("Sterbedatum", ""))
        
        self.basic_entries["todesursache"].delete(0, tk.END)
        self.basic_entries["todesursache"].insert(0, roman.get("Todesursache", ""))
        
        # Ehepartner füllen
        männer = roman.get("Männer", [])
        self.marriage_frequency_var.set(roman.get("Häufigkeit Heirat", ""))
        
        for i, partner in enumerate(männer):
            if i < len(self.marriage_entries):
                self.marriage_entries[i].delete(0, tk.END)
                self.marriage_entries[i].insert(0, partner)
        
        # Kinder füllen
        kinder = roman.get("Kinder", [])
        self.children_count_var.set(roman.get("Anzahl Kinder", ""))
        
        for i, kind in enumerate(kinder):
            if i < len(self.children_entries):
                self.children_entries[i].delete(0, tk.END)
                self.children_entries[i].insert(0, kind)
        
        # Familie/Vorfahren füllen
        if "familie" in self.family_entries:
            self.family_entries["familie"].delete("1.0", tk.END)
            self.family_entries["familie"].insert("1.0", roman.get("Familie", ""))
        
        if "vorfahren" in self.family_entries:
            self.family_entries["vorfahren"].delete("1.0", tk.END)
            self.family_entries["vorfahren"].insert("1.0", roman.get("Vorfahren", ""))
        
        if "verlobung" in self.family_entries:
            self.family_entries["verlobung"].delete("1.0", tk.END)
            self.family_entries["verlobung"].insert("1.0", roman.get("Verlobung", ""))
        
        # Besonderheiten füllen
        besonderheiten = roman.get("Individuelle Besonderheiten", {})
        
        if "auftreten" in self.special_entries:
            self.special_entries["auftreten"].delete("1.0", tk.END)
            self.special_entries["auftreten"].insert("1.0", besonderheiten.get("Auftreten", ""))
        
        if "kleidung" in self.special_entries:
            self.special_entries["kleidung"].delete("1.0", tk.END)
            self.special_entries["kleidung"].insert("1.0", besonderheiten.get("Kleidung", ""))
        
        if "schmuck" in self.special_entries:
            self.special_entries["schmuck"].delete("1.0", tk.END)
            self.special_entries["schmuck"].insert("1.0", besonderheiten.get("Schmuck", ""))
        
        # Inszenierung füllen
        inszenierung = roman.get("Inszenierung", {})
        
        if "öffentlich" in self.inszenierung_entries:
            self.inszenierung_entries["öffentlich"].delete("1.0", tk.END)
            self.inszenierung_entries["öffentlich"].insert("1.0", inszenierung.get("Öffentlich", ""))
        
        if "privat" in self.inszenierung_entries:
            self.inszenierung_entries["privat"].delete("1.0", tk.END)
            self.inszenierung_entries["privat"].insert("1.0", inszenierung.get("Privat", ""))
        
        # Ehrungen füllen
        ehrungen = roman.get("Ehrungen", {})
        
        if "augusta_titel" in self.honors_entries:
            self.honors_entries["augusta_titel"].delete("1.0", tk.END)
            self.honors_entries["augusta_titel"].insert("1.0", ehrungen.get("Augusta-Titel", ""))
        
        if "carpentum_recht" in self.honors_entries:
            self.honors_entries["carpentum_recht"].delete("1.0", tk.END)
            self.honors_entries["carpentum_recht"].insert("1.0", ehrungen.get("Carpentum-Recht", ""))
        
        if "weitere" in self.honors_entries:
            self.honors_entries["weitere"].delete("1.0", tk.END)
            self.honors_entries["weitere"].insert("1.0", ehrungen.get("Weitere", ""))
        
        # Quellen füllen
        quellen = roman.get("Quellen", {})
        
        if "divinisierung" in self.sources_entries:
            self.sources_entries["divinisierung"].delete("1.0", tk.END)
            self.sources_entries["divinisierung"].insert("1.0", quellen.get("Divinisierung", ""))
        
        if "bestattung" in self.sources_entries:
            self.sources_entries["bestattung"].delete("1.0", tk.END)
            self.sources_entries["bestattung"].insert("1.0", quellen.get("Bestattung", ""))
        
        if "archäologische_quellen" in self.sources_entries:
            self.sources_entries["archäologische_quellen"].delete("1.0", tk.END)
            self.sources_entries["archäologische_quellen"].insert("1.0", quellen.get("Archäologische Quellen", ""))
        
        if "münzen" in self.sources_entries:
            self.sources_entries["münzen"].delete("1.0", tk.END)
            self.sources_entries["münzen"].insert("1.0", quellen.get("Münzen", ""))
        
        if "inschriften" in self.sources_entries:
            self.sources_entries["inschriften"].delete("1.0", tk.END)
            self.sources_entries["inschriften"].insert("1.0", quellen.get("Inschriften", ""))
        
        # Literarische Quellen
        lit_quellen = quellen.get("Literarische Quellen", {})
        
        if "autor" in self.lit_sources_entries:
            self.lit_sources_entries["autor"].delete("1.0", tk.END)
            self.lit_sources_entries["autor"].insert("1.0", lit_quellen.get("Autor", ""))
        
        if "werk" in self.lit_sources_entries:
            self.lit_sources_entries["werk"].delete("1.0", tk.END)
            self.lit_sources_entries["werk"].insert("1.0", lit_quellen.get("Werk", ""))
    
    def _clear_details(self):
        """Leert alle Detailfelder"""
        self.current_roman = None
        
        # Grunddaten leeren
        for entry in self.basic_entries.values():
            entry.delete(0, tk.END)
        
        # Ehepartner leeren
        self.marriage_frequency_var.set("")
        for entry in self.marriage_entries:
            entry.delete(0, tk.END)
        
        # Kinder leeren
        self.children_count_var.set("")
        for entry in self.children_entries:
            entry.delete(0, tk.END)
        
        # Familie leeren
        for text_widget in self.family_entries.values():
            text_widget.delete("1.0", tk.END)
        
        # Besonderheiten leeren
        for text_widget in self.special_entries.values():
            text_widget.delete("1.0", tk.END)
        
        # Inszenierung leeren
        for text_widget in self.inszenierung_entries.values():
            text_widget.delete("1.0", tk.END)
        
        # Ehrungen leeren
        for text_widget in self.honors_entries.values():
            text_widget.delete("1.0", tk.END)
        
        # Quellen leeren
        for text_widget in self.sources_entries.values():
            text_widget.delete("1.0", tk.END)
        
        # Literarische Quellen leeren
        for text_widget in self.lit_sources_entries.values():
            text_widget.delete("1.0", tk.END)
    
    def _create_roman(self):
        """Öffnet ein Dialog zum Erstellen eines neuen Romans"""
        if not self.app:
            return
        
        # Dialog erstellen
        dialog = tk.Toplevel(self)
        dialog.title("Neuen Römer erstellen")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Formular erstellen
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Grunddaten
        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        name_entry = tk.Entry(frame, width=30)
        name_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(frame, text="Geburtsdatum:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        geburt_entry = tk.Entry(frame, width=30)
        geburt_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(frame, text="Sterbedatum:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tod_entry = tk.Entry(frame, width=30)
        tod_entry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(frame, text="Familie:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        familie_entry = tk.Entry(frame, width=30)
        familie_entry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="e", pady=10)
        
        def save_new_roman():
            # Daten sammeln
            data = {
                "Name": name_entry.get(),
                "Geburtsdatum": geburt_entry.get(),
                "Sterbedatum": tod_entry.get(),
                "Familie": familie_entry.get(),
                "Männer": [],
                "Kinder": []
            }
            
            # Neuen Römer erstellen
            from Objects.Romans import Roman
            new_roman = Roman(data["Name"], **data)
            
            # Der App hinzufügen
            self.app.AddRoman(new_roman)
            
            # Dialog schließen
            dialog.destroy()
            
            # Tabelle aktualisieren
            self._load_data()
        
        save_btn = ttk.Button(button_frame, text="Speichern", command=save_new_roman)
        save_btn.pack(side="right", padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Abbrechen", command=dialog.destroy)
        cancel_btn.pack(side="right", padx=5)
    
    def _delete_roman(self):
        """Löscht den ausgewählten Römer"""
        selection = self.tree.selection()
        if not selection or not self.app:
            return
            
        # Index des ausgewählten Elements
        item = self.tree.item(selection[0])
        values = item["values"]
        
        # Finde den Index des ausgewählten Römers
        roman_index = None
        for i, roman in enumerate(self.app.romans):
            if roman.get("Name", "") == values[0]:
                roman_index = i
                break
        
        if roman_index is not None:
            # Bestätigungsdialog
            confirm = messagebox.askyesno(
                "Römer löschen",
                f"Möchten Sie den Römer '{values[0]}' wirklich löschen?",
                parent=self
            )
            
            if confirm:
                # Römer löschen
                self.app.RemoveRoman(roman_index)
                
                # Tabelle aktualisieren
                self._load_data()
                
                # Details leeren
                self._clear_details()
    
    def _save_roman_tab(self, tab_name):
        """Speichert die Änderungen eines Tabs für den aktuellen Römer"""
        if not self.current_roman or not self.app:
            return
        
        # Je nach Tab verschiedene Daten speichern
        if tab_name == "basic":
            # Grunddaten
            changes = {}
            
            new_name = self.basic_entries["name"].get()
            if new_name != self.current_roman.get("Name", ""):
                changes["Name"] = new_name
            
            new_geburt = self.basic_entries["geburtsdatum"].get()
            if new_geburt != self.current_roman.get("Geburtsdatum", ""):
                changes["Geburtsdatum"] = new_geburt
            
            new_tod = self.basic_entries["sterbedatum"].get()
            if new_tod != self.current_roman.get("Sterbedatum", ""):
                changes["Sterbedatum"] = new_tod
            
            new_todesursache = self.basic_entries["todesursache"].get()
            if new_todesursache != self.current_roman.get("Todesursache", ""):
                changes["Todesursache"] = new_todesursache
            
            # Änderungen anwenden
            for property_name, new_value in changes.items():
                self.app.EditRomanProperty(self.current_roman, property_name, new_value)
            
        elif tab_name == "marriage":
            # Ehepartner
            new_frequency = self.marriage_frequency_var.get()
            if new_frequency != self.current_roman.get("Häufigkeit Heirat", ""):
                self.app.EditRomanProperty(self.current_roman, "Häufigkeit Heirat", new_frequency)
            
            partners = []
            for entry in self.marriage_entries:
                value = entry.get().strip()
                partners.append(value)
            
            self.app.EditRomanProperty(self.current_roman, "Männer", partners)
            
        elif tab_name == "children":
            # Kinder
            new_count = self.children_count_var.get()
            if new_count != self.current_roman.get("Anzahl Kinder", ""):
                self.app.EditRomanProperty(self.current_roman, "Anzahl Kinder", new_count)
            
            children = []
            for entry in self.children_entries:
                value = entry.get().strip()
                children.append(value)
            
            self.app.EditRomanProperty(self.current_roman, "Kinder", children)
            
        elif tab_name == "family":
            # Familie und Vorfahren
            changes = {}
            
            new_familie = self.family_entries["familie"].get("1.0", tk.END).strip()
            if new_familie != self.current_roman.get("Familie", ""):
                changes["Familie"] = new_familie
            
            new_vorfahren = self.family_entries["vorfahren"].get("1.0", tk.END).strip()
            if new_vorfahren != self.current_roman.get("Vorfahren", ""):
                changes["Vorfahren"] = new_vorfahren
            
            new_verlobung = self.family_entries["verlobung"].get("1.0", tk.END).strip()
            if new_verlobung != self.current_roman.get("Verlobung", ""):
                changes["Verlobung"] = new_verlobung
            
            # Änderungen anwenden
            for property_name, new_value in changes.items():
                self.app.EditRomanProperty(self.current_roman, property_name, new_value)
            
        elif tab_name == "special":
            # Besonderheiten
            besonderheiten = self.current_roman.get("Individuelle Besonderheiten", {})
            
            new_besonderheiten = {
                "Auftreten": self.special_entries["auftreten"].get("1.0", tk.END).strip(),
                "Kleidung": self.special_entries["kleidung"].get("1.0", tk.END).strip(),
                "Schmuck": self.special_entries["schmuck"].get("1.0", tk.END).strip()
            }
            
            self.app.EditRomanProperty(self.current_roman, "Individuelle Besonderheiten", new_besonderheiten)
            
            # Inszenierung
            inszenierung = self.current_roman.get("Inszenierung", {})
            
            new_inszenierung = {
                "Öffentlich": self.inszenierung_entries["öffentlich"].get("1.0", tk.END).strip(),
                "Privat": self.inszenierung_entries["privat"].get("1.0", tk.END).strip()
            }
            
            self.app.EditRomanProperty(self.current_roman, "Inszenierung", new_inszenierung)
            
        elif tab_name == "honors":
            # Ehrungen
            ehrungen = self.current_roman.get("Ehrungen", {})
            
            new_ehrungen = {
                "Augusta-Titel": self.honors_entries["augusta_titel"].get("1.0", tk.END).strip(),
                "Carpentum-Recht": self.honors_entries["carpentum_recht"].get("1.0", tk.END).strip(),
                "Weitere": self.honors_entries["weitere"].get("1.0", tk.END).strip()
            }
            
            self.app.EditRomanProperty(self.current_roman, "Ehrungen", new_ehrungen)
            
        elif tab_name == "sources":
            # Quellen
            quellen = self.current_roman.get("Quellen", {})
            
            new_quellen = {
                "Divinisierung": self.sources_entries["divinisierung"].get("1.0", tk.END).strip(),
                "Bestattung": self.sources_entries["bestattung"].get("1.0", tk.END).strip(),
                "Archäologische Quellen": self.sources_entries["archäologische_quellen"].get("1.0", tk.END).strip(),
                "Münzen": self.sources_entries["münzen"].get("1.0", tk.END).strip(),
                "Inschriften": self.sources_entries["inschriften"].get("1.0", tk.END).strip(),
                "Literarische Quellen": {
                    "Autor": self.lit_sources_entries["autor"].get("1.0", tk.END).strip(),
                    "Werk": self.lit_sources_entries["werk"].get("1.0", tk.END).strip()
                }
            }
            
            self.app.EditRomanProperty(self.current_roman, "Quellen", new_quellen)
        
        # Tabelle aktualisieren
        self._load_data()
        
        # Erfolgsmeldung
        messagebox.showinfo("Änderungen gespeichert", "Die Änderungen wurden erfolgreich gespeichert.", parent=self)
    
    def _filter_table(self, event):
        """Filtert die Tabelle nach dem Suchbegriff"""
        search_term = self.search_var.get().lower()
        
        # Alle Einträge entfernen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Gefilterte Daten hinzufügen
        for roman in self.app.romans:
            name = roman.get("Name", "").lower()
            geburt = str(roman.get("Geburtsdatum", "")).lower()
            tod = str(roman.get("Sterbedatum", "")).lower()
            familie = roman.get("Familie", "").lower()
            
            # Wenn der Suchbegriff in einem der Felder vorkommt
            if (search_term in name or search_term in geburt or
                search_term in tod or search_term in familie):
                
                self.tree.insert("", "end", values=(
                    roman.get("Name", ""),
                    roman.get("Geburtsdatum", ""),
                    roman.get("Sterbedatum", ""),
                    roman.get("Familie", "")
                ))
    
    def UpdateData(self, data=None) -> None:
        """Aktualisiert die Daten im Frame"""
        self._load_data()