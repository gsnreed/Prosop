import sys
import os
import tkinter as tk

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors, Fonts, AppConfig
from utils.logger import logger

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
            font=Fonts.STANDARD_BOLD,
            bg=AppColors.SUBMENU_FRAME,
            fg=AppColors.KU_COLOR,
            text="Unterkategorien"
        )
        self.submenu_header.pack(side='top', fill='x', padx=10, pady=(10,5))
        
        # Frame für Submenü-Optionen
        self.options_frame = tk.Frame(self, bg=AppColors.SUBMENU_FRAME)
        self.options_frame.pack(fill='both', expand=True, padx=5)
        
        # Definiere verfügbare Submenüs
        self.submenus = AppConfig.SUBMENUS
    
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
                    font=Fonts.SUBMENU,
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
                font=Fonts.SUBMENU,  # Normale Schrift
                fg=AppColors.KU_COLOR
            )
        
        # Neue Auswahl setzen
        self.selected_submenu_item = sub_option
        if sub_option in self.submenu_labels:
            selected_label = self.submenu_labels[sub_option]
            selected_label.configure(
                bg=AppColors.HOVER,
                font=Fonts.SUBMENU_BOLD,  # Fettschrift
                
            )
        
        # Inhalt aktualisieren
        self.parent.HandleSubmenuSelect(option, sub_option)

        # Ereignis protokollieren
        logger.info(f"Option '{sub_option}' ausgewählt")