import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
import webbrowser

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.commands import AddRomanCommand, EditRomanCommand, RemoveRomanCommand
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
        
        # Tabellen-Container
        table_container = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        table_container.pack(fill=tk.BOTH, expand=True, padx=UIConstants.PADDING_LARGE, pady=(UIConstants.PADDING_MEDIUM, UIConstants.PADDING_SMALL))
        
        # Tabelle mit modernem Stil
        self.CreateStyledTable(table_container)
        
        # Button-Bereich
        # button_container = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        # button_container.pack(fill=tk.X, padx=UIConstants.PADDING_LARGE, pady=(UIConstants.PADDING_SMALL, UIConstants.PADDING_LARGE))
        
        # self.CreateActionButtons(button_container)
        
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

        self.create_button = self.CreateStyledButton(
            save_container,
            text=f"{Icons.ADD} Neuen Römer erstellen",
            command=self.CreateNewRoman,
            style='Primary'
        )
        self.create_button.pack(side=tk.LEFT)

        self.delete_button = self.CreateStyledButton(
            save_container,
            text=f"{Icons.DELETE} Löschen",
            command=self.DeleteSelectedRoman,
            style='Danger',
            state=tk.DISABLED
        )
        self.delete_button.pack(side=tk.LEFT)

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
        self.DisableFields()

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

    def LoadTableData(self):
        """Lädt Daten in die Tabelle"""

        # Alle aktuellen Einträge entfernen
        for item in self.tree.get_children():
            self.tree.delete(item)

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

    def CreateFamilyContent(self, parent):
        """Erstellt den Inhalt für den Family-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.FAMILY} Familieninformationen", 
                font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Formularfelder
        fields = [
            ('Vater', 'Vater', 'entry'),
            ('Mutter', 'Mutter', 'entry'),
            ('Geschwister', 'Geschwister', 'entry'),
            ('Vorfahren', 'Vorfahren', 'entry'),
            ('Bemerkungen', 'Bemerkungen', 'text')
        ]

        self.family_fields = {}
        for field_key, field_label, field_type in fields:
            widget = self.CreateFormField(container, field_key, field_label, field_type)
            self.family_fields[field_key] = widget
    
    def CreateFormField(self, parent, field_key, field_label, field_type, values=None):
        row_frame = tk.Frame(parent, bg=AppColors.TAB_BG)
        row_frame.pack(fill=tk.X, pady=8)

        label = tk.Label(row_frame, text=f"{field_label}:", 
                        font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                        fg=AppColors.KU_COLOR, width=20, anchor=tk.W)
        label.pack(side=tk.LEFT, padx=(0, 10))

        if field_type == 'entry':
            widget = tk.Entry(row_frame, font=Fonts.INPUT, 
                            bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                            width=40, relief=tk.RIDGE, bd=2)
            widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

        elif field_type == 'combo':
            widget = ttk.Combobox(row_frame, font=Fonts.INPUT, 
                                values=values, width=38, state='readonly')
            widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

        elif field_type == 'text':
            text_frame = tk.Frame(parent, bg=AppColors.TAB_BG)
            text_frame.pack(fill=tk.BOTH, expand=True, pady=8)
                
            widget = tk.Text(text_frame, font=Fonts.INPUT, 
                            bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                            height=4, relief=tk.RIDGE, bd=2)
            widget.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        return widget

    def CreateSpecialContent(self, parent):
        """Erstellt den Inhalt für den Besonderheiten-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.STAR} Individuelle Besonderheiten", 
                font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Hauptcontainer für alle Sektionen
        main_container = tk.Frame(container, bg=AppColors.TAB_BG)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ========== Äußere Erscheinung ==========
        appearance_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        appearance_section.pack(fill=tk.X, pady=(0, 15))

        appearance_inner = tk.Frame(appearance_section, bg=AppColors.TAB_BG)
        appearance_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Sektion-Titel
        tk.Label(appearance_inner, text="Äußere Erscheinung", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Auftreten
        auftreten_frame = tk.Frame(appearance_inner, bg=AppColors.TAB_BG)
        auftreten_frame.pack(fill=tk.X, pady=5)

        tk.Label(auftreten_frame, text="Auftreten:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.W).pack(side=tk.LEFT)

        self.special_fields['Auftreten'] = tk.Entry(auftreten_frame, font=Fonts.INPUT, 
                                                    bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                                                    width=40, relief=tk.RIDGE, bd=2)
        self.special_fields['Auftreten'].pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Kleidung
        kleidung_frame = tk.Frame(appearance_inner, bg=AppColors.TAB_BG)
        kleidung_frame.pack(fill=tk.X, pady=5)

        tk.Label(kleidung_frame, text="Kleidung:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.W).pack(side=tk.LEFT)

        self.special_fields['Kleidung'] = tk.Entry(kleidung_frame, font=Fonts.INPUT, 
                                                bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                                                width=40, relief=tk.RIDGE, bd=2)
        self.special_fields['Kleidung'].pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Schmuck
        schmuck_frame = tk.Frame(appearance_inner, bg=AppColors.TAB_BG)
        schmuck_frame.pack(fill=tk.X, pady=5)

        tk.Label(schmuck_frame, text="Schmuck:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.W).pack(side=tk.LEFT)

        self.special_fields['Schmuck'] = tk.Entry(schmuck_frame, font=Fonts.INPUT, 
                                                bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                                                width=40, relief=tk.RIDGE, bd=2)
        self.special_fields['Schmuck'].pack(side=tk.LEFT, fill=tk.X, expand=True)

        # ========== Inszenierung ==========
        staging_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        staging_section.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        staging_inner = tk.Frame(staging_section, bg=AppColors.TAB_BG)
        staging_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Sektion-Titel
        tk.Label(staging_inner, text="Inszenierung", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Öffentlich
        public_frame = tk.Frame(staging_inner, bg=AppColors.TAB_BG)
        public_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(public_frame, text="Öffentlich:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.NW).pack(side=tk.LEFT, pady=(5, 0))

        text_container = tk.Frame(public_frame, bg=AppColors.TAB_BG)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.special_fields['Öffentlich'] = tk.Text(text_container, font=Fonts.INPUT, 
                                                bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                                                height=4, relief=tk.RIDGE, bd=2, wrap=tk.WORD)
        self.special_fields['Öffentlich'].pack(fill=tk.BOTH, expand=True)

        # Privat
        private_frame = tk.Frame(staging_inner, bg=AppColors.TAB_BG)
        private_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(private_frame, text="Privat:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.NW).pack(side=tk.LEFT, pady=(5, 0))

        text_container = tk.Frame(private_frame, bg=AppColors.TAB_BG)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.special_fields['Privat'] = tk.Text(text_container, font=Fonts.INPUT, 
                                            bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                                            height=4, relief=tk.RIDGE, bd=2, wrap=tk.WORD)
        self.special_fields['Privat'].pack(fill=tk.BOTH, expand=True)

        # ========== Zusätzliche Bemerkungen ==========
        remarks_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        remarks_section.pack(fill=tk.BOTH, expand=True)

        remarks_inner = tk.Frame(remarks_section, bg=AppColors.TAB_BG)
        remarks_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Sektion-Titel
        tk.Label(remarks_inner, text="Zusätzliche Bemerkungen", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Bemerkungen Text
        self.special_fields['Bemerkungen'] = tk.Text(remarks_inner, font=Fonts.INPUT, 
                                                    bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                                                    height=5, relief=tk.RIDGE, bd=2, wrap=tk.WORD)
        self.special_fields['Bemerkungen'].pack(fill=tk.BOTH, expand=True)

    def CreateHonorsContent(self, parent):
        """Erstellt den Inhalt für den Ehrungen-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.TROPHY} Ehrungen und Titel", 
                font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Hauptcontainer für alle Ehrungen
        main_container = tk.Frame(container, bg=AppColors.TAB_BG)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ========== Augusta-Titel ==========
        augusta_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        augusta_section.pack(fill=tk.X, pady=(0, 15))

        augusta_inner = tk.Frame(augusta_section, bg=AppColors.TAB_BG)
        augusta_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion
        tk.Label(augusta_inner, text="Augusta-Titel", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Combobox-Zeile
        augusta_combo_frame = tk.Frame(augusta_inner, bg=AppColors.TAB_BG)
        augusta_combo_frame.pack(fill=tk.X, pady=5)

        tk.Label(augusta_combo_frame, text="Status:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.W).pack(side=tk.LEFT)

        self.honors_fields['Augusta-Titel-Status'] = ttk.Combobox(
            augusta_combo_frame, 
            font=Fonts.INPUT,
            values=['Ja', 'Nein', 'Unbekannt', 'In Bearbeitung'],
            width=20,
            state='readonly'
        )
        self.honors_fields['Augusta-Titel-Status'].pack(side=tk.LEFT, padx=(0, 10))
        self.honors_fields['Augusta-Titel-Status'].set('Unbekannt')

        # Textfeld für Details
        augusta_text_frame = tk.Frame(augusta_inner, bg=AppColors.TAB_BG)
        augusta_text_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(augusta_text_frame, text="Details:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.NW).pack(side=tk.LEFT, pady=(5, 0))

        text_container = tk.Frame(augusta_text_frame, bg=AppColors.TAB_BG)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.honors_fields['Augusta-Titel-Details'] = tk.Text(
            text_container, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=3, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.honors_fields['Augusta-Titel-Details'].pack(fill=tk.BOTH, expand=True)

        # ========== Carpentum-Recht ==========
        carpentum_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        carpentum_section.pack(fill=tk.X, pady=(0, 15))

        carpentum_inner = tk.Frame(carpentum_section, bg=AppColors.TAB_BG)
        carpentum_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion
        tk.Label(carpentum_inner, text="Carpentum-Recht", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Combobox-Zeile
        carpentum_combo_frame = tk.Frame(carpentum_inner, bg=AppColors.TAB_BG)
        carpentum_combo_frame.pack(fill=tk.X, pady=5)

        tk.Label(carpentum_combo_frame, text="Status:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.W).pack(side=tk.LEFT)

        self.honors_fields['Carpentum-Recht-Status'] = ttk.Combobox(
            carpentum_combo_frame, 
            font=Fonts.INPUT,
            values=['Ja', 'Nein', 'Unbekannt', 'In Bearbeitung'],
            width=20,
            state='readonly'
        )
        self.honors_fields['Carpentum-Recht-Status'].pack(side=tk.LEFT, padx=(0, 10))
        self.honors_fields['Carpentum-Recht-Status'].set('Unbekannt')

        # Textfeld für Details
        carpentum_text_frame = tk.Frame(carpentum_inner, bg=AppColors.TAB_BG)
        carpentum_text_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(carpentum_text_frame, text="Details:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=15, anchor=tk.NW).pack(side=tk.LEFT, pady=(5, 0))

        text_container = tk.Frame(carpentum_text_frame, bg=AppColors.TAB_BG)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.honors_fields['Carpentum-Recht-Details'] = tk.Text(
            text_container, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=3, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.honors_fields['Carpentum-Recht-Details'].pack(fill=tk.BOTH, expand=True)


        # ========== Weitere Ehrungen ==========
        weitere_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        weitere_section.pack(fill=tk.BOTH, expand=True)

        weitere_inner = tk.Frame(weitere_section, bg=AppColors.TAB_BG)
        weitere_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion
        weitere_title_frame = tk.Frame(weitere_inner, bg=AppColors.TAB_BG)
        weitere_title_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(weitere_title_frame, text="Weitere Ehrungen", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Info-Label
        info_label = tk.Label(weitere_title_frame, 
                            text="(Chronologisch auflisten)", 
                            font=Fonts.STANDARD_ITALIC, 
                            bg=AppColors.TAB_BG, 
                            fg=AppColors.STATUS_FG)
        info_label.pack(side=tk.LEFT, padx=(10, 0))

        # Großes Textfeld für weitere Ehrungen
        self.honors_fields['Weitere'] = tk.Text(
            weitere_inner, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=8, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.honors_fields['Weitere'].pack(fill=tk.BOTH, expand=True)

        # ========== Hinweis-Box ==========
        hint_frame = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        hint_frame.pack(fill=tk.X, pady=(15, 0))

        hint_inner = tk.Frame(hint_frame, bg=AppColors.TAB_BG)
        hint_inner.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(hint_inner, 
                text=f"{Icons.INFO} Hinweis:", 
                font=Fonts.STANDARD_BOLD, 
                bg=AppColors.TAB_BG, 
                fg=AppColors.TAB_FG).pack(side=tk.LEFT)

        tk.Label(hint_inner, 
                text="Bitte geben Sie Daten und Ehrungen chronologisch an. Nutzen Sie das Format: 'Jahr: Ehrung/Titel'", 
                font=Fonts.STANDARD, 
                bg=AppColors.TAB_BG, 
                fg=AppColors.TAB_FG,
                wraplength=600).pack(side=tk.LEFT, padx=(5, 0))

    def CreateSourcesContent(self, parent):
        """Erstellt den Inhalt für den Quellen-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.BOOK} Historische Quellen", 
                font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Hauptcontainer für alle Quellen
        main_container = tk.Frame(container, bg=AppColors.TAB_BG)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ========== Divinisierung ==========
        divin_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        divin_section.pack(fill=tk.X, pady=(0, 15))

        divin_inner = tk.Frame(divin_section, bg=AppColors.TAB_BG)
        divin_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion
        tk.Label(divin_inner, text="Divinisierung (Vergöttlichung)", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Textfeld für Divinisierung
        self.sources_fields['Divinisierung'] = tk.Text(
            divin_inner, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=3, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.sources_fields['Divinisierung'].pack(fill=tk.BOTH, expand=True)

        # ========== Bestattung ==========
        bestattung_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        bestattung_section.pack(fill=tk.X, pady=(0, 15))

        bestattung_inner = tk.Frame(bestattung_section, bg=AppColors.TAB_BG)
        bestattung_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion
        tk.Label(bestattung_inner, text="Bestattung", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(anchor=tk.W, pady=(0, 10))

        # Textfeld für Bestattung
        self.sources_fields['Bestattung'] = tk.Text(
            bestattung_inner, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=3, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.sources_fields['Bestattung'].pack(fill=tk.BOTH, expand=True)

        # ========== Archäologische Quellen ==========
        arch_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        arch_section.pack(fill=tk.X, pady=(0, 15))

        arch_inner = tk.Frame(arch_section, bg=AppColors.TAB_BG)
        arch_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion mit Icon
        arch_title_frame = tk.Frame(arch_inner, bg=AppColors.TAB_BG)
        arch_title_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(arch_title_frame, text="🏛️ Archäologische Quellen", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Textfeld für Archäologische Quellen
        self.sources_fields['Archäologische Quellen'] = tk.Text(
            arch_inner, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=4, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.sources_fields['Archäologische Quellen'].pack(fill=tk.BOTH, expand=True)

        # ========== Münzen ==========
        coins_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        coins_section.pack(fill=tk.X, pady=(0, 15))

        coins_inner = tk.Frame(coins_section, bg=AppColors.TAB_BG)
        coins_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion mit Icon
        coins_title_frame = tk.Frame(coins_inner, bg=AppColors.TAB_BG)
        coins_title_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(coins_title_frame, text="🪙 Münzen", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Info-Label
        info_label = tk.Label(coins_title_frame, 
                            text="(Prägeort, Datierung, Beschreibung)", 
                            font=Fonts.STANDARD_ITALIC, 
                            bg=AppColors.TAB_BG, 
                            fg=AppColors.STATUS_FG)
        info_label.pack(side=tk.LEFT, padx=(10, 0))

        # Textfeld für Münzen
        self.sources_fields['Münzen'] = tk.Text(
            coins_inner, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=4, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.sources_fields['Münzen'].pack(fill=tk.BOTH, expand=True)

        # ========== Inschriften ==========
        inscr_section = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        inscr_section.pack(fill=tk.BOTH, expand=True)

        inscr_inner = tk.Frame(inscr_section, bg=AppColors.TAB_BG)
        inscr_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Titel der Sektion mit Icon
        inscr_title_frame = tk.Frame(inscr_inner, bg=AppColors.TAB_BG)
        inscr_title_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(inscr_title_frame, text="📜 Inschriften", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Info-Label
        info_label = tk.Label(inscr_title_frame, 
                            text="(Fundort, Datierung, Text)", 
                            font=Fonts.STANDARD_ITALIC, 
                            bg=AppColors.TAB_BG, 
                            fg=AppColors.STATUS_FG)
        info_label.pack(side=tk.LEFT, padx=(10, 0))

        # Textfeld für Inschriften
        self.sources_fields['Inschriften'] = tk.Text(
            inscr_inner, 
            font=Fonts.INPUT, 
            bg=AppColors.INPUT_BG, 
            fg=AppColors.INPUT_FG,
            height=5, 
            relief=tk.RIDGE, 
            bd=2, 
            wrap=tk.WORD
        )
        self.sources_fields['Inschriften'].pack(fill=tk.BOTH, expand=True)

        # ========== Hinweis-Box ==========
        hint_frame = tk.Frame(main_container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        hint_frame.pack(fill=tk.X, pady=(15, 0))

        hint_inner = tk.Frame(hint_frame, bg=AppColors.TAB_BG)
        hint_inner.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(hint_inner, 
                text=f"{Icons.INFO} Tipp:", 
                font=Fonts.STANDARD_BOLD, 
                bg=AppColors.TAB_BG, 
                fg=AppColors.TAB_FG).pack(side=tk.LEFT)

        tk.Label(hint_inner, 
                text="Geben Sie bei Münzen und Inschriften möglichst genaue Referenzen an (z.B. RIC-Nummern, CIL-Nummern)", 
                font=Fonts.STANDARD, 
                bg=AppColors.TAB_BG, 
                fg=AppColors.TAB_FG,
                wraplength=600).pack(side=tk.LEFT, padx=(5, 0))

    def CreateLiterarySourcesContent(self, parent):
        """Erstellt den Inhalt für den Literarische Quellen-Tab"""
        container = tk.Frame(parent, bg=AppColors.TAB_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        title_frame = tk.Frame(container, bg=AppColors.TAB_BG)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text=f"{Icons.FILE} Literarische Quellen", 
                font=Fonts.HEADER_MEDIUM, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)

        # Button zum Hinzufügen
        self.literary_add_button = self.CreateStyledButton(
            title_frame,
            text=f"{Icons.ADD} Quelle hinzufügen",
            command=lambda: self.AddLiterarySourceEntry(sources_container),
            style='Primary'
        )
        self.literary_add_button.pack(side=tk.RIGHT)

        # Info-Text
        info_frame = tk.Frame(container, bg=AppColors.TAB_BG, relief=tk.RIDGE, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))

        info_inner = tk.Frame(info_frame, bg=AppColors.TAB_BG)
        info_inner.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(info_inner, 
                text=f"{Icons.INFO} Hinweis:", 
                font=Fonts.STANDARD_BOLD, 
                bg=AppColors.TAB_BG, 
                fg=AppColors.TAB_FG).pack(side=tk.LEFT)

        tk.Label(info_inner, 
                text="Fügen Sie hier Verweise auf literarische Quellen, wissenschaftliche Publikationen und Online-Ressourcen hinzu.", 
                font=Fonts.STANDARD, 
                bg=AppColors.TAB_BG, 
                fg=AppColors.TAB_FG,
                wraplength=600).pack(side=tk.LEFT, padx=(5, 0))

        # Container für Quellen-Einträge
        sources_container = tk.Frame(container, bg=AppColors.TAB_BG)
        sources_container.pack(fill=tk.BOTH, expand=True)

        self.literary_sources_container = sources_container
        self.literary_sources_entries = []

    def AddLiterarySourceEntry(self, parent, example=False):
        """Fügt einen neuen Literarische-Quelle-Eintrag hinzu"""
        source_frame = tk.Frame(parent, bg=AppColors.TAB_BG, relief=tk.RAISED, bd=1)
        source_frame.pack(fill=tk.X, pady=10)
        
        inner_frame = tk.Frame(source_frame, bg=AppColors.TAB_BG)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header mit Nummer und Löschen-Button
        header_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text=f"📚 Quelle #{len(self.literary_sources_entries) + 1}", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)
        
        delete_button = tk.Button(header_frame, text=Icons.DELETE, 
                                font=Fonts.ICON, bg=AppColors.BUTTON_DANGER_BG,
                                fg=AppColors.BUTTON_DANGER_FG, bd=0,
                                command=lambda: self.RemoveLiterarySourceEntry(source_frame),
                                cursor='hand2')
        delete_button.pack(side=tk.RIGHT)
        
        # Felder Container
        fields = {}
        
        # Autor/Titel Zeile
        author_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        author_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(author_frame, text="Autor/Titel:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR,
                width=12, anchor=tk.W).pack(side=tk.LEFT)
        
        author_entry = tk.Entry(author_frame, font=Fonts.INPUT, bg=AppColors.INPUT_BG,
                            fg=AppColors.INPUT_FG, relief=tk.RIDGE, bd=2)
        author_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        fields['Autor'] = author_entry
        
        # Link Zeile
        link_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        link_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(link_frame, text="🔗 Link/URL:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR,
                width=12, anchor=tk.W).pack(side=tk.LEFT)
        
        link_entry = tk.Entry(link_frame, font=Fonts.INPUT, bg=AppColors.INPUT_BG,
                            fg=AppColors.INPUT_FG, relief=tk.RIDGE, bd=2)
        link_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        fields['Link'] = link_entry
        
        # Button zum Öffnen des Links
        open_link_button = tk.Button(link_frame, text="🌐 Öffnen",
                                font=Fonts.BUTTON_SMALL, bg=AppColors.BUTTON_SECONDARY_BG,
                                fg=AppColors.BUTTON_SECONDARY_FG, bd=0,
                                command=lambda: self.OpenLink(link_entry.get()),
                                cursor='hand2', padx=10)
        open_link_button.pack(side=tk.LEFT)
        
        # Zitat/Auszug Zeile
        quote_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        quote_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(quote_frame, text="Zitat/Auszug:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR,
                anchor=tk.NW).pack(anchor=tk.W)
        
        quote_text = tk.Text(quote_frame, font=Fonts.INPUT, 
                        bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                        height=3, relief=tk.RIDGE, bd=2, wrap=tk.WORD)
        quote_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        fields['Zitat'] = quote_text
        
        # Notizen Zeile
        notes_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(notes_frame, text="Notizen:", font=Fonts.STANDARD,
                bg=AppColors.TAB_BG, fg=AppColors.KU_COLOR,
                anchor=tk.NW).pack(anchor=tk.W)
        
        notes_text = tk.Text(notes_frame, font=Fonts.INPUT, 
                        bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG,
                        height=2, relief=tk.RIDGE, bd=2, wrap=tk.WORD)
        notes_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        fields['Notizen'] = notes_text
            
        self.literary_sources_entries.append({'frame': source_frame, 'fields': fields})
        
        # Scrollbar-Bindung hinzufügen
        if hasattr(self.tab_literary_sources, 'canvas'):
            self.BindMouseWheelToWidget(source_frame, self.tab_literary_sources.canvas)

    def RemoveLiterarySourceEntry(self, frame):
        """Entfernt einen Literarische-Quelle-Eintrag"""
        # Finde und entferne aus Liste
        for i, entry in enumerate(self.literary_sources_entries):
            if entry['frame'] == frame:
                self.literary_sources_entries.pop(i)
                break
        
        # Entferne Frame
        frame.destroy()
        
        # Nummerierung aktualisieren
        self.UpdateLiterarySourceNumbers()

    def UpdateLiterarySourceNumbers(self):
        """Aktualisiert die Nummerierung der literarischen Quellen"""
        for i, entry in enumerate(self.literary_sources_entries):
            # Finde das Label im Header
            header_frame = entry['frame'].winfo_children()[0].winfo_children()[0]
            for widget in header_frame.winfo_children():
                if isinstance(widget, tk.Label) and "Quelle #" in widget.cget("text"):
                    widget.config(text=f"📚 Quelle #{i + 1}")
                    break

    def OpenLink(self, url):
        """Öffnet einen Link im Browser"""
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        if url and url != "https://":
            try:
                webbrowser.open(url)
            except:
                messagebox.showerror("Fehler", "Der Link konnte nicht geöffnet werden.")
        else:
            messagebox.showwarning("Hinweis", "Bitte geben Sie einen gültigen Link ein.")

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
        
        for field_key, field_label, field_type in fields:
            widget = self.CreateFormField(container, field_key, field_label, field_type)
            self.basic_fields[field_key] = widget

            # Validierung für das Name-Feld
            if field_key == 'Name':
                widget.bind('<KeyRelease>', self.ValidateNameField)
                widget.bind('<FocusOut>', self.ValidateNameField)
    
    def ValidateNameField(self, event=None):
        """Validiert das Name-Feld und ändert die Hintergrundfarbe"""
        name_widget = self.basic_fields.get('Name')
        if name_widget:
            name_value = name_widget.get().strip()
            if not name_value:
                # Roter Hintergrund für leeres Feld
                name_widget.config(bg='#ffcccc')
            else:
                # Normale Hintergrundfarbe
                name_widget.config(bg=AppColors.INPUT_BG)

    def ValidateForm(self):
        """Validiert das gesamte Formular"""
        # Prüfe ob Name ausgefüllt ist
        name_widget = self.basic_fields.get('Name')
        if name_widget:
            name_value = name_widget.get().strip()
            if not name_value:
                # Markiere das Feld rot
                name_widget.config(bg='#ffcccc')
                # Zeige Fehlermeldung
                messagebox.showerror(
                    "Pflichtfeld fehlt", 
                    "Bitte geben Sie einen Namen ein. Dies ist ein Pflichtfeld."
                )
                # Wechsle zum Grunddaten-Tab
                self.notebook.select(0)
                # Setze Fokus auf das Name-Feld
                name_widget.focus_set()
                return False
        return True

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
        self.marriage_add_button = self.CreateStyledButton(
            title_frame,
            text=f"{Icons.ADD} Ehe hinzufügen",
            command=lambda: self.AddMarriageEntry(marriages_container),
            style='Primary'
        )
        self.marriage_add_button.pack(side=tk.RIGHT)

        basic_container = tk.Frame(container, bg=AppColors.TAB_BG)
        basic_container.pack(fill=tk.BOTH, expand=tk.TRUE)

        tk.Label(basic_container, text=f"Anzahl Ehen:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=20, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 10))
        
        self.marriage_widget = tk.Entry(basic_container, font=Fonts.INPUT, 
                                bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                                width=40, relief=tk.RIDGE, bd=2)
        self.marriage_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
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
                                command=lambda: self.RemoveMarriageEntry(marriage_frame),
                                cursor='hand2')
        delete_button.pack(side=tk.RIGHT)
        
        # Felder
        fields = {}
        field_configs = [
            ('Partner', 'Ehepartner'),
            ('Heiratsdatum', 'Heiratsdatum'),
            ('Heiratsort', 'Heiratsort'),
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

        fields['Bemerkungen'] = widget
        
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
        
        # Button zum Hinzufügen
        self.children_add_button = self.CreateStyledButton(
            title_frame,
            text=f"{Icons.ADD} Kind hinzufügen",
            command=lambda: self.AddChildEntry(children_container),
            style='Primary'
        )
        self.children_add_button.pack(side=tk.RIGHT)

        basic_container = tk.Frame(container, bg=AppColors.TAB_BG)
        basic_container.pack(fill=tk.BOTH, expand=tk.TRUE)

        tk.Label(basic_container, text=f"Anzahl Kinder:", 
                font=Fonts.STANDARD, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR, width=20, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 10))
        
        self.children_widget = tk.Entry(basic_container, font=Fonts.INPUT, 
                                bg=AppColors.INPUT_BG, fg=AppColors.INPUT_FG, 
                                width=40, relief=tk.RIDGE, bd=2)
        self.children_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Container für Kinder
        children_container = tk.Frame(container, bg=AppColors.TAB_BG)
        children_container.pack(fill=tk.BOTH, expand=True)
        
        self.children_container = children_container
        self.children_entries = []

    def AddChildEntry(self, parent):
        """Fügt einen neuen Kind-Eintrag hinzu"""
        child_frame = tk.Frame(parent, bg=AppColors.TAB_BG, relief=tk.RAISED, bd=1)
        child_frame.pack(fill=tk.X, pady=10)
        
        inner_frame = tk.Frame(child_frame, bg=AppColors.TAB_BG)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        header_frame = tk.Frame(inner_frame, bg=AppColors.TAB_BG)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(header_frame, text=f"Kind #{len(self.children_entries) + 1}", 
                font=Fonts.SUBHEADER, bg=AppColors.TAB_BG, 
                fg=AppColors.KU_COLOR).pack(side=tk.LEFT)
        
        # Löschen-Button
        delete_button = tk.Button(header_frame, text=Icons.DELETE,
                                font=Fonts.ICON, bg=AppColors.BUTTON_DANGER_BG,
                                fg=AppColors.BUTTON_DANGER_FG, bd=0,
                                command=lambda: self.RemoveChildEntry(child_frame),
                                cursor='hand2')
        delete_button.pack(side=tk.RIGHT)
        
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
        self.UpdateChildNumbers()

        if hasattr(self.tab_children, 'canvas'):
            self.BindMouseWheelToWidget(child_frame, self.tab_children.canvas)

    def RemoveChildEntry(self, frame):
        """Entfernt einen Kind-Eintrag"""
        for i, entry in enumerate(self.children_entries):
            if entry['frame'] == frame:
                self.children_entries.pop(i)
                break
        
        frame.destroy()
        self.UpdateChildNumbers()

    def UpdateChildNumbers(self):
        """Aktualisiert die Nummerierung der Ehen"""
        for i, entry in enumerate(self.children_entries):
            # Finde das Label im Header
            header_frame = entry['frame'].winfo_children()[0].winfo_children()[0]
            for widget in header_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=f"Kind #{i + 1}")
                    break

    def CreateScrollableTab(self, tab):
        """Erstellt einen scrollbaren Bereich innerhalb eines Tabs"""
        # Container für Canvas und Scrollbar
        scroll_container = tk.Frame(tab, bg=AppColors.TAB_BG)
        scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas
        canvas = tk.Canvas(scroll_container, bg=AppColors.TAB_BG, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar (initially hidden)
        scrollbar = ttk.Scrollbar(scroll_container, orient=tk.VERTICAL, command=canvas.yview)
        
        # Canvas mit Scrollbar verbinden
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame für den Inhalt
        content_frame = tk.Frame(canvas, bg=AppColors.TAB_BG)
        canvas_window = canvas.create_window(0, 0, anchor=tk.NW, window=content_frame)
        
        # Improved event handlers
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            update_scrollbar_visibility()
        
        def configure_canvas_width(event=None):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            update_scrollbar_visibility()
        
        def update_scrollbar_visibility():
            """Zeigt/versteckt Scrollbar basierend auf Inhaltsgröße"""
            canvas.update_idletasks()
            bbox = canvas.bbox("all")
            if bbox:
                content_height = bbox[3] - bbox[1]
                canvas_height = canvas.winfo_height()
                
                if content_height > canvas_height:
                    if not tab.scroll_enabled:
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                        tab.scroll_enabled = True
                else:
                    if tab.scroll_enabled:
                        scrollbar.pack_forget()
                        tab.scroll_enabled = False
        
        # Mouse wheel support
        def on_mousewheel(event):
            if tab.scroll_enabled:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind events
        content_frame.bind('<Configure>', configure_scroll_region)
        canvas.bind('<Configure>', configure_canvas_width)
        canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: on_mousewheel(type('obj', (object,), {'delta': 120})))  # Linux
        canvas.bind("<Button-5>", lambda e: on_mousewheel(type('obj', (object,), {'delta': -120})))  # Linux
        
        # Speichere Referenzen
        tab.canvas = canvas
        tab.scrollbar = scrollbar
        tab.content_frame = content_frame
        tab.scroll_enabled = False
        tab.update_scrollbar_visibility = update_scrollbar_visibility  # For external calls
        
        return content_frame  # Return the frame where content should be added

    def FilterTable(self, event=None):
        """Filtert die Tabelle basierend auf der Sucheingabe"""
        search_term = self.search_var.get().lower()
        
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
                self.delete_button.config(state=tk.NORMAL)  # Button aktivieren
                self.status_label.config(text=f"{Icons.INFO} {self.__current_roman['Name']} ausgewählt")
                self.EnableFields()
        else:
            self.__current_roman = None
            self.ClearDetails()
            self.delete_button.config(state=tk.DISABLED)  # Button deaktivieren
            self.status_label.config(text=Messages.NO_SELECTION)
            self.DisableFields()

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
        # Erstelle ein neues Roman-Objekt
        new_roman = Roman('')
        
        # Erstelle ein AddRomanCommand
        command = AddRomanCommand(self.__app.romans, new_roman)
        
        # Führe das Command aus
        self.__app.command_manager.ExecuteCommand(command)

        # Feld sperren
        self.create_button.config(state=tk.DISABLED)

        # In ersten Tab wechseln
        self.notebook.select(0)
        
        # Aktualisiere die Tabelle
        self.LoadTableData()
        
        # Wähle den neuen Römer aus
        # Finde das neue Item in der Tabelle
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == '':
                self.tree.selection_set(item)
                self.tree.see(item)  # Scrolle zum neuen Item
                break
        
        # Trigger OnSelect Event
        self.OnSelect()
        
        # Fokus auf das Name-Feld setzen
        if 'Name' in self.basic_fields:
            self.notebook.select(0)  # Wechsle zum ersten Tab
            name_widget = self.basic_fields['Name']
            name_widget.focus_set()
            name_widget.config(bg='#ffcccc')  # Markiere als Pflichtfeld

    def DisableFields(self):
        """Deaktiviert alle Felder und Buttons in den Tabs"""
        # Deaktiviere alle Felder in den Tabs
        for field in self.basic_fields.values():
            field.config(state=tk.DISABLED)
        
        # Deaktiviere Marriage Felder
        if hasattr(self, 'marriage_widget'):
            self.marriage_widget.config(state=tk.DISABLED)
        
        # Deaktiviere Children Felder  
        if hasattr(self, 'children_widget'):
            self.children_widget.config(state=tk.DISABLED)
        
        for field in self.family_fields.values():
            field.config(state=tk.DISABLED)
        
        for field in self.special_fields.values():
            field.config(state=tk.DISABLED)
        
        for field in self.honors_fields.values():
            field.config(state=tk.DISABLED)
        
        for field in self.sources_fields.values():
            field.config(state=tk.DISABLED)
        
        # Deaktiviere Buttons
        if hasattr(self, 'literary_add_button'):
            self.literary_add_button.config(state=tk.DISABLED)
        if hasattr(self, 'children_add_button'):
            self.children_add_button.config(state=tk.DISABLED)
        if hasattr(self, 'marriage_add_button'):
            self.marriage_add_button.config(state=tk.DISABLED)
        
        # Speichern Button deaktivieren
        self.save_button.config(state=tk.DISABLED)

    def EnableFields(self):
        """Aktiviert alle Felder und Buttons in den Tabs"""
        # Aktiviere alle Felder in den Tabs
        for field in self.basic_fields.values():
            field.config(state=tk.NORMAL)
        
        # Aktiviere Marriage Felder
        if hasattr(self, 'marriage_widget'):
            self.marriage_widget.config(state=tk.NORMAL)
        
        # Aktiviere Children Felder
        if hasattr(self, 'children_widget'):
            self.children_widget.config(state=tk.NORMAL)
        
        for field in self.family_fields.values():
            field.config(state=tk.NORMAL)
        
        for field in self.special_fields.values():
            field.config(state=tk.NORMAL)
        
        for field in self.honors_fields.values():
            field.config(state=tk.NORMAL)
        
        for field in self.sources_fields.values():
            field.config(state=tk.NORMAL)
        
        # Aktiviere Buttons
        if hasattr(self, 'literary_add_button'):
            self.literary_add_button.config(state=tk.NORMAL)
        if hasattr(self, 'children_add_button'):
            self.children_add_button.config(state=tk.NORMAL)
        if hasattr(self, 'marriage_add_button'):
            self.marriage_add_button.config(state=tk.NORMAL)
        
        # Speichern Button aktivieren
        self.save_button.config(state=tk.NORMAL)
    
    def UpdateButtonStates(self):
        """Aktualisiert die Button-Zustände basierend auf dem aktuellen Zustand"""
        if self.__current_roman is None:
            self.delete_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
        else:
            self.delete_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)

    def DeleteSelectedRoman(self):
        """Löscht den ausgewählten Römer"""
        if self.__current_roman is None:
            return
        
        # Bestätigungsdialog
        result = messagebox.askyesno(
            "Römer löschen", 
            f"Möchten Sie '{self.__current_roman.get('Name', 'Unbenannt')}' wirklich löschen?"
        )
        
        if not result:
            return
        
        self.create_button.config(state=tk.NORMAL)
        
        # Erstelle ein RemoveRomanCommand
        command = RemoveRomanCommand(self.__app.romans, self.__app.romans.index(self.__current_roman))
        
        # Führe das Command aus
        self.__app.command_manager.ExecuteCommand(command)
        
        # Aktualisiere die Tabelle
        self.LoadTableData()
        
        # Leere die Detailfelder
        self.ClearDetails()
        
        # Setze den aktuellen Römer auf None
        self.__current_roman = None
        
        # Button deaktivieren
        self.delete_button.config(state=tk.DISABLED)
        
        self.__app.menu_manager.UpdateEditMenuState()
        self.__app.file_modified = True

    def SaveChanges(self):
        """Speichert die Änderungen"""

        self.create_button.config(state=tk.NORMAL)

        if self.__current_roman is None:
            return
        
        # Validiere das Formular
        if not self.ValidateForm():
            return
        
        # Sammle die geänderten Eigenschaften
        properties = self.__current_roman.properties.copy()
        
        # ========== GRUNDDATEN TAB ==========
        basic_fields_mapping = {
            'Name': 'Name',
            'Geburtsdatum': 'Geburtsdatum',
            'Geburtsort': 'Geburtsort',
            'Sterbedatum': 'Sterbedatum',
            'Sterbeort': 'Sterbeort',
            'Todesursache': 'Todesursache',
            'Bemerkungen': 'Bemerkungen'
        }
        
        for field_key, json_key in basic_fields_mapping.items():
            if field_key in self.basic_fields:
                widget = self.basic_fields[field_key]
                if isinstance(widget, tk.Text):
                    properties[json_key] = widget.get('1.0', tk.END).strip()
                else:
                    properties[json_key] = widget.get().strip()
        
        # ========== EHEN TAB ==========
        properties['Anzahl Ehen'] = self.marriage_widget.get().strip()
        ehen = []
        for entry in self.marriage_entries:
            ehe = {}
            fields = entry['fields']
            
            if 'Partner' in fields:
                ehe['Partner'] = fields['Partner'].get().strip()
            
            if 'Heiratsdatum' in fields:
                ehe['Heiratsdatum'] = fields['Heiratsdatum'].get().strip()
            
            if 'Heiratsort' in fields:
                ehe['Heiratsort'] = fields['Heiratsort'].get().strip()
            
            if 'Bemerkungen' in fields:
                ehe['Bemerkungen'] = fields['Bemerkungen'].get('1.0', tk.END).strip()
            
            ehen.append(ehe)
        
        properties['Ehen'] = ehen
        
        # ========== KINDER TAB ==========
        properties['Anzahl Kinder'] = self.children_widget.get().strip()
        kinder = []
        for entry in self.children_entries:
            kind = {}
            fields = entry['fields']
            
            if 'Name' in fields:
                kind['Name'] = fields['Name'].get().strip()
            
            if 'Geschlecht' in fields:
                kind['Geschlecht'] = fields['Geschlecht'].get().strip()
            
            if 'Geburtsjahr' in fields:
                kind['Geburtsjahr'] = fields['Geburtsjahr'].get().strip()
            
            if 'Bemerkungen' in fields:
                kind['Bemerkungen'] = fields['Bemerkungen'].get('1.0', tk.END).strip()
            
            kinder.append(kind)
        
        properties['Kinder'] = kinder
        
        # ========== FAMILIE TAB ==========
        family_fields_mapping = {
            'Vater': 'Vater',
            'Mutter': 'Mutter',
            'Geschwister': 'Geschwister',
            'Vorfahren': 'Vorfahren',
            'Bemerkungen': 'Familienbemerkungen'
        }
        
        for field_key, json_key in family_fields_mapping.items():
            if field_key in self.family_fields:
                widget = self.family_fields[field_key]
                if isinstance(widget, tk.Text):
                    properties[json_key] = widget.get('1.0', tk.END).strip()
                else:
                    properties[json_key] = widget.get().strip()
        
        # ========== BESONDERHEITEN TAB ==========
        besonderheiten = {}
        
        if 'Auftreten' in self.special_fields:
            besonderheiten['Auftreten'] = self.special_fields['Auftreten'].get().strip()
        
        if 'Kleidung' in self.special_fields:
            besonderheiten['Kleidung'] = self.special_fields['Kleidung'].get().strip()
        
        if 'Schmuck' in self.special_fields:
            besonderheiten['Schmuck'] = self.special_fields['Schmuck'].get().strip()
        
        if 'Öffentlich' in self.special_fields:
            besonderheiten['Öffentlich'] = self.special_fields['Öffentlich'].get('1.0', tk.END).strip()
        
        if 'Privat' in self.special_fields:
            besonderheiten['Privat'] = self.special_fields['Privat'].get('1.0', tk.END).strip()
        
        if 'Bemerkungen' in self.special_fields:
            besonderheiten['Bemerkungen'] = self.special_fields['Bemerkungen'].get('1.0', tk.END).strip()
        
        properties['Besonderheiten'] = besonderheiten
        
        # ========== EHRUNGEN TAB ==========
        ehrungen = {}
        
        if 'Augusta-Titel-Status' in self.honors_fields:
            ehrungen['Augusta-Titel-Status'] = self.honors_fields['Augusta-Titel-Status'].get().strip()
        
        if 'Augusta-Titel-Details' in self.honors_fields:
            ehrungen['Augusta-Titel-Details'] = self.honors_fields['Augusta-Titel-Details'].get('1.0', tk.END).strip()
        
        if 'Carpentum-Recht-Status' in self.honors_fields:
            ehrungen['Carpentum-Recht-Status'] = self.honors_fields['Carpentum-Recht-Status'].get().strip()

        if 'Carpentum-Recht-Details' in self.honors_fields:
            ehrungen['Carpentum-Recht-Details'] = self.honors_fields['Carpentum-Recht-Details'].get('1.0', tk.END).strip()
        
        if 'Weitere' in self.honors_fields:
            ehrungen['Weitere'] = self.honors_fields['Weitere'].get('1.0', tk.END).strip()
        
        properties['Ehrungen'] = ehrungen
        
        # ========== QUELLEN TAB ==========
        quellen = {}
        
        if 'Divinisierung' in self.sources_fields:
            quellen['Divinisierung'] = self.sources_fields['Divinisierung'].get('1.0', tk.END).strip()
        
        if 'Bestattung' in self.sources_fields:
            quellen['Bestattung'] = self.sources_fields['Bestattung'].get('1.0', tk.END).strip()
        
        if 'Archäologische Quellen' in self.sources_fields:
            quellen['Archäologische Quellen'] = self.sources_fields['Archäologische Quellen'].get('1.0', tk.END).strip()
        
        if 'Münzen' in self.sources_fields:
            quellen['Münzen'] = self.sources_fields['Münzen'].get('1.0', tk.END).strip()
        
        if 'Inschriften' in self.sources_fields:
            quellen['Inschriften'] = self.sources_fields['Inschriften'].get('1.0', tk.END).strip()
        
        properties['Quellen'] = quellen
        
        # ========== LITERARISCHE QUELLEN TAB ==========
        literarische_quellen = []
        for entry in self.literary_sources_entries:
            quelle = {}
            fields = entry['fields']
            
            if 'Autor' in fields:
                quelle['Autor'] = fields['Autor'].get().strip()
            
            if 'Link' in fields:
                quelle['Link'] = fields['Link'].get().strip()
            
            if 'Zitat' in fields:
                quelle['Zitat'] = fields['Zitat'].get('1.0', tk.END).strip()
            
            if 'Notizen' in fields:
                quelle['Notizen'] = fields['Notizen'].get('1.0', tk.END).strip()
            
            literarische_quellen.append(quelle)
        
        properties['Literarische Quellen'] = literarische_quellen
        
        # Erstelle ein EditRomanCommand
        command = EditRomanCommand(self.__current_roman, properties)
        
        # Führe das Command aus
        self.__app.command_manager.ExecuteCommand(command)
        
        # Aktualisiere die Tabelle
        self.LoadTableData()
        # Erfolgs-Feedback
        self.status_label.config(text=f"{Icons.SUCCESS} Änderungen gespeichert")

        # Zeige Erfolgs-Meldung
        messagebox.showinfo(
            "Speichern erfolgreich",
            f"Die Änderungen für '{properties.get('Name', 'Unbekannt')}' wurden erfolgreich gespeichert."
        )

        self.__app.menu_manager.UpdateEditMenuState()
        self.__app.file_modified = True

    def ExportData(self):
        """Exportiert die Daten"""
        print(f"{Icons.EXPORT} Daten exportieren...")

    def ClearDetails(self):
        """Leert alle Detailfelder"""
        # ========== GRUNDDATEN TAB ==========
        for field in self.basic_fields.values():
            if isinstance(field, tk.Text):
                field.delete('1.0', tk.END)
            else:
                field.delete(0, tk.END)
        
        # ========== EHEN TAB ==========
        self.marriage_widget.delete(0, tk.END)
        for entry in self.marriage_entries[:]:
            entry['frame'].destroy()
        self.marriage_entries.clear()
        
        # ========== KINDER TAB ==========
        self.children_widget.delete(0, tk.END)
        for entry in self.children_entries[:]:
            entry['frame'].destroy()
        self.children_entries.clear()
        
        # ========== FAMILIE TAB ==========
        for field in self.family_fields.values():
            if isinstance(field, tk.Text):
                field.delete('1.0', tk.END)
            else:
                field.delete(0, tk.END)
        
        # ========== BESONDERHEITEN TAB ==========
        for field in self.special_fields.values():
            if isinstance(field, tk.Text):
                field.delete('1.0', tk.END)
            else:
                field.delete(0, tk.END)
        
        # ========== EHRUNGEN TAB ==========
        for field in self.honors_fields.values():
            if isinstance(field, tk.Text):
                field.delete('1.0', tk.END)
            elif isinstance(field, ttk.Combobox):
                field.set('')
            else:
                field.delete(0, tk.END)
        
        # ========== QUELLEN TAB ==========
        for field in self.sources_fields.values():
            if isinstance(field, tk.Text):
                field.delete('1.0', tk.END)
            else:
                field.delete(0, tk.END)
        
        # ========== LITERARISCHE QUELLEN TAB ==========
        for entry in self.literary_sources_entries[:]:
            entry['frame'].destroy()
        self.literary_sources_entries.clear()
        
        # Status-Label zurücksetzen
        self.status_label.config(text=Messages.NO_SELECTION)

    def DisplayRoman(self):
        """Zeigt die Daten des ausgewählten Römers in allen Feldern an"""
        if self.__current_roman is None:
            return
        
        self.ClearDetails()
        self.EnableFields()
        
        # ========== GRUNDDATEN TAB ==========
        # Einfache Textfelder
        basic_fields_mapping = {
            'Name': 'Name',
            'Geburtsdatum': 'Geburtsdatum',
            'Geburtsort': 'Geburtsort',
            'Sterbedatum': 'Sterbedatum',
            'Sterbeort': 'Sterbeort',
            'Todesursache': 'Todesursache',
            'Bemerkungen': 'Bemerkungen'
        }
        
        for field_key, json_key in basic_fields_mapping.items():
            if field_key in self.basic_fields:
                widget = self.basic_fields[field_key]
                value = self.__current_roman.get(json_key, '')
                
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
                    widget.insert('1.0', value)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)

                # Validiere Name-Feld nach dem Laden
                if field_key == 'Name':
                    self.ValidateNameField()
        
        # ========== EHEN TAB ==========
        # Erst alle vorhandenen Ehen-Einträge löschen
        self.marriage_widget.delete(0, tk.END)
        self.marriage_widget.insert(0, self.__current_roman.get('Anzahl Ehen', ''))
        for entry in self.marriage_entries[:]:
            entry['frame'].destroy()
        self.marriage_entries.clear()
        
        # Ehen aus den Daten laden
        ehen = self.__current_roman.get('Ehen', [])
        for ehe in ehen:
            self.AddMarriageEntry(self.marriages_container)
            # Letzten hinzugefügten Eintrag füllen
            if self.marriage_entries:
                last_entry = self.marriage_entries[-1]
                fields = last_entry['fields']
                
                if 'Partner' in fields and 'Partner' in ehe:
                    fields['Partner'].delete(0, tk.END)
                    fields['Partner'].insert(0, ehe['Partner'])
                
                if 'Heiratsdatum' in fields and 'Heiratsdatum' in ehe:
                    fields['Heiratsdatum'].delete(0, tk.END)
                    fields['Heiratsdatum'].insert(0, ehe['Heiratsdatum'])
                
                if 'Heiratsort' in fields and 'Heiratsort' in ehe:
                    fields['Heiratsort'].delete(0, tk.END)
                    fields['Heiratsort'].insert(0, ehe['Heiratsort'])

                if 'Bemerkungen' in fields and 'Bemerkungen' in ehe:    # Textfeld
                    fields['Bemerkungen'].delete('1.0', tk.END)
                    fields['Bemerkungen'].insert('1.0', ehe['Bemerkungen'])
        
        # ========== KINDER TAB ==========
        # Erst alle vorhandenen Kinder-Einträge löschen
        self.children_widget.delete(0, tk.END)
        self.children_widget.insert(0, self.__current_roman.get('Anzahl Kinder', ''))
        for entry in self.children_entries[:]:
            entry['frame'].destroy()
        self.children_entries.clear()
        
        # Kinder aus den Daten laden
        kinder = self.__current_roman.get('Kinder', [])
        for kind in kinder:
            self.AddChildEntry(self.children_container)
            # Letzten hinzugefügten Eintrag füllen
            if self.children_entries:
                last_entry = self.children_entries[-1]
                fields = last_entry['fields']
                
                if 'Name' in fields and 'Name' in kind:
                    fields['Name'].delete(0, tk.END)
                    fields['Name'].insert(0, kind['Name'])
                
                if 'Geschlecht' in fields and 'Geschlecht' in kind:
                    fields['Geschlecht'].set(kind['Geschlecht'])
                
                if 'Geburtsjahr' in fields and 'Geburtsjahr' in kind:
                    fields['Geburtsjahr'].delete(0, tk.END)
                    fields['Geburtsjahr'].insert(0, kind['Geburtsjahr'])
                
                if 'Bemerkungen' in fields and 'Bemerkungen' in kind:
                    fields['Bemerkungen'].delete('1.0', tk.END)
                    fields['Bemerkungen'].insert('1.0', kind['Bemerkungen'])
        
        # ========== FAMILIE TAB ==========
        family_fields_mapping = {
            'Vater': 'Vater',
            'Mutter': 'Mutter',
            'Geschwister': 'Geschwister',
            'Vorfahren': 'Vorfahren',
            'Bemerkungen': 'Familienbemerkungen'
        }
        
        for field_key, json_key in family_fields_mapping.items():
            if field_key in self.family_fields:
                widget = self.family_fields[field_key]
                value = self.__current_roman.get(json_key, '')
                
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
                    widget.insert('1.0', value)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)
        
        # ========== BESONDERHEITEN TAB ==========
        besonderheiten = self.__current_roman.get('Besonderheiten', {})
        
        # Äußere Erscheinung
        if 'Auftreten' in self.special_fields:
            self.special_fields['Auftreten'].delete(0, tk.END)
            self.special_fields['Auftreten'].insert(0, besonderheiten.get('Auftreten', ''))
        
        if 'Kleidung' in self.special_fields:
            self.special_fields['Kleidung'].delete(0, tk.END)
            self.special_fields['Kleidung'].insert(0, besonderheiten.get('Kleidung', ''))
        
        if 'Schmuck' in self.special_fields:
            self.special_fields['Schmuck'].delete(0, tk.END)
            self.special_fields['Schmuck'].insert(0, besonderheiten.get('Schmuck', ''))
        
        # Inszenierung
        
        if 'Öffentlich' in self.special_fields:
            self.special_fields['Öffentlich'].delete('1.0', tk.END)
            self.special_fields['Öffentlich'].insert('1.0', besonderheiten.get('Öffentlich', ''))
            if self.special_fields['Öffentlich'].get('1.0', 'end-1c'):
                self.special_fields['Öffentlich'].config(fg=AppColors.INPUT_FG)
        
        if 'Privat' in self.special_fields:
            self.special_fields['Privat'].delete('1.0', tk.END)
            self.special_fields['Privat'].insert('1.0', besonderheiten.get('Privat', ''))
            if self.special_fields['Privat'].get('1.0', 'end-1c'):
                self.special_fields['Privat'].config(fg=AppColors.INPUT_FG)
        
        if 'Bemerkungen' in self.special_fields:
            self.special_fields['Bemerkungen'].delete('1.0', tk.END)
            self.special_fields['Bemerkungen'].insert('1.0', besonderheiten.get('Bemerkungen', ''))
        
        # ========== EHRUNGEN TAB ==========
        ehrungen = self.__current_roman.get('Ehrungen', {})
        
        # Augusta-Titel
        augusta_status = ehrungen.get('Augusta-Titel-Status', '')
        if 'Augusta-Titel-Status' in self.honors_fields:
            # Extrahiere Status (JA/NEIN) aus dem Text
            if augusta_status == 'Ja':
                self.honors_fields['Augusta-Titel-Status'].set('Ja')
            elif augusta_status == 'Nein':
                self.honors_fields['Augusta-Titel-Status'].set('Nein')
            else:
                self.honors_fields['Augusta-Titel-Status'].set('Unbekannt')
        
        augusta_details = ehrungen.get('Augusta-Titel-Details', '')
        if 'Augusta-Titel-Details' in self.honors_fields:
            # Füge den vollen Text ein
            self.honors_fields['Augusta-Titel-Details'].insert('1.0', augusta_details)
            if augusta_details:
                self.honors_fields['Augusta-Titel-Details'].config(fg=AppColors.INPUT_FG)
        
        # Carpentum-Recht
        carpentum_status = ehrungen.get('Carpentum-Recht-Status', '')
        if 'Carpentum-Recht-Status' in self.honors_fields:
            if carpentum_status == 'Ja':
                self.honors_fields['Carpentum-Recht-Status'].set('Ja')
            elif carpentum_status == 'Nein':
                self.honors_fields['Carpentum-Recht-Status'].set('Nein')
            else:
                self.honors_fields['Carpentum-Recht-Status'].set('Unbekannt')
        
        carpentum_details = ehrungen.get('Carpentum-Recht-Details', '')
        if 'Carpentum-Recht-Details' in self.honors_fields:
            self.honors_fields['Carpentum-Recht-Details'].delete('1.0', tk.END)
            self.honors_fields['Carpentum-Recht-Details'].insert('1.0', carpentum_details)
            if carpentum_details:
                self.honors_fields['Carpentum-Recht-Details'].config(fg=AppColors.INPUT_FG)
        
        # Weitere Ehrungen
        if 'Weitere' in self.honors_fields:
            self.honors_fields['Weitere'].delete('1.0', tk.END)
            weitere_value = ehrungen.get('Weitere', '')
            self.honors_fields['Weitere'].insert('1.0', weitere_value)
            if weitere_value:
                self.honors_fields['Weitere'].config(fg=AppColors.INPUT_FG)
        
        # ========== QUELLEN TAB ==========
        quellen = self.__current_roman.get('Quellen', {})
        
        quellen_fields_mapping = {
            'Divinisierung': 'Divinisierung',
            'Bestattung': 'Bestattung',
            'Archäologische Quellen': 'Archäologische Quellen',
            'Münzen': 'Münzen',
            'Inschriften': 'Inschriften'
        }
        
        for field_key, json_key in quellen_fields_mapping.items():
            if field_key in self.sources_fields:
                widget = self.sources_fields[field_key]
                value = quellen.get(json_key, '')
                
                # Füge neuen Wert ein
                if value:
                    widget.insert('1.0', value)
                    widget.config(fg=AppColors.INPUT_FG)
        
        # ========== LITERARISCHE QUELLEN TAB ==========
        # Erst alle vorhandenen Einträge löschen
        for entry in self.literary_sources_entries[:]:
            entry['frame'].destroy()
        self.literary_sources_entries.clear()
        
        # Literarische Quellen laden
        lit_quellen = self.__current_roman.get('Literarische Quellen', [])
        
        if lit_quellen:
            for quelle in lit_quellen:
                self.AddLiterarySourceEntry(self.literary_sources_container)
                
                # Letzten hinzugefügten Eintrag füllen
                if self.literary_sources_entries:
                    last_entry = self.literary_sources_entries[-1]
                    fields = last_entry['fields']
                    
                    if 'Autor' in fields and 'Autor' in quelle:
                        fields['Autor'].delete(0, tk.END)
                        fields['Autor'].insert(0, quelle['Autor'])
                        fields['Autor'].config(fg=AppColors.INPUT_FG)
                    
                    if 'Link' in fields and 'Link' in quelle:
                        fields['Link'].delete(0, tk.END)
                        fields['Link'].insert(0, quelle['Link'])
                        fields['Link'].config(fg=AppColors.INPUT_FG)
                    
                    if 'Zitat' in fields and 'Zitat' in quelle:
                        fields['Zitat'].delete('1.0', tk.END)
                        fields['Zitat'].insert('1.0', quelle['Zitat'])
                        fields['Zitat'].config(fg=AppColors.INPUT_FG)
                    
                    if 'Notizen' in fields and 'Notizen' in quelle:
                        fields['Notizen'].delete('1.0', tk.END)
                        fields['Notizen'].insert('1.0', quelle['Notizen'])
                        fields['Notizen'].config(fg=AppColors.INPUT_FG)
        
        # Tab-Auswahl wiederherstellen
        if hasattr(self.__class__, 'last_selected_tab'):
            try:
                self.notebook.select(self.__class__.last_selected_tab)
            except:
                self.notebook.select(0)