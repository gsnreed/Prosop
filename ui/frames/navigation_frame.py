import sys
import os
import tkinter as tk

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors, AppConfig, Fonts
from utils.logger import logger

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
        self.options_with_submenu = AppConfig.SUBMENUS.keys()
        
        self._CreateHeader()
        self._CreateNavigationOptions()
    
    def _CreateHeader(self) -> None:
        """Erstellt die Navigationsüberschrift"""
        self.navigation_header = tk.Label(
            self,
            font=Fonts.HEADER,
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
                font=Fonts.STANDARD,
                bg=AppColors.SIDEBAR_FRAME,
                fg=AppColors.KU_COLOR,
                padx=15,  # Reduziert von 20 auf 15 für konsistenteres Aussehen
                pady=5,
                cursor="hand2",
                anchor=tk.W
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
                font=Fonts.STANDARD,
                text=prefix + self.selected_option
            )
        
        # Neue Auswahl setzen
        self.selected_option = option
        selected_label = self.nav_labels[option]
        prefix = "» " if self.HasSubmenu(option) else "  "
        selected_label.configure(
            bg=AppColors.HOVER,
            fg=AppColors.KU_COLOR,
            font=Fonts.STANDARD_BOLD,
            text=prefix + option
        )
        
        # Inhalt aktualisieren
        self.content_updater.UpdateContent(option)
        
        # Ereignis protokollieren
        logger.info(f"Navigation: Option '{option}' ausgewählt")