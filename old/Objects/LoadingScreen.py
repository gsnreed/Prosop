import tkinter as tk
from tkinter import ttk

class LoadingScreen(tk.Toplevel):
    def __init__(self, parent, message="Bitte warten..."):
        super().__init__(parent)
        self.title("Wird geladen")
        self.geometry("300x100")
        self.resizable(False, False)
        self.transient(parent)  # Dialog dem Hauptfenster unterordnen
        
        # Verhindern, dass der Fenster geschlossen wird
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Positionierung in der Mitte des Elternfensters
        x = parent.winfo_x() + parent.winfo_width() // 2 - 150
        y = parent.winfo_y() + parent.winfo_height() // 2 - 50
        self.geometry(f"+{x}+{y}")
        
        # Nachricht
        tk.Label(self, text=message, font=("Helvetica", 12)).pack(pady=(15, 10))
        
        # Fortschrittsbalken
        self.progress = ttk.Progressbar(self, mode='indeterminate', length=250)
        self.progress.pack(pady=10)
        
        # Start der Animation
        self.progress.start()
        
        # Immer im Vordergrund (wichtig!)
        self.attributes("-topmost", True)
        
        # Modal machen (blockiert Eingaben im Hauptfenster)
        self.grab_set()
        
        # Diese Aufrufe sind wichtig, um sicherzustellen,
        # dass das Fenster angezeigt wird
        self.deiconify()
        self.lift()
        self.focus_force()
        
        # Aktualisierung des Dialogfensters erzwingen
        self.update()

    def finish(self):
        """Schließt den Ladebildschirm"""
        try:
            self.grab_release()  # Wichtig: Grab freigeben
            self.progress.stop()
            self.destroy()
        except:
            pass