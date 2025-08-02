import tkinter as tk
from tkinter import ttk
import os
import sys

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.commands import EditRomanCommand
from utils.config import AppColors, Fonts
from ui.frames.content.base_content import BaseContentFrame
from utils.logger import logger

class CreateFrame(BaseContentFrame):
    # Statische Variable
    last_selected_tab = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.__current_roman = None
        self.__app = self.FindMainApp(parent)
        self.CreateUi()

    def FindMainApp(self, widget):
        """Rekursive Suche nach der Main-App in der obersten Ebene"""
        ret = None
        if hasattr(widget, 'romans'):
            ret = widget
        elif widget.master:
            ret = self.FindMainApp(widget.master)
        return ret
    
    def CreateUi(self) -> None:
        # Hauptcontainer
        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 10)
        self.columnconfigure(0, weight=1)

        # Tabellenansicht
        top_frame = tk.Frame(self, bg = AppColors.CONTENT_FRAME)
        top_frame.grid(row=0, column = 0, sticky=tk.NSEW, padx = 10, pady=(10, 5))

        # Header mit Suchfeld
        header_frame = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        header_label = tk.Label(header_frame, text='Editieren von Römern', font=Fonts.HEADER, bg = AppColors.CONTENT_FRAME, fg=AppColors.KU_COLOR)
        header_label.pack(side=tk.LEFT, padx = 10)

        # Suchfeld
        search_frame = tk.Frame(header_frame, bg = AppColors.CONTENT_FRAME)
        search_frame.pack(side=tk.RIGHT, padx=10)

        search_label = tk.Label(search_frame, bg=AppColors.CONTENT_FRAME, fg=AppColors.KU_COLOR, font=Fonts.STANDARD_BOLD, text='Suche')
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        seacrh_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, font=Fonts.STANDARD, fg = AppColors.KU_COLOR, bd=1, relief=tk.SOLID)
        seacrh_entry.pack(side=tk.LEFT, padx=(0, 10))
        seacrh_entry.bind('<KeyRelease>', self.FilterTable)

        # Tabelle
        table_frame = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        table_frame.pack(fill=tk.BOTH, expand=True)

        y_scrollbar = ttk.Scrollbar(table_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Style konfigurieren
        style_name = 'CustomTreeview.Treeview'
        style = self.ConfigureTreeviewStyle(style_name)

        columns = ('Name', 'Geburt', 'Tod', 'Todesursache', 'Familie', 'Ehemänner', 'Kinder')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scrollbar.set,
            style=style_name,
            selectmode=tk.BROWSE
        )

        # Scrollbars mit Treeview verbinden
        y_scrollbar.config(command=self.tree.yview)

        # Spaltenüberschriften definieren
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, anchor=tk.CENTER)
        
        for roman in self.__app.romans:
            self.tree.insert('', tk.END, values=(
                roman['Name'], 
                roman['Geburtsdatum'], 
                roman['Sterbedatum'], 
                roman['Todesursache'], 
                roman['Familie'],
                roman['Häufigkeit Heirat'], 
                roman['Anzahl Kinder']))
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        buttons_frame = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        # Create button
        self.create_button = ttk.Button(
            buttons_frame, 
            text="Neuen Römer erstellen", 
            command=self.CreateNewRoman
        )
        self.create_button.pack(side=tk.LEFT, padx=(10, 5))

        # Delete button
        self.delete_button = ttk.Button(
            buttons_frame, 
            text="Ausgewählten Römer löschen", 
            command=self.DeleteSelectedRoman,
            state=tk.DISABLED  # Initially disabled
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Event-Binding für Auswahl
        self.tree.bind('<<TreeviewSelect>>', self.OnSelect)
        self.tree.bind('<ButtonRelease-1>', self.OnTreeClick)
        self.tree.bind('<Shift-Button-1>', lambda e: "break")
        self.tree.bind('<Shift-ButtonRelease-1>', lambda e: "break")

        # Trennstrich
        seperator = ttk.Separator(self, orient=tk.HORIZONTAL)
        seperator.grid(row=1, column=0, sticky=tk.EW, padx=10)

        # Detailansicht
        bottom_frame = tk.Frame(self, bg=AppColors.CONTENT_FRAME)
        bottom_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=(5, 10))

        # Header für Detailansicht
        detail_header = tk.Label(
            bottom_frame,
            text='Details',
            font=Fonts.HEADER,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        detail_header.pack(anchor=tk.W, padx=10)

        self.notebook = ttk.Notebook(bottom_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Registerkarten erstellen
        self.tab_basic = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_marriage = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_children = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_family = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_special = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_honors = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)
        self.tab_sources = tk.Frame(self.notebook, bg=AppColors.CONTENT_FRAME)

        self.notebook.add(self.tab_basic, text='Grunddaten')
        self.notebook.add(self.tab_marriage, text='Ehen')
        self.notebook.add(self.tab_children, text='Kinder')
        self.notebook.add(self.tab_family, text='Familie')
        self.notebook.add(self.tab_special, text='Besonderheiten')
        self.notebook.add(self.tab_honors, text='Ehrungen')
        self.notebook.add(self.tab_sources, text='Quellen')

        # Inhalt der Tabs erstellen
        self.CreateBasicTab()
        self.CreateMarriageTab()
        self.CreateChildrenTab()
        #self.CreateFamilyTab()
        #self.CreateSpecialTab()
        #self.CreateHonorsTab()
        #self.CreateSourcesTab()

        self.notebook.bind('<<NotebookTabChanged>>', self.OnTabChanged)
        self.notebook.select(CreateFrame.last_selected_tab)

        # Zunächst leere Felder
        #self.ClearDetails()
        
        # Tabelle mit Daten füllen
        #self.LoadData()
    
    def OnTabChanged(self, event):
        CreateFrame.last_selected_tab = self.notebook.index('current')

    def ConfigureTreeviewStyle(self, style_name):
        style = ttk.Style()
        
        # Grundlegende Treeview-Konfiguration
        style.configure('Treeview',
                        background=AppColors.CONTENT_FRAME,
                        foreground=AppColors.KU_COLOR,
                        rowheight=25,
                        fieldbackground=AppColors.CONTENT_FRAME)
        
        # Überschriften anpassen
        style.configure('Treeview.Heading',
                        background=AppColors.CONTENT_FRAME,
                        foreground=AppColors.KU_COLOR,
                        relief=tk.FLAT,
                        font=Fonts.STANDARD)
        
        # Ausgewählte Zeilen anpassen
        style.map('Treeview',
            background=[('selected', AppColors.HIGHLIGHT)],
            foreground=[('selected', AppColors.KU_COLOR)])
        
        style.map('Treeview.Heading',
          background=[('active', AppColors.HIGHLIGHT)],
          foreground=[('active', AppColors.KU_COLOR)])

        style.configure(style_name, 
                        font=Fonts.SUBMENU,  # Schriftart für Zellen
                        rowheight=30)        # Höhere Zeilen
        
        return style
    
    def CreateBasicTab(self):
        """Erstellt die Grunddaten-Registerkarte"""
        for widget in self.tab_basic.winfo_children():
            widget.destroy()
        form_frame = tk.Frame(self.tab_basic, bg=AppColors.CONTENT_FRAME)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Formularfelder für Grunddaten
        fields = ['Name', 'Geburtsdatum', 'Sterbedatum', 'Todesursache']

        self.basic_entries = {}
        
        for i, field_key in enumerate(fields):
            label = tk.Label(
                form_frame,
                text=f'{field_key}:',
                font=Fonts.SUBMENU,
                bg=AppColors.CONTENT_FRAME,
                fg=AppColors.KU_COLOR,
                anchor=tk.W
            )
            label.grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = tk.Entry(form_frame, width=40, font=Fonts.STANDARD, fg = AppColors.KU_COLOR, bd=1, relief=tk.SOLID)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            
            self.basic_entries[field_key] = entry
        
        # Speicher-Button
        save_frame = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        save_frame.grid(row=len(fields), column=0, columnspan=2, sticky=tk.SE, pady=10)
        
        save_button = ttk.Button(save_frame, text='Änderungen speichern', command=lambda: self.SaveRomanTab('basic'))
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Form-Frame dehnbar machen
        form_frame.columnconfigure(1, weight=1)
    
    def CreateMarriageTab(self):
        """Erstellt die Ehen-Registerkarte"""
        for widget in self.tab_marriage.winfo_children():
            widget.destroy()
                
        form_frame = tk.Frame(self.tab_marriage, bg=AppColors.CONTENT_FRAME)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Häufigkeit Heirat
        frequency_label = tk.Label(
            form_frame,
            text='Häufigkeit Heirat:',
            font=Fonts.SUBMENU,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            anchor=tk.W
        )
        frequency_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.marriage_frequency_var = tk.StringVar()
        frequency_entry = tk.Entry(
            form_frame, 
            textvariable=self.marriage_frequency_var, 
            width=40, 
            font=Fonts.STANDARD, 
            fg=AppColors.KU_COLOR, 
            bd=1, 
            relief=tk.SOLID
        )
        frequency_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Verlobung
        engagement_label = tk.Label(
            form_frame,
            text='Verlobung:',
            font=Fonts.SUBMENU,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            anchor=tk.W
        )
        engagement_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.engagement_var = tk.StringVar()
        frequency_entry = tk.Entry(
            form_frame, 
            textvariable=self.engagement_var, 
            width=40, 
            font=Fonts.STANDARD, 
            fg=AppColors.KU_COLOR, 
            bd=1, 
            relief=tk.SOLID
        )
        frequency_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Überschrift für Ehepartner
        partner_label = tk.Label(
            form_frame,
            text='Ehepartner:',
            font=Fonts.SUBMENU,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            anchor=tk.W
        )
        partner_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(15, 5))
        
        # Container für die Ehepartner-Einträge
        self.marriage_container = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        self.marriage_container.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=10)
        
        self.marriage_entries = []
        self.marriage_frames = []
        
        # Erstes Ehepartner-Feld hinzufügen
        self.AddDynamicField(self.marriage_entries, self.marriage_frames, self.marriage_container)
        
        # Button-Bereich am unteren Rand
        buttons_row = 4
        
        # 'Feld hinzufügen'-Button (links) - KORRIGIERT
        add_button = ttk.Button(
            form_frame, 
            text='Ehemann hinzufügen', 
            command=lambda: self.AddDynamicField(self.marriage_entries, self.marriage_frames, self.marriage_container)
        )
        add_button.grid(row=buttons_row, column=0, sticky=tk.W, padx=10, pady=10)
        
        # Speicher-Button (rechts)
        save_frame = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        save_frame.grid(row=buttons_row, column=1, sticky=tk.SE, pady=10)
        
        save_button = ttk.Button(save_frame, text='Änderungen speichern', command=lambda: self.SaveRomanTab('marriage'))
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Form-Frame dehnbar machen
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(2, weight=1)

    def AddDynamicField(self, entries_list, frames_list, container):
        """Fügt ein weiteres Feld für Ehepartner oder Kinder hinzu"""
        # Der Index ist die aktuelle Anzahl der Einträge
        i = len(entries_list)
        
        # Erstelle den Frame mit dem Container als Parent
        entry_frame = tk.Frame(container, bg=AppColors.CONTENT_FRAME)
        entry_frame.pack(fill=tk.X, pady=2)
        
        # Index-Label
        label = tk.Label(
            entry_frame, 
            text=f'{i+1}:', 
            width=2, 
            bg=AppColors.CONTENT_FRAME, 
            fg=AppColors.KU_COLOR,
            font=Fonts.STANDARD
        )
        label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Eingabefeld
        entry = tk.Entry(
            entry_frame, 
            width=40, 
            font=Fonts.STANDARD, 
            fg=AppColors.KU_COLOR, 
            bd=1, 
            relief=tk.SOLID
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # X-Button zum Löschen (für alle außer dem ersten Feld)
        if i > 0:
            delete_button = tk.Button(
                entry_frame,
                text="✕",
                font=("Arial", 8, "bold"),
                fg=AppColors.KU_COLOR,
                bg=AppColors.CONTENT_FRAME,
                bd=1,
                padx=5,
                relief=tk.SOLID,
                cursor="hand2"
            )
            delete_button.pack(side=tk.RIGHT, padx=(5, 0))
            
            # Speichere den aktuellen Index für den Delete-Handler
            current_index = i
            delete_button.configure(
                command=lambda frame=entry_frame, idx=current_index: 
                    self.DeleteDynamicField(frame, idx, entries_list, frames_list, container)
            )
        
        # Füge das neue Feld zu den Listen hinzu
        entries_list.append(entry)
        frames_list.append(entry_frame)
        
        return entry

    def DeleteDynamicField(self, frame, index, entries_list, frames_list, container):
        """Löscht ein dynamisches Feld"""
        # Frame aus der Oberfläche entfernen
        frame.destroy()
        
        # Einträge aus den Listen entfernen
        if 0 <= index < len(entries_list):
            del entries_list[index]
            del frames_list[index]
        
        # Alle Buttons neu erstellen, um ihre Indizes zu aktualisieren
        self.RecreateDeleteButtons(entries_list, frames_list, container)
        
    def RecreateDeleteButtons(self, entries_list, frames_list, container):
        """Aktualisiert alle Löschen-Buttons mit korrekten Indizes"""
        # Zuerst Indizes der Labels aktualisieren
        for i, frame in enumerate(frames_list):
            # Label aktualisieren
            for child in frame.winfo_children():
                if isinstance(child, tk.Label) and child.cget("width") == 2:
                    child.config(text=f'{i+1}:')
                
                # Alte Buttons entfernen
                if isinstance(child, tk.Button) and child.cget("text") == "✕":
                    child.destroy()
            
            # Neuen Button erstellen (außer für das erste Feld)
            if i > 0:
                delete_button = tk.Button(
                    frame,
                    text="✕",
                    font=("Arial", 8, "bold"),
                    fg=AppColors.KU_COLOR,
                    bg=AppColors.CONTENT_FRAME,
                    bd=1,
                    padx=5,
                    relief=tk.SOLID,
                    cursor="hand2"
                )
                delete_button.pack(side=tk.RIGHT, padx=(5, 0))
                delete_button.configure(
                    command=lambda f=frame, idx=i: 
                        self.DeleteDynamicField(f, idx, entries_list, frames_list, container)
                )

    def CreateChildrenTab(self):
        """Erstellt die Kinder-Registerkarte"""
        for widget in self.tab_children.winfo_children():
            widget.destroy()
                
        form_frame = tk.Frame(self.tab_children, bg=AppColors.CONTENT_FRAME)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Anzahl Kinder
        frequency_label = tk.Label(
            form_frame,
            text='Anzahl Kinder:',
            font=Fonts.SUBMENU,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            anchor=tk.W
        )
        frequency_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.children_count_var = tk.StringVar()
        count_entry = tk.Entry(
            form_frame, 
            textvariable=self.children_count_var, 
            width=40, 
            font=Fonts.STANDARD, 
            fg=AppColors.KU_COLOR, 
            bd=1, 
            relief=tk.SOLID
        )
        count_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Überschrift für Kinder
        children_label = tk.Label(
            form_frame,
            text='Kinder:',
            font=Fonts.SUBMENU,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            anchor=tk.W
        )
        children_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(15, 5))
        
        # Container für die Kinder-Einträge
        self.children_container = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        self.children_container.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=10)
        
        self.children_entries = []
        self.children_frames = []
        
        # Erstes Kind-Feld hinzufügen
        self.AddDynamicField(self.children_entries, self.children_frames, self.children_container)
        
        # Button-Bereich am unteren Rand
        buttons_row = 3
        
        # 'Feld hinzufügen'-Button (links) - KORRIGIERT
        add_button = ttk.Button(
            form_frame, 
            text='Kind hinzufügen', 
            command=lambda: self.AddDynamicField(self.children_entries, self.children_frames, self.children_container)
        )
        add_button.grid(row=buttons_row, column=0, sticky=tk.W, padx=10, pady=10)
        
        # Speicher-Button (rechts)
        save_frame = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        save_frame.grid(row=buttons_row, column=1, sticky=tk.SE, pady=10)
        
        save_button = ttk.Button(save_frame, text='Änderungen speichern', command=lambda: self.SaveRomanTab('children'))
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Form-Frame dehnbar machen
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(2, weight=1)

    def OnSelect(self, event):
        """Behandelt die Auswahl in der Tabelle"""
        selection = self.tree.selection()
    
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.__current_roman = None
            for roman in self.__app.romans:
                if roman.get('Name', '') == values[0]:
                    self.__current_roman = roman
                    break
            
            if self.__current_roman is not None:
                self.DisplayRoman()
        else:
            self.__current_roman = None
            self.ClearDetails()
        
        self.UpdateButtonStates()
    
    def DisplayRoman(self):
        """Zeigt die Daten des ausgewählten Romans in den Detail-Tabs an"""
        if self.__current_roman:
            # Basic Tab: Alle Felder mit einem Durchgang füllen
            field_mapping = {
                'Name': 'Name',
                'Geburtsdatum': 'Geburtsdatum', 
                'Sterbedatum': 'Sterbedatum',
                'Todesursache': 'Todesursache'
            }
            
            for ui_field, data_field in field_mapping.items():
                if ui_field in self.basic_entries:
                    self.basic_entries[ui_field].delete(0, tk.END)
                    self.basic_entries[ui_field].insert(0, self.__current_roman.get(data_field, ''))
            
            # Marriage Tab: Frequenz setzen
            self.marriage_frequency_var.set(self.__current_roman.get('Häufigkeit Heirat', ''))
            self.engagement_var.set(self.__current_roman.get('Verlobung', ''))
            
            # Marriage Tab: Entferne alle zusätzlichen Felder und behalte nur das erste
            if len(self.marriage_entries) > 1:
                for i in range(len(self.marriage_entries) - 1, 0, -1):
                    self.marriage_frames[i].destroy()
                
                # Nur das erste Feld behalten, Rest entfernen
                self.marriage_entries = [self.marriage_entries[0]]
                self.marriage_frames = [self.marriage_frames[0]]
            
            # Marriage Tab: Ehemänner-Felder erstellen für nicht-leere Einträge
            husbands = self.__current_roman.get('Männer', [])
            if husbands:
                # Erstes Feld füllen
                self.marriage_entries[0].delete(0, tk.END)
                if len(husbands) > 0:
                    self.marriage_entries[0].insert(0, husbands[0] if husbands[0] else '')
                
                # Zusätzliche Felder für weitere Ehemänner hinzufügen
                for i in range(1, len(husbands)):
                    if husbands[i]:  # Nur nicht-leere Einträge
                        self.AddDynamicField(self.marriage_entries, self.marriage_frames, self.marriage_container)
                        self.marriage_entries[-1].delete(0, tk.END)
                        self.marriage_entries[-1].insert(0, husbands[i])
            
            # Children Tab: Frequenz setzen
            self.children_count_var.set(self.__current_roman.get('Anzahl Kinder', ''))
            
            # Children Tab: Entferne alle zusätzlichen Felder und behalte nur das erste
            if len(self.children_entries) > 1:
                for i in range(len(self.children_entries) - 1, 0, -1):
                    self.children_frames[i].destroy()
                
                # Nur das erste Feld behalten, Rest entfernen
                self.children_entries = [self.children_entries[0]]
                self.children_frames = [self.children_frames[0]]
            
            # Children Tab: Kinder-Felder erstellen für nicht-leere Einträge
            children = self.__current_roman.get('Kinder', [])
            if children:
                # Erstes Feld füllen
                self.children_entries[0].delete(0, tk.END)
                if len(children) > 0:
                    self.children_entries[0].insert(0, children[0] if children[0] else '')
                
                # Zusätzliche Felder für weitere Kinder hinzufügen
                for i in range(1, len(children)):
                    if children[i]:  # Nur nicht-leere Einträge
                        self.AddDynamicField(self.children_entries, self.children_frames, self.children_container)
                        self.children_entries[-1].delete(0, tk.END)
                        self.children_entries[-1].insert(0, children[i])

    def FilterTable(self, event):
        """Filtert die Tabelle nach dem Suchbegriff und durchsucht alle Felder"""
        search_term = self.search_var.get().lower()
        
        # Alle Einträge entfernen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Wenn kein Suchbegriff, zeige alle
        if not search_term:
            self.LoadTableData()
            return
        
        # Gefilterte Daten hinzufügen
        for roman in self.__app.romans:
            # Durchsuche alle Werte im Dictionary rekursiv
            if self.SearchInValues(roman, search_term):
                self.tree.insert('', 'end', values=(
                    roman.get('Name', ''),
                    roman.get('Geburtsdatum', ''),
                    roman.get('Sterbedatum', ''),
                    roman.get('Todesursache', ''),
                    roman.get('Familie', ''),
                    roman.get('Häufigkeit Heirat', ''),
                    roman.get('Anzahl Kinder', '')
                ))
        
    def SearchInValues(self, obj, search_term):
        """Rekursiv alle Werte in einem Objekt durchsuchen"""
        # Für Dictionary-Objekte
        if isinstance(obj, dict):
            for value in obj.values():
                if self.SearchInValues(value, search_term):
                    return True
                    
        # Für Listen oder Tupel
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                if self.SearchInValues(item, search_term):
                    return True
        
        # Für einfache Werte (Strings, Zahlen, etc.)
        else:
            return search_term in str(obj).lower()
        
        return False

    def LoadTableData(self):
        """Lädt alle Daten in die Tabelle"""
        for roman in self.__app.romans:
            self.tree.insert('', 'end', values=(
                roman.get('Name', ''),
                roman.get('Geburtsdatum', ''),
                roman.get('Sterbedatum', ''),
                roman.get('Todesursache', ''),
                roman.get('Familie', ''),
                roman.get('Häufigkeit Heirat', ''),
                roman.get('Anzahl Kinder', '')
            ))
    
    def SaveRomanTab(self, tab_name):
        """Speichert die Änderungen eines Tabs für den aktuellen Römer mit Command-Pattern"""
        if not self.__current_roman or not self.__app:
            return
        
        # Command-Manager aus der App holen
        command_manager = self.__app.command_manager
        
        match(tab_name):
            case 'basic':
                 # Grunddaten speichern
                for field_name, entry in self.basic_entries.items():
                    new_value = entry.get()
                    old_value = self.__current_roman.get(field_name, '')
                    
                    if new_value != old_value:
                        # Erstelle und führe EditRomanCommand aus
                        command = EditRomanCommand(self.__current_roman, field_name, new_value)
                        command_manager.ExecuteCommand(command)
            case 'marriage':
                # Häufigkeit der Heirat speichern
                new_frequency = self.marriage_frequency_var.get()
                new_engagement = self.engagement_var.get()
                old_frequency = self.__current_roman.get('Häufigkeit Heirat', '')
                old_engagement = self.__current_roman.get('Verlobung', '')
                
                if new_frequency != old_frequency:
                    command = EditRomanCommand(self.__current_roman, 'Häufigkeit Heirat', new_frequency)
                    command_manager.ExecuteCommand(command)

                if new_engagement != old_engagement:
                    command = EditRomanCommand(self.__current_roman, 'Verlobung', new_engagement)
                    command_manager.ExecuteCommand(command)
                
                # Ehemänner speichern
                husbands = []
                for entry in self.marriage_entries:
                    husbands.append(entry.get())
                
                old_husbands = self.__current_roman.get('Männer', [])
                if husbands != old_husbands:
                    command = EditRomanCommand(self.__current_roman, 'Männer', husbands)
                    command_manager.ExecuteCommand(command)
           
            case 'children':
                # Anzahl der Kinder speichern
                new_count = self.children_count_var.get()
                old_count = self.__current_roman.get('Anzahl Kinder', '')
                
                if new_count != old_count:
                    command = EditRomanCommand(self.__current_roman, 'Anzahl Kinder', new_count)
                    command_manager.ExecuteCommand(command)
                
                # Kinder speichern
                children = []
                for entry in self.children_entries:
                    children.append(entry.get())
                
                old_children = self.__current_roman.get('Kinder', [])
                if children != old_children:
                    command = EditRomanCommand(self.__current_roman, 'Kinder', children)
                    command_manager.ExecuteCommand(command)
        
            case 'family':
                # Familie speichern (falls implementiert)
                new_family = self.family_entry.get() if hasattr(self, 'family_entry') else ''
                old_family = self.__current_roman.get('Familie', '')
                
                if new_family != old_family:
                    command = EditRomanCommand(self.__current_roman, 'Familie', new_family)
                    command_manager.ExecuteCommand(command)
        
        # Nach dem Speichern die Tabelle aktualisieren
        self.UpdateTableRow()
        self.LoadTableData()
        self.__app.file_modified = True
        self.__app.menu_manager.UpdateEditMenuState()
        
        # Bestätigungsmeldung anzeigen
        logger.info(f"Änderungen am Tab '{tab_name}' für Römer '{self.__current_roman.get('Name', '')}' gespeichert")

    def UpdateTableRow(self):
        """Aktualisiert die ausgewählte Zeile in der Tabelle"""
        selection = self.tree.selection()
        if not selection:
            return
            
        # Aktualisiere die Werte in der Tabelle
        item_id = selection[0]
        self.tree.item(item_id, values=(
            self.__current_roman.get('Name', ''),
            self.__current_roman.get('Geburtsdatum', ''),
            self.__current_roman.get('Sterbedatum', ''),
            self.__current_roman.get('Todesursache', ''),
            self.__current_roman.get('Familie', ''),
            self.__current_roman.get('Häufigkeit Heirat', ''),
            self.__current_roman.get('Anzahl Kinder', '')
        ))

    def CreateFamilyTab(self):
        """Erstellt die Familie-Registerkarte"""
        for widget in self.tab_family.winfo_children():
            widget.destroy()
            
        form_frame = tk.Frame(self.tab_family, bg=AppColors.CONTENT_FRAME)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Familie-Label
        family_label = tk.Label(
            form_frame,
            text='Familie:',
            font=Fonts.SUBMENU,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            anchor=tk.W
        )
        family_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        # Familie-Eingabefeld
        self.family_entry = tk.Entry(
            form_frame, 
            width=40, 
            font=Fonts.STANDARD, 
            fg=AppColors.KU_COLOR, 
            bd=1, 
            relief=tk.SOLID
        )
        self.family_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Wenn ein Roman ausgewählt ist, Wert setzen
        if self.__current_roman:
            self.family_entry.delete(0, tk.END)
            self.family_entry.insert(0, self.__current_roman.get('Familie', ''))
        
        # Speicher-Button
        save_frame = tk.Frame(form_frame, bg=AppColors.CONTENT_FRAME)
        save_frame.grid(row=1, column=1, sticky=tk.SE, pady=10)
        
        save_button = ttk.Button(save_frame, text='Änderungen speichern', command=lambda: self.SaveRomanTab('family'))
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Form-Frame dehnbar machen
        form_frame.columnconfigure(1, weight=1)

    def OnTreeClick(self, event):
        """An- und Abwahl von Optionen der Tabelle"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell" or region == "tree":
            item_id = self.tree.identify_row(event.y)
            if item_id:
                if item_id in self.tree.selection() and len(self.tree.selection()) == 1:
                    if hasattr(self, '_last_clicked_item') and self._last_clicked_item == item_id:
                        self.tree.selection_remove(item_id)
                        self.__current_roman = None
                        self.ClearDetails()
                        self.UpdateButtonStates()
                    
                    self._last_clicked_item = item_id

    def ClearDetails(self):
        """Löscht Detailfelder"""
        # Basic tab
        for entry in self.basic_entries.values():
            entry.delete(0, tk.END)
        
        # Marriage tab
        self.marriage_frequency_var.set("")
        self.engagement_var.set("")
        for entry in self.marriage_entries:
            entry.delete(0, tk.END)
        
        # Children tab
        self.children_count_var.set("")
        for entry in self.children_entries:
            entry.delete(0, tk.END)

    def UpdateButtonStates(self):
        """Aktivieren/Deaktivieren der Buttons"""
        if self.__current_roman:
            self.create_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.create_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.DISABLED)

    def CreateNewRoman(self):
        pass

    def DeleteSelectedRoman(self):
        pass