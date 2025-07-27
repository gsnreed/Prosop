import tkinter as tk
import time
from datetime import datetime
import os
import sys

# Projektverzeichnis zum Suchpfad hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Absolute Importe
from Objects.Config import AppConfig, AppColors
from Objects.Logger import logger
from Objects.Content import ContentManager

# --- UI-Komponenten ---
class TopFrame(tk.Frame):
    """
    Oberer Rahmen der Anwendung mit Logo, Titel und Uhr.
    """
    
    def __init__(self, parent) -> None:
        """Initialisiere den oberen Rahmen"""
        super().__init__(parent, bg=AppColors.TOP_FRAME)
        
        # Grid-Layout konfigurieren
        self.columnconfigure(0, weight=0)  # Logo-Spalte (feste Größe)
        self.columnconfigure(1, weight=1)  # Titel-Spalte (dehnbar)
        self.columnconfigure(2, weight=0)  # Uhr-Spalte (feste Größe)
        
        # Erstelle UI-Komponenten
        self._CreateLogo()
        self._CreateTitle()
        self._CreateClock()
    
    def _CreateLogo(self) -> None:
        """Erstellt und platziert das Universitätslogo"""
        self.uni_logo = tk.PhotoImage(file=AppConfig.UNIVERSITY_LOGO).subsample(15)
        logo_label = tk.Label(self, image=self.uni_logo, bg=AppColors.TOP_FRAME)
        logo_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    
    def _CreateTitle(self) -> None:
        """Erstellt und platziert den Anwendungstitel"""
        self.title_label = tk.Label(
            self,
            font=('Helvetica', 15, 'bold'),
            bg=AppColors.TOP_FRAME,
            fg=AppColors.KU_COLOR,
            text=AppConfig.MAIN_TITLE
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')
    
    def _CreateClock(self) -> None:
        """Erstellt und platziert die Uhr"""
        self.time_label = tk.Label(
            self,
            font=('Helvetica', 15),
            bg=AppColors.TOP_FRAME,
            fg=AppColors.KU_COLOR
        )
        self.time_label.grid(row=0, column=2, padx=20, pady=10, sticky='e')
        self.UpdateClock()
    
    def UpdateClock(self) -> None:
        """Aktualisiert das Zeit-Label mit der aktuellen Uhrzeit"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        # Aktualisiere die Uhr jede Sekunde
        self.after(1000, self.UpdateClock)

class SubMenuFrame(tk.Frame):
    """
    Rahmen für Submenü-Optionen, erscheint rechts neben dem Navigation Frame.
    """
    
    def __init__(self, parent) -> None:
        super().__init__(parent, bg=AppColors.SUBMENU_FRAME)
        self.parent = parent
        self.selected_submenu_item = None
        self.submenu_labels = {}  # Speichert alle Submenu-Labels
        
        # Submenü-Header erstellen
        self.submenu_header = tk.Label(
            self,
            font=('Helvetica', 12, 'bold'),
            bg=AppColors.SUBMENU_FRAME,
            fg=AppColors.KU_COLOR,
            text="Unterkategorien"
        )
        self.submenu_header.pack(side='top', fill='x', padx=10, pady=(10,5))
        
        # Frame für Submenü-Optionen
        self.options_frame = tk.Frame(self, bg=AppColors.SUBMENU_FRAME)
        self.options_frame.pack(fill='both', expand=True, padx=5)
        
        # Definiere verfügbare Submenüs
        self.submenus = {
            'Ansicht': ['Liste', 'Karte', 'Tabelle', 'Zeitstrahl'],
            'Erstellung': ['Person', 'Ort', 'Ereignis', 'Quelle'],
            'Export': ['PDF', 'CSV', 'Excel', 'JSON'],
            'Import': ['CSV-Import', 'JSON-Import', 'Datenbank-Import'],
            'BibTex': ['Literatur hinzufügen', 'Zitieren', 'Verwalten']
        }
    
    def UpdateSubmenu(self, option: str) -> None:
        """Aktualisiert die Submenüoptionen für die gewählte Hauptoption"""
        # Bestehende Optionen entfernen
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Zurücksetzen der Label-Sammlung
        self.submenu_labels = {}
        self.selected_submenu_item = None
        
        # Header aktualisieren
        self.submenu_header.config(text=f"{option}")
        
        # Neue Optionen hinzufügen
        if option in self.submenus:
            submenu_items = self.submenus[option]
            for sub_option in submenu_items:
                label = tk.Label(
                    self.options_frame,
                    text=sub_option,
                    font=('Helvetica', 11),
                    bg=AppColors.SUBMENU_FRAME,
                    fg=AppColors.KU_COLOR,
                    padx=15,
                    pady=4,
                    cursor="hand2",
                    anchor='w'  # Linksbündiger Text
                )
                label.pack(fill='x', pady=1)
                
                # Event-Binding für das Label
                label.bind("<Enter>", lambda e, l=label: self.OnSubMenuHover(l, True))
                label.bind("<Leave>", lambda e, l=label: self.OnSubMenuHover(l, False))
                label.bind("<Button-1>", lambda e, o=option, s=sub_option: self.OnSubMenuSelect(o, s))
                
                # Label speichern
                self.submenu_labels[sub_option] = label
            
            # Automatisch das erste Element auswählen
            if submenu_items:
                first_option = submenu_items[0]
                self.OnSubMenuSelect(option, first_option)
    
    def OnSubMenuHover(self, label: str, is_hover: bool) -> None:
        """Behandelt Hover-Events für Submenüoptionen"""
        sub_option = label.cget("text")
        # Nur hervorheben, wenn nicht ausgewählt
        if sub_option != self.selected_submenu_item:
            if is_hover:
                label.configure(bg=AppColors.HOVER)
            else:
                label.configure(bg=AppColors.SUBMENU_FRAME)
    
    def OnSubMenuSelect(self, option: str, sub_option: str) -> None:
        """Behandelt die Auswahl einer Submenüoption"""
        # Zurücksetzen der vorherigen Auswahl
        if self.selected_submenu_item and self.selected_submenu_item in self.submenu_labels:
            old_label = self.submenu_labels[self.selected_submenu_item]
            old_label.configure(
                bg=AppColors.SUBMENU_FRAME,
                font=('Helvetica', 11),  # Normale Schrift
                fg=AppColors.KU_COLOR
            )
        
        # Neue Auswahl setzen
        self.selected_submenu_item = sub_option
        if sub_option in self.submenu_labels:
            selected_label = self.submenu_labels[sub_option]
            selected_label.configure(
                bg=AppColors.HOVER,
                font=('Helvetica', 11, 'bold'),  # Fettschrift
                
            )
        
        # Inhalt aktualisieren
        self.parent.HandleSubmenuSelect(option, sub_option)

        # Ereignis protokollieren
        logger.info(f"Option '{sub_option}' ausgewählt")

class NavigationFrame(tk.Frame):
    """
    Seitenleiste mit Navigationsoptionen.
    """
    
    def __init__(self, parent, content_updater) -> None:
        super().__init__(parent, bg=AppColors.SIDEBAR_FRAME)
        self.content_updater = content_updater
        self.nav_labels = {}
        self.selected_option = None
        
        # Definiere, welche Optionen Submenus haben
        self.options_with_submenu = ['Ansicht', 'Erstellung', 'Export', 'Import', 'BibTex']
        
        self._CreateHeader()
        self._CreateNavigationOptions()
    
    def _CreateHeader(self) -> None:
        """Erstellt die Navigationsüberschrift"""
        self.navigation_header = tk.Label(
            self,
            font=('Helvetica', 15, 'bold'),
            bg=AppColors.SIDEBAR_FRAME,
            fg=AppColors.KU_COLOR,
            text=AppConfig.NAVIGATION_TITLE
        )
        self.navigation_header.pack(side='top', padx=10, pady=10)  # Padding hinzugefügt
    
    def _CreateNavigationOptions(self) -> None:
        """Erstellt alle Navigationsoptionen"""
        # Container-Frame mit Padding
        container_frame = tk.Frame(self, bg=AppColors.SIDEBAR_FRAME)
        container_frame.pack(fill=tk.X, padx=5)  # Padding links und rechts
        
        options_frame = tk.Frame(container_frame, bg=AppColors.SIDEBAR_FRAME)
        options_frame.pack(fill=tk.X, pady=2)
        
        # Erstelle für jede Option ein Label
        for option in AppConfig.NAV_OPTIONS:
            # Markiere Optionen mit Submenü
            has_submenu = option in self.options_with_submenu
            prefix = "» " if has_submenu else "  "
            
            label = tk.Label(
                options_frame,
                text=prefix + option,
                font=('Helvetica', 12),
                bg=AppColors.SIDEBAR_FRAME,
                fg=AppColors.KU_COLOR,
                padx=15,  # Reduziert von 20 auf 15 für konsistenteres Aussehen
                pady=5,
                cursor="hand2",
                anchor=tk.w
            )
            label.pack(fill=tk.X, pady=2)
            
            # Event-Binding für das Label
            label.bind("<Enter>", lambda e, opt=option: self.OnHover(opt, True))
            label.bind("<Leave>", lambda e, opt=option: self.OnHover(opt, False))
            label.bind("<Button-1>", lambda e, opt=option: self.OnSelect(opt))
            
            # Label im Dictionary speichern
            self.nav_labels[option] = label
    
    def HasSubmenu(self, option: str) -> None:
        """Prüft, ob eine Option ein Submenü hat"""
        return option in self.options_with_submenu
    
    def OnHover(self, option: str, is_hover: bool) -> None:
        """Behandelt Hover-Events für Navigationsoptionen"""
        label = self.nav_labels[option]
        # Nur hervorheben, wenn nicht ausgewählt
        if option != self.selected_option:
            if is_hover:
                label.configure(bg=AppColors.HOVER)
            else:
                label.configure(bg=AppColors.SIDEBAR_FRAME)
    
    def OnSelect(self, option: str) -> None:
        """Behandelt die Auswahl einer Navigationsoption"""
        # Zurücksetzen der vorherigen Auswahl
        if self.selected_option:
            old_label = self.nav_labels[self.selected_option]
            prefix = "» " if self.HasSubmenu(self.selected_option) else "  "
            old_label.configure(
                bg=AppColors.SIDEBAR_FRAME,
                fg=AppColors.KU_COLOR,
                font=('Helvetica', 12),
                text=prefix + self.selected_option
            )
        
        # Neue Auswahl setzen
        self.selected_option = option
        selected_label = self.nav_labels[option]
        prefix = "» " if self.HasSubmenu(option) else "  "
        selected_label.configure(
            bg=AppColors.HOVER,
            fg=AppColors.KU_COLOR,
            font=('Helvetica', 12, 'bold'),
            text=prefix + option
        )
        
        # Inhalt aktualisieren
        self.content_updater.UpdateContent(option)
        
        # Ereignis protokollieren
        logger.info(f"Navigation: Option '{option}' ausgewählt")

class ContentFrame(tk.Frame):
    """
    Hauptinhaltsfläche für den ausgewählten Navigationsbereich.
    """
    
    def __init__(self, parent) -> None:
        """Initialisiere den Inhaltsrahmen"""
        super().__init__(parent, bg=AppColors.CONTENT_FRAME)
        self.content_manager = ContentManager(self)
    
    def UpdateContent(self, option: str) -> None:
        """Aktualisiert den Inhalt basierend auf der ausgewählten Navigation."""
        self.content_manager.ShowContent(option)

        # Ereignis protokollieren
        logger.info(f"Content der Option '{option}' wurde geladen.")