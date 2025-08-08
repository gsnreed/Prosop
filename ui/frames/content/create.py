import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.commands import EditRomanCommand
from utils.config import AppColors, Fonts, UIConstants, Icons, Messages
from ui.frames.content.base_content import BaseContentFrame
from data.models.roman import Roman
from utils.logger import logger

class CreateFrame(BaseContentFrame):
    # Statische Variable
    last_selected_tab = 0
    
    def __init__(self, parent):
        super().__init__(parent)
        self.__current_roman = None
        self.__app = self.master.master
        self.sort_column = None
        self.sort_reverse = False
        self.CreateUi()

    def CreateUi(self):
        # Hauptcontainer Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hauptcontainer für bessere Trennung
        main_container = tk.Frame(self, bg=AppColors.BACKGROUND)
        main_container.grid(row=0, column=0, sticky=tk.NSEW)
        main_container.rowconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        main_container.columnconfigure(0, weight=1)

        # ========== OBERER BEREICH: Tabelle ==========
        top_container = tk.Frame(main_container, bg=AppColors.BACKGROUND)
        top_container.grid(row=0, column=0, sticky=tk.NSEW, padx=UIConstants.PADDING_LARGE, pady=(UIConstants.PADDING_LARGE, UIConstants.PADDING_SMALL))
        
        # Rahmen mit Schatten-Effekt
        top_frame = tk.Frame(top_container, bg=AppColors.CONTENT_FRAME, relief=tk.RAISED, bd=1)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header-Bereich
        header_frame = tk.Frame(top_frame, bg=AppColors.KU_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header-Inhalt Container
        header_content = tk.Frame(header_frame, bg=AppColors.KU_COLOR)
        header_content.pack(fill=tk.BOTH, expand=True, padx=UIConstants.PADDING_XLARGE, pady=UIConstants.PADDING_MEDIUM)
        
        # Titel mit Icon
        title_frame = tk.Frame(header_content, bg=AppColors.KU_COLOR)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        header_label = tk.Label(
            title_frame, 
            text=f'{Icons.SCROLL} Römerverwaltung', 
            font=Fonts.HEADER_LARGE, 
            bg=AppColors.KU_COLOR, 
            fg=AppColors.BUTTON_PRIMARY_FG
        )
        header_label.pack(side=tk.LEFT)
        
        # Suchbereich mit modernem Design
        search_container = tk.Frame(header_content, bg=AppColors.KU_COLOR)
        search_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        search_frame = tk.Frame(search_container, bg=AppColors.SEARCH_BG, relief=tk.RIDGE, bd=1)
        search_frame.pack(fill=tk.Y)
        
        # Such-Icon
        search_icon = tk.Label(
            search_frame, 
            text=Icons.SEARCH, 
            bg=AppColors.SEARCH_BG, 
            fg=AppColors.SEARCH_FG,
            font=Fonts.ICON
        )
        search_icon.pack(side=tk.LEFT, padx=(UIConstants.PADDING_MEDIUM, UIConstants.PADDING_SMALL))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            width=35,
            font=Fonts.INPUT, 
            fg=AppColors.SEARCH_FG,
            bg=AppColors.SEARCH_BG,
            bd=0,
            insertbackground=AppColors.SEARCH_FG
        )
        search_entry.pack(side=tk.LEFT, fill=tk.Y, pady=8, padx=(0, UIConstants.PADDING_MEDIUM))
        search_entry.bind('<KeyRelease>', self.FilterTable)
        
        # Placeholder-Text
        self.AddPlaceholder(search_entry, Messages.SEARCH_PLACEHOLDER)
        
        # Tabellen-Container
        table_container = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        table_container.pack(fill=tk.BOTH, expand=True, padx=UIConstants.PADDING_LARGE, pady=(UIConstants.PADDING_MEDIUM, UIConstants.PADDING_SMALL))
        
        # Tabelle mit modernem Stil
        self.CreateStyledTable(table_container)
        
        # Button-Bereich
        button_container = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        button_container.pack(fill=tk.X, padx=UIConstants.PADDING_LARGE, pady=(UIConstants.PADDING_SMALL, UIConstants.PADDING_LARGE))
        
        self.CreateActionButtons(button_container)
        
        # ========== UNTERER BEREICH: Details ==========
        bottom_container = tk.Frame(main_container, bg=AppColors.BACKGROUND)
        bottom_container.grid(row=1, column=0, sticky=tk.NSEW, 
                            padx=UIConstants.PADDING_LARGE, 
                            pady=(UIConstants.PADDING_SMALL, UIConstants.PADDING_LARGE))

        # Rahmen mit Schatten-Effekt
        middle_frame = tk.Frame(bottom_container, bg=AppColors.CONTENT_FRAME, relief=tk.RAISED, bd=1)
        middle_frame.pack(fill=tk.BOTH, expand=True)

        # Layout für middle_frame konfigurieren
        middle_frame.grid_rowconfigure(1, weight=1)  # Notebook-Bereich expandiert
        middle_frame.grid_columnconfigure(0, weight=1)

        # Detail-Header (Row 0)
        detail_header_frame = tk.Frame(middle_frame, bg=AppColors.DETAIL_HEADER_BG, height=50)
        detail_header_frame.grid(row=0, column=0, sticky=tk.EW)
        detail_header_frame.grid_propagate(False)

        detail_header_content = tk.Frame(detail_header_frame, bg=AppColors.DETAIL_HEADER_BG)
        detail_header_content.pack(fill=tk.BOTH, expand=True, padx=UIConstants.PADDING_XLARGE, pady=UIConstants.PADDING_MEDIUM)

        detail_label = tk.Label(
            detail_header_content,
            text=f'{Icons.DOCUMENT} Detailansicht',
            font=Fonts.SUBHEADER,
            bg=AppColors.DETAIL_HEADER_BG,
            fg=AppColors.DETAIL_HEADER_FG
        )
        detail_label.pack(side=tk.LEFT)

        # Status-Indikator
        self.status_label = tk.Label(
            detail_header_content,
            text=Messages.NO_SELECTION,
            font=Fonts.STANDARD_ITALIC,
            bg=AppColors.DETAIL_HEADER_BG,
            fg=AppColors.STATUS_FG
        )
        self.status_label.pack(side=tk.RIGHT)

        # Notebook Container (Row 1) - dieser expandiert
        notebook_container = tk.Frame(middle_frame, bg=AppColors.CONTENT_FRAME)
        notebook_container.grid(row=1, column=0, sticky=tk.NSEW, 
                            padx=UIConstants.PADDING_LARGE, 
                            pady=UIConstants.PADDING_MEDIUM)

        self.CreateStyledNotebook(notebook_container)

        # Speichern-Button Container (Row 2) - bleibt immer unten
        save_container = tk.Frame(middle_frame, bg=AppColors.CONTENT_FRAME)
        save_container.grid(row=2, column=0, sticky=tk.EW, 
                        padx=UIConstants.PADDING_LARGE, 
                        pady=(0, UIConstants.PADDING_LARGE))

        self.save_button = self.CreateStyledButton(
            save_container,
            text=f"{Icons.SAVE} Änderungen speichern",
            command=self.SaveChanges,
            style='Success'
        )
        self.save_button.pack(side=tk.RIGHT)

        # Anfangszustand
        self.ClearDetails()
        self.UpdateButtonStates()

    def CreateStyledTable(self, parent):
        """Erstellt eine moderne Tabelle mit verbessertem Design"""
        # Tabellen-Frame
        table_frame = tk.Frame(parent, bg=AppColors.TABLE_BG)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar mit modernem Stil
        scrollbar_frame = tk.Frame(table_frame, bg=AppColors.TABLE_BG, width=12)
        scrollbar_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        y_scrollbar = ttk.Scrollbar(scrollbar_frame, style='Vertical.TScrollbar')
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 0))
        
        # Treeview-Stil konfigurieren
        style = ttk.Style()
        style_name = 'CustomTreeview.Treeview'
        
        style.configure(style_name,
            background=AppColors.TABLE_BG,
            foreground=AppColors.TABLE_FG,
            fieldbackground=AppColors.TABLE_BG,
            borderwidth=0,
            font=Fonts.TABLE
        )
        
        style.configure(f'{style_name}.Heading',
            background=AppColors.TABLE_HEADER_BG,
            foreground=AppColors.KU_COLOR,
            borderwidth=0,
            font=Fonts.TABLE_HEADER
        )
        
        style.map(style_name,
            background=[('selected', AppColors.TABLE_SELECTED_BG)],
            foreground=[('selected', AppColors.TABLE_SELECTED_FG)]
        )
        
        # Spalten definieren
        columns = ('Name', 'Geburt', 'Tod', 'Todesursache', 'Familie', 'Ehemänner', 'Kinder')
        column_widths = {
            'Name': 200,
            'Geburt': 100,
            'Tod': 100,
            'Todesursache': 150,
            'Familie': 120,
            'Ehemänner': 100,
            'Kinder': 80
        }
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='tree headings',
            yscrollcommand=y_scrollbar.set,
            style=style_name,
            selectmode=tk.BROWSE,
            height=10
        )
        
        # Icon-Spalte ausblenden
        self.tree.column('#0', width=0, stretch=False)
        
        # Spalten konfigurieren
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.SortColumn(c))
            self.tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbar verbinden
        y_scrollbar.config(command=self.tree.yview)
        
        # Daten laden
        self.LoadTableData()
        
        # Events
        self.tree.bind('<<TreeviewSelect>>', self.OnSelect)
        self.tree.bind('<Double-Button-1>', self.OnDoubleClick)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def CreateActionButtons(self, parent):
        """Erstellt moderne Action-Buttons"""
        # Linke Button-Gruppe
        left_buttons = tk.Frame(parent, bg=AppColors.CONTENT_FRAME)
        left_buttons.pack(side=tk.LEFT)
        
        self.create_button = self.CreateStyledButton(
            left_buttons,
            text=f"{Icons.ADD} Neuen Römer erstellen",
            command=self.CreateNewRoman,
            style='Primary'
        )
        self.create_button.pack(side=tk.LEFT, padx=(0, UIConstants.PADDING_SMALL))
        
        self.delete_button = self.CreateStyledButton(
            left_buttons,
            text=f"{Icons.DELETE} Löschen",
            command=self.DeleteSelectedRoman,
            style='Danger',
            state=tk.DISABLED
        )
        self.delete_button.pack(side=tk.LEFT, padx=UIConstants.PADDING_SMALL)
        
        # Rechte Button-Gruppe
        right_buttons = tk.Frame(parent, bg=AppColors.CONTENT_FRAME)
        right_buttons.pack(side=tk.RIGHT)
        
        self.export_button = self.CreateStyledButton(
            right_buttons,
            text=f"{Icons.EXPORT} Exportieren",
            command=self.ExportData,
            style='Secondary'
        )
        self.export_button.pack(side=tk.LEFT, padx=UIConstants.PADDING_SMALL)

    def CreateStyledButton(self, parent, text, command, style='Primary', **kwargs):
        """Erstellt einen modernen Button mit verschiedenen Stilen"""
        button_styles = {
            'Primary': {
                'bg': AppColors.BUTTON_PRIMARY_BG,
                'fg': AppColors.BUTTON_PRIMARY_FG,
                'activebackground': AppColors.BUTTON_PRIMARY_HOVER,
                'font': Fonts.BUTTON
            },
            'Secondary': {
                'bg': AppColors.BUTTON_SECONDARY_BG,
                'fg': AppColors.BUTTON_SECONDARY_FG,
                'activebackground': AppColors.BUTTON_SECONDARY_HOVER,
                'font': Fonts.BUTTON
            },
            'Success': {
                'bg': AppColors.BUTTON_SUCCESS_BG,
                'fg': AppColors.BUTTON_SUCCESS_FG,
                'activebackground': AppColors.BUTTON_SUCCESS_HOVER,
                'font': Fonts.BUTTON
            },
            'Danger': {
                'bg': AppColors.BUTTON_DANGER_BG,
                'fg': AppColors.BUTTON_DANGER_FG,
                'activebackground': AppColors.BUTTON_DANGER_HOVER,
                'font': Fonts.BUTTON
            }
        }
        
        style_config = button_styles.get(style, button_styles['Primary'])
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            relief=tk.RIDGE,
            bd=0,
            padx=UIConstants.PADDING_XLARGE,
            pady=8,
            cursor='hand2',
            **style_config,
            **kwargs
        )
        
        # Hover-Effekte
        def on_enter(e):
            if button['state'] != tk.DISABLED:
                button['background'] = style_config['activebackground']
        
        def on_leave(e):
            if button['state'] != tk.DISABLED:
                button['background'] = style_config['bg']
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button

    def CreateStyledNotebook(self, parent):
        """Erstellt ein modernes Notebook mit verbessertem Design"""
        # Notebook-Stil
        style = ttk.Style()
        style.configure('Modern.TNotebook', 
            background=AppColors.CONTENT_FRAME,
            borderwidth=0
        )
        style.configure('Modern.TNotebook.Tab',
            padding=[UIConstants.PADDING_XLARGE, UIConstants.PADDING_MEDIUM],
            font=Fonts.TAB
        )
        
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tabs mit Icons
        tab_config = [
            ('tab_basic', f'{Icons.PERSON} Grunddaten'),
            ('tab_marriage', f'{Icons.MARRIAGE} Ehen'),
            ('tab_children', f'{Icons.CHILD} Kinder'),
            ('tab_family', f'{Icons.FAMILY} Familie'),
            ('tab_special', f'{Icons.STAR} Besonderheiten'),
            ('tab_honors', f'{Icons.TROPHY} Ehrungen'),
            ('tab_sources', f'{Icons.BOOK} Quellen'),
            ('tab_literary_sources', f'{Icons.FILE} Literarische Quellen')
        ]
        
        for tab_name, title in tab_config:
            tab = tk.Frame(self.notebook, bg=AppColors.TAB_BG)
            self.notebook.add(tab, text=title)
            setattr(self, tab_name, tab)
        
        # Tab-Inhalte erstellen
        self.CreateTabContents()
        
        # Events
        self.notebook.bind('<<NotebookTabChanged>>', self.OnTabChanged)

    # Hilfsmethoden
    def AddPlaceholder(self, entry, placeholder_text):
        """Fügt Placeholder-Text zu einem Entry-Widget hinzu"""
        entry.insert(0, placeholder_text)
        entry['fg'] = AppColors.SEARCH_PLACEHOLDER
        
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry['fg'] = AppColors.SEARCH_FG
        
        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder_text)
                entry['fg'] = AppColors.SEARCH_PLACEHOLDER
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def LoadTableData(self):
        """Lädt Daten in die Tabelle"""
        for roman in self.__app.romans:
            self.tree.insert('', tk.END, values=(
                roman.get('Name', ''), 
                roman.get('Geburtsdatum', ''), 
                roman.get('Sterbedatum', ''), 
                roman.get('Todesursache', ''), 
                roman.get('Familie', ''),
                roman.get('Häufigkeit Heirat', ''), 
                roman.get('Anzahl Kinder', '')
            ))

    def CreateTabContents(self):
        """Erstellt die Inhalte für alle Tabs mit Scrollbar"""
        # Dictionaries für Eingabefelder
        self.basic_fields = {}
        self.marriage_fields = {}
        self.children_fields = {}
        self.family_fields = {}
        self.special_fields = {}
        self.honors_fields = {}
        self.sources_fields = {}
        self.literary_fields = {}
        
        # Für jeden Tab einen scrollbaren Bereich erstellen
        tabs = [
            (self.tab_basic, self.CreateBasicDataContent),
            (self.tab_marriage, self.CreateMarriageContent),
            (self.tab_children, self.CreateChildrenContent),
            (self.tab_family, self.CreateFamilyContent),
            (self.tab_special, self.CreateSpecialContent),
            (self.tab_honors, self.CreateHonorsContent),
            (self.tab_sources, self.CreateSourcesContent),
            (self.tab_literary_sources, self.CreateLiterarySourcesContent)
        ]
        
        for tab, content_creator in tabs:
            # Scrollbarer Bereich für jeden Tab
            self.CreateScrollableTab(tab)
            # Inhalt erstellen
            content_creator(tab.content_frame)
            self.BindMouseWheelToWidget(tab.content_frame, tab.canvas)

    def BindMouseWheelToWidget(self, widget, canvas):
        """Bindet Mausrad-Events an ein Widget und alle seine Kinder"""
        def on_mousewheel(event):
            # Finde den Tab zu diesem Canvas
            tab = None
            for t in [self.tab_basic, self.tab_marriage, self.tab_children, 
                    self.tab_family, self.tab_special, self.tab_honors, 
                    self.tab_sources, self.tab_literary_sources]:
                if hasattr(t, 'canvas') and t.canvas == canvas:
                    tab = t
                    break
            
            # Nur scrollen wenn es nötig ist
            if tab and hasattr(tab, 'scroll_enabled') and tab.scroll_enabled:
                # Windows/MacOS
                if event.delta:
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                # Linux
                else:
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")
            
            return "break"
        
        # Binde Events an das Widget
        widget.bind("<MouseWheel>", on_mousewheel)  # Windows/MacOS
        widget.bind("<Button-4>", on_mousewheel)    # Linux
        widget.bind("<Button-5>", on_mousewheel)    # Linux
        
        # Rekursiv für alle Kinder
        for child in widget.winfo_children():
            self.BindMouseWheelToWidget(child, canvas)

    def CreateMarriageContent(self, parent):
        pass

    def CreateChildrenContent(self, parent):
        pass

    def CreateFamilyContent(self, parent):
        pass

    def CreateSpecialContent(self, parent):
        pass

    def CreateHonorsContent(self, parent):
        pass

    def CreateSourcesContent(self, parent):
        pass

    def CreateLiterarySourcesContent(self, parent):
        pass

    def CreateBasicDataContent(self, parent):
        """Erstellt den Inhalt für den Grunddaten-Tab"""
        # Container mit Padding
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.PERSON} Persönliche Informationen", 
             font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
             fg=AppColors.KU_COLOR).pack(side=tk.LEFT)
        
        # Formularfelder
        fields = [
            ('Name', 'Name', 'entry'),
            ('Geburtsdatum', 'Geburtsdatum', 'entry'),
            ('Geburtsort', 'Geburtsort', 'entry'),
            ('Sterbedatum', 'Sterbedatum', 'entry'),
            ('Sterbeort', 'Sterbeort', 'entry'),
            ('Todesursache', 'Todesursache', 'entry'),
            ('Bemerkungen', 'Bemerkungen', 'text')
        ]
        
        for field_data in fields:
            field_key = field_data[0]
            field_label = field_data[1]
            field_type = field_data[2]
            
            row_frame = tk.Frame(container, bg=AppColors.TAB_BG)
            row_frame.pack(fill=tk.X, pady=8)
            
            # Label
            label = tk.Label(row_frame, text=f"{field_label}:", 
                            font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                            fg=AppColors.KU_COLOR, width=20, anchor=tk.W)
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Widget basierend auf Typ
            if field_type == 'entry':
                widget = tk.Entry(row_frame, font=Fonts.INPUT, 
                                bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                                width=40, relief=tk.RIDGE, bd=2)
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
            elif field_type == 'combo':
                widget = ttk.Combobox(row_frame, font=Fonts.INPUT, 
                                    values=field_data[3], width=38, state='readonly')
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
            elif field_type == 'text':
                text_frame = tk.Frame(container, bg=AppColors.TAB_BG)
                text_frame.pack(fill=tk.BOTH, expand=True, pady=8)
                
                widget = tk.Text(text_frame, font=Fonts.INPUT, 
                            bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                            height=4, relief=tk.RIDGE, bd=2)
                widget.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
            
            # Speichere Referenz
            self.basic_fields[field_key] = widget

    def CreateMarriageContent(self, parent):
        """Erstellt den Inhalt für den Ehen-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.MARRIAGE} Eheschließungen", 
             font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
             fg=AppColors.KU_COLOR).pack(side=tk.LEFT)
        
        # Button zum Hinzufügen
        add_button = self.CreateStyledButton(
            title_frame,
            text=f"{Icons.ADD} Ehe hinzufügen",
            command=lambda: self.AddMarriageEntry(marriages_container),
            style='Primary'
        )
        add_button.pack(side=tk.RIGHT)
        
        # Container für Ehen
        marriages_container = tk.Frame(container, bg=AppColors.TAB_BG)
        marriages_container.pack(fill=tk.BOTH, expand=True)
        
        self.marriages_container = marriages_container
        self.marriage_entries = []

    def AddMarriageEntry(self, parent):
        """Fügt einen neuen Ehe-Eintrag hinzu"""
        marriage_frame = tk.Frame(parent, bg=AppColors.TAB_BG, relief=tk.RAISED, bd=1)
        marriage_frame.pack(fill=tk.X, pady=10)
        
        inner_frame = tk.Frame(marriage_frame, bg=AppColors.TAB_BG)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header mit Nummer und Löschen-Button
        header_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text=f"Ehe #{len(self.marriage_entries) + 1}", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)
        
        delete_button = tk.Button(header_frame, text=Icons.DELETE, 
                                font=Fonts.ICON, bg=AppColors.BUTTON_DANGER_BG,
                                fg=AppColors.BUTTON_DANGER_FG, bd=0,
                                command=lambda: self.RemoveMarriageEntry(marriage_frame))
        delete_button.pack(side=tk.RIGHT)
        
        # Felder
        fields = {}
        field_configs = [
            ('Partner', 'Ehepartner'),
            ('Heiratsdatum', 'Heiratsdatum'),
            ('Heiratsort', 'Heiratsort'),
            ('Scheidungsdatum', 'Scheidungsdatum'),
        ]
        
        for field_key, field_label in field_configs:
            row = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=f"{field_label}:", font=Fonts.STANDARD,
                    bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR,
                    width=15, anchor=tk.W).pack(side=tk.LEFT)
            
            entry = tk.Entry(row, font=Fonts.INPUT, bg=AppColors.INPUT_BG,
                            fg=AppColors.INPUT_FG, width=30, relief=tk.RIDGE, bd=2)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            fields[field_key] = entry
        
        text_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=8)
                
        tk.Label(text_frame, text=f"Bemerkungen:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, anchor=tk.W).pack(anchor=tk.W)
                
        widget = tk.Text(text_frame, font=Fonts.INPUT, 
                    bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                    height=4, relief=tk.RIDGE, bd=2)
        widget.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.marriage_entries.append({'frame': marriage_frame, 'fields': fields})

        if hasattr(self.tab_marriage, 'canvas'):
            self.BindMouseWheelToWidget(marriage_frame, self.tab_marriage.canvas)

    def RemoveMarriageEntry(self, frame):
        """Entfernt einen Ehe-Eintrag"""
        # Finde und entferne aus Liste
        for i, entry in enumerate(self.marriage_entries):
            if entry['frame'] == frame:
                self.marriage_entries.pop(i)
                break
        
        # Entferne Frame
        frame.destroy()
        
        # Nummerierung aktualisieren
        self.UpdateMarriageNumbers()

    def UpdateMarriageNumbers(self):
        """Aktualisiert die Nummerierung der Ehen"""
        for i, entry in enumerate(self.marriage_entries):
            # Finde das Label im Header
            header_frame = entry['frame'].winfo_children()[0].winfo_children()[0]
            for widget in header_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=f"Ehe #{i + 1}")
                    break
    
    def CreateChildrenContent(self, parent):
        """Erstellt den Inhalt für den Kinder-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text=f"{Icons.CHILD} Kinder", 
                font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)
        
        # Statistik
        stats_frame = tk.Frame(container, bg=AppColors.HIGHLIGHT, relief=tk.RIDGE, bd=1)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_inner = tk.Frame(stats_frame, bg=AppColors.HIGHLIGHT)
        stats_inner.pack(padx=15, pady=10)
        
        self.children_count_label = tk.Label(stats_inner, 
                                        text="Anzahl Kinder: 0", 
                                        font=Fonts.STANDARD_BOLD,
                                        bg=AppColors.HIGHLIGHT, 
                                        fg=AppColors.KU_COLOR)
        self.children_count_label.pack()
        
        # Button zum Hinzufügen
        add_button = self.CreateStyledButton(
            container,
            text=f"{Icons.ADD} Kind hinzufügen",
            command=lambda: self.AddChildEntry(children_container),
            style='Primary'
        )
        add_button.pack(anchor=tk.W, pady=(0, 10))
        
        # Container für Kinder
        children_container = tk.Frame(container, bg=AppColors.TAB_BG)
        children_container.pack(fill=tk.BOTH, expand=True)
        
        self.children_container = children_container
        self.children_entries = []

    def AddChildEntry(self, parent):
        """Fügt einen neuen Kind-Eintrag hinzu"""
        child_frame = tk.Frame(parent, bg=AppColors.TAB_BG, relief=tk.RAISED, bd=1)
        child_frame.pack(fill=tk.X, pady=5)
        
        inner_frame = tk.Frame(child_frame, bg=AppColors.TAB_BG)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Container für die erste Zeile (Name, Geschlecht, Geburtsjahr, Löschen)
        first_row = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        first_row.pack(fill=tk.X)
        
        # Felder
        fields = {}
        
        # Name
        tk.Label(first_row, text="Name:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        
        name_entry = tk.Entry(first_row, font=Fonts.INPUT, bg=AppColors.INPUT_BG,
                            fg=AppColors.INPUT_FG, width=25, relief=tk.RIDGE, bd=2)
        name_entry.pack(side=tk.LEFT, padx=(0, 15))
        fields['Name'] = name_entry
        
        # Geschlecht
        tk.Label(first_row, text="Geschlecht:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        
        gender_combo = ttk.Combobox(first_row, font=Fonts.INPUT,
                                values=['Männlich', 'Weiblich', 'Unbekannt'],
                                width=12, state='readonly')
        gender_combo.pack(side=tk.LEFT, padx=(0, 15))
        fields['Geschlecht'] = gender_combo
        
        # Geburtsjahr
        tk.Label(first_row, text="Geburtsjahr:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        
        birth_entry = tk.Entry(first_row, font=Fonts.INPUT, bg=AppColors.INPUT_BG,
                            fg=AppColors.INPUT_FG, width=25, relief=tk.RIDGE, bd=2)
        birth_entry.pack(side=tk.LEFT, padx=(0, 15))
        fields['Geburtsjahr'] = birth_entry
        
        # Löschen-Button
        delete_button = tk.Button(first_row, text=Icons.DELETE,
                                font=Fonts.ICON, bg=AppColors.BUTTON_DANGER_BG,
                                fg=AppColors.BUTTON_DANGER_FG, bd=0,
                                command=lambda: self.RemoveChildEntry(child_frame))
        delete_button.pack(side=tk.RIGHT)
        
        # Container für die zweite Zeile (Bemerkung)
        second_row = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        second_row.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Bemerkung
        tk.Label(second_row, text="Bemerkung:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR).pack(anchor=tk.W, padx=(0, 5))
        
        note = tk.Text(second_row, font=Fonts.INPUT, 
                    bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                    height=3, relief=tk.RIDGE, bd=2)
        note.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        fields['Bemerkungen'] = note
        
        self.children_entries.append({'frame': child_frame, 'fields': fields})
        self.UpdateChildrenCount()

        if hasattr(self.tab_children, 'canvas'):
            self.BindMouseWheelToWidget(child_frame, self.tab_children.canvas)

    def RemoveChildEntry(self, frame):
        """Entfernt einen Kind-Eintrag"""
        for i, entry in enumerate(self.children_entries):
            if entry['frame'] == frame:
                self.children_entries.pop(i)
                break
        
        frame.destroy()
        self.UpdateChildrenCount()

    def UpdateChildrenCount(self):
        """Aktualisiert die Anzahl der Kinder"""
        count = len(self.children_entries)
        self.children_count_label.config(text=f"Anzahl Kinder: {count}")

    def CreateScrollableTab(self, tab):
        """Erstellt einen scrollbaren Bereich innerhalb eines Tabs"""
        # Container für Canvas und Scrollbar
        scroll_container = tk.Frame(tab, bg=AppColors.TAB_BG)
        scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas
        canvas = tk.Canvas(scroll_container, bg=AppColors.TAB_BG, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(scroll_container, orient=tk.VERTICAL, command=canvas.yview)
        
        # Canvas mit Scrollbar verbinden
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame für den Inhalt
        content_frame = tk.Frame(canvas, bg=AppColors.TAB_BG)
        canvas_window = canvas.create_window(0, 0, anchor=tk.NW, window=content_frame)
        
        # Funktion zum Prüfen ob Scrolling nötig ist
        def check_scroll_needed():
            canvas.update_idletasks()
            content_height = content_frame.winfo_reqheight()
            canvas_height = canvas.winfo_height()
            
            if content_height > canvas_height:
                # Scrollbar anzeigen
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                return True
            else:
                # Scrollbar verstecken
                scrollbar.pack_forget()
                return False
        
        # Events für Canvas-Größenanpassung
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Prüfe ob Scrollbar benötigt wird
            tab.scroll_enabled = check_scroll_needed()
        
        def configure_canvas_width(event=None):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            # Prüfe ob Scrollbar benötigt wird
            tab.scroll_enabled = check_scroll_needed()
        
        content_frame.bind('<Configure>', configure_scroll_region)
        canvas.bind('<Configure>', configure_canvas_width)
        
        # Speichere Referenzen
        tab.canvas = canvas
        tab.scrollbar = scrollbar
        tab.content_frame = content_frame
        tab.scroll_enabled = False  # Initial kein Scrolling

    def UpdateButtonStates(self):
        """Aktualisiert die Button-Zustände"""
        pass

    def FilterTable(self, event=None):
        """Filtert die Tabelle basierend auf der Sucheingabe"""
        search_term = self.search_var.get().lower()
        
        # Placeholder-Text ignorieren
        if search_term == Messages.SEARCH_PLACEHOLDER.lower():
            return
        
        # Alle Items löschen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Gefilterte Items wieder einfügen
        for roman in self.__app.romans:
            values = [
                str(roman.get('Name', '')),
                str(roman.get('Geburtsdatum', '')),
                str(roman.get('Sterbedatum', '')),
                str(roman.get('Todesursache', '')),
                str(roman.get('Familie', '')),
                str(roman.get('Häufigkeit Heirat', '')),
                str(roman.get('Anzahl Kinder', ''))
            ]
                
            if any(search_term in value.lower() for value in values):
                self.tree.insert('', tk.END, values=values)

    def OnSelect(self, event=None):
        """Wird aufgerufen, wenn ein Item in der Tabelle ausgewählt wird"""
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

            self.delete_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"{Icons.INFO} {self.__current_roman['Name']} ausgewählt")
        else:
            self.__current_roman = None
            self.ClearDetails()

            self.delete_button.config(state=tk.DISABLED)
            self.status_label.config(text=Messages.NO_SELECTION)

    def OnDoubleClick(self, event=None):
        """Wird bei Doppelklick auf ein Tabellen-Item aufgerufen"""
        selection = self.tree.selection()
        if selection:
            # Zum ersten Tab wechseln
            self.notebook.select(0)

    def OnTabChanged(self, event=None):
        """Wird aufgerufen, wenn ein Tab gewechselt wird"""
        if hasattr(self.__class__, 'last_selected_tab'):
            self.__class__.last_selected_tab = self.notebook.index(self.notebook.select())

    def SortColumn(self, col):
        """Sortiert die Tabelle alphabetisch nach der angeklickten Spalte"""
        # Alle aktuellen Daten aus der Tabelle holen
        data = []
        for child in self.tree.get_children():
            data.append((child, self.tree.item(child)['values']))
        
        # Bestimme Sortierrichtung
        if self.sort_column == col:
            # Gleiche Spalte wieder geklickt - Richtung umkehren
            self.sort_reverse = not self.sort_reverse
        else:
            # Neue Spalte - aufsteigend sortieren
            self.sort_column = col
            self.sort_reverse = False
        
        # Spaltenindex finden
        col_index = self.tree['columns'].index(col)
        
        # Alphabetisch sortieren
        def sort_key(item):
            value = item[1][col_index]
            # Konvertiere zu String und lowercase für case-insensitive Sortierung
            return str(value).lower() if value else ''
        
        # Sortiere die Daten
        data.sort(key=sort_key, reverse=self.sort_reverse)
        
        # Tabelle neu aufbauen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for item_id, values in data:
            self.tree.insert('', tk.END, values=values)
        
        # Visuelles Feedback für Sortierung
        self.UpdateColumnHeaders(col)

    def UpdateColumnHeaders(self, sorted_col):
        """Aktualisiert die Spaltenüberschriften mit Sortier-Indikatoren"""
        # Sortier-Symbole
        arrow_up = ' ▲'
        arrow_down = ' ▼'
        
        for col in self.tree['columns']:
            # Aktuellen Text ohne Pfeile holen
            current_text = self.tree.heading(col)['text']
            clean_text = current_text.replace(arrow_up, '').replace(arrow_down, '')
            
            # Neuen Text mit Pfeil setzen, wenn dies die sortierte Spalte ist
            if col == sorted_col:
                if self.sort_reverse:
                    new_text = clean_text + arrow_down
                else:
                    new_text = clean_text + arrow_up
            else:
                new_text = clean_text
            
            # Heading aktualisieren
            self.tree.heading(col, text=new_text)

    def CreateNewRoman(self):
        """Erstellt einen neuen Römer"""
        print(f"{Icons.ADD} Neuen Römer erstellen...")

    def DeleteSelectedRoman(self):
        """Löscht den ausgewählten Römer"""
        print(f"{Icons.DELETE} Römer löschen...")

    def SaveChanges(self):
        """Speichert die Änderungen"""
        print(f"{Icons.SAVE} {Messages.SAVE_SUCCESS}")

    def ExportData(self):
        """Exportiert die Daten"""
        print(f"{Icons.EXPORT} Daten exportieren...")

    def ClearDetails(self):
        """Leert alle Detailfelder"""
        pass

    def DisplayRoman(self):
        pass