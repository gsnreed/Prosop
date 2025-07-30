import tkinter as tk
from tkinter import ttk
import os
import sys

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors, Fonts
from ui.frames.content.base_content import BaseContentFrame
from utils.logger import logger

class CreateFrame(BaseContentFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__current_roman = None
        self.__app = self.FindMainApp(parent)

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
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 3)
        self.columnconfigure(0, weight=1)

        # Tabellenansicht
        top_frame = tk.Frame(self, bg = AppColors.CONTENT_FRAME)
        top_frame.grid(row=0, column = 0, sticky='nsew', padx = 10, pady=(10, 5))

        # Header mit Suchfeld
        header_frame = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        header_frame.pack(fill='x', pady=(0, 10))

        header_label = tk.Label(header_frame, text='Editieren von Römern', font=Fonts.HEADER, bg = AppColors.CONTENT_FRAME, fg=AppColors.KU_COLOR)
        header_label.pack(side='left', padx = 10)

        # Suchfeld
        search_frame = tk.Frame(header_frame, bg = AppColors.CONTENT_FRAME)
        search_frame.pack(side='right', padx=10)

        search_label = tk.Label(search_frame, bg=AppColors.CONTENT_FRAME, fg=AppColors.KU_COLOR, font=Fonts.STANDARD_BOLD, text='Suche')
        search_label.pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        seacrh_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, font=Fonts.STANDARD, fg = AppColors.KU_COLOR, bd=1, relief='solid')
        seacrh_entry.pack(side='left', padx=(0, 10))
        seacrh_entry.bind('<KeyRelease>', self.FilterTable)

        # Tabelle
        table_frame = tk.Frame(top_frame, bg=AppColors.CONTENT_FRAME)
        table_frame.pack(fill='both', expand=True)

        y_scrollbar = ttk.Scrollbar(table_frame)
        y_scrollbar.pack(side='right', fill='y')

        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal')
        x_scrollbar.pack(side='bottom', fill='x')

        columns = ('Name', 'Geburt', 'Tod', 'Todesursache', 'Familie', 'Ehemänner', 'Kinder')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Scrollbars mit Treeview verbinden
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)

        # Spaltenüberschriften definieren
        self.tree.heading("Name", text="Name")
        self.tree.heading("Geburt", text="Geburt")
        self.tree.heading("Tod", text="Tod")
        self.tree.heading("Todesursache", text="Todesursache")
        self.tree.heading("Familie", text="Familie")
        self.tree.heading("Ehemänner", text="Ehemänner")
        self.tree.heading("Kinder", text="Kinder")
        
        self.tree.pack(fill="both", expand=True)
    
    def FilterTable(self):
        pass