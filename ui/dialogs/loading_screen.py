import tkinter as tk
from tkinter import ttk
import sys
import os

# Zwei Ebenen nach oben (von /ui/dialogs/ zu Projekt-Root /Prosop/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import Fonts

class LoadingScreen(tk.Toplevel):
    """Ladescreen Implementierung"""
    def __init__(self, parent, message="Bitte warten..."):
        super().__init__(parent)
        self.title("Wird geladen")
        self.geometry("300x100")
        self.resizable(False, False)
        self.transient(parent)  # Dialog dem Hauptfenster unterordnen
        
        # Verhindern, dass das Fenster geschlossen wird
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Positionierung in der Mitte des Fensters
        x = parent.winfo_x() + parent.winfo_width() // 2 - 150
        y = parent.winfo_y() + parent.winfo_height() // 2 - 50
        self.geometry(f"+{x}+{y}")
        
        # Nachricht
        tk.Label(self, text=message, font=Fonts.LOADING_SCREEN).pack(pady=(15, 10))
        
        # Fortschrittsbalken
        self.progress = ttk.Progressbar(self, mode='indeterminate', length=250)
        self.progress.pack(pady=10)
        
        # Start der Animation
        self.progress.start()
        
        # Immer im Vordergrund
        self.attributes("-topmost", True)
        
        # Eingaben im Hauptfenster blockieren
        self.grab_set()
        
        # Fenster anzeigen
        self.deiconify()
        self.lift()
        self.focus_force()
        
        # Aktualisierung des Dialogfensters erzwingen
        self.update()

    def Finish(self):
        """Schließt den Ladebildschirm"""
        try:
            # Fenster freigeben
            self.grab_release()
            self.progress.stop()
            self.destroy()
        except:
            pass