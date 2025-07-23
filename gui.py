import tkinter as tk
import logging
import time
from datetime import datetime

# --- Logging Setup ---
logging.basicConfig(
    filename='./Log/log.log',
    level=logging.NOTSET,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Farbdefinitionen ---
selectionbar_color = '#eff5f6'
topFrameColor = '#F5E1FD'
sidebarFrameColor = "#EEC6FF"
header_color = '#53366b'
visualisation_frame_color = "#ffffff"
kuColor = '#232F66'
hoverColor = "#D9A7FC"

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Fensterkonfiguration ---
        self.title('Prosop')
        self.geometry("1200x800")
        self.resizable(True, True)
        self.config(bg=selectionbar_color)
        
        # Icon als Instanzattribut speichern
        self.icon = tk.PhotoImage(file='./Pictures/KULogo.png')
        self.iconphoto(True, self.icon)

        # --- Grid Setup für Hauptlayout ---
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        # --- Top Layout ---
        self.topFrame = tk.Frame(self, bg=topFrameColor)
        self.topFrame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Konfiguriere das Grid-Layout im topFrame
        self.topFrame.columnconfigure(0, weight=0)  # Logo-Spalte (feste Größe)
        self.topFrame.columnconfigure(1, weight=1)  # Titel-Spalte (dehnbar)
        self.topFrame.columnconfigure(2, weight=0)  # Uhr-Spalte (feste Größe)

        # Logo links
        self.uniLogo = tk.PhotoImage(file='./Pictures/KU.png').subsample(15)
        logoLabel = tk.Label(self.topFrame, image=self.uniLogo, bg=topFrameColor)
        logoLabel.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        # Titel mittig
        self.titleLabel = tk.Label(self.topFrame,
                                font=('Helvetica', 15, 'bold'),
                                bg=topFrameColor, 
                                fg=kuColor,
                                text='Prosopographie der Julisch-Claudischen Kaiserzeit')
        self.titleLabel.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')

        # Uhrzeit rechts
        self.timeLabel = tk.Label(self.topFrame, 
                                font=('Helvetica', 15),
                                bg=topFrameColor, 
                                fg=kuColor)
        self.timeLabel.grid(row=0, column=2, padx=20, pady=10, sticky='e')
        self.UpdateClock()

        # --- Navigation Layout ---
        self.navigationFrame = tk.Frame(self, bg=sidebarFrameColor)
        self.navigationFrame.grid(row=1, column=0, sticky='nsew')

        self.navigationHeader = tk.Label(self.navigationFrame, 
                                   font=('Helvetica', 15, 'bold'),
                                   bg=sidebarFrameColor, 
                                   fg=kuColor, 
                                   text='Navigation')
        self.navigationHeader.pack(side='top', padx=20, pady=10)

        # Content Frame erstellen
        self.contentFrame = tk.Frame(self, bg=visualisation_frame_color)
        self.contentFrame.grid(row=1, column=1, sticky='nsew')

        self.CreateNavigationOptions()
        
    def UpdateClock(self):
        """Aktualisiert das Zeit-Label mit der aktuellen Uhrzeit"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.timeLabel.config(text=current_time)
        # Aktualisiere die Uhr jede Sekunde
        self.after(1000, self.UpdateClock)

    def CreateNavigationOptions(self):
        options = ['Startseite', 'Ansicht', 'Erstellung', 'Statistik', 'Import', 'Export', 'BibTex', 'Hilfe', 'Impressum']

        self.navLabels = {}
        self.selectedOption = None

        optionsFrame = tk.Frame(self.navigationFrame, bg=sidebarFrameColor)
        optionsFrame.pack(fill=tk.X, pady=2)

        for option in options:
            label = tk.Label(
                optionsFrame,
                text=option,
                font=('Helvetica', 12),
                bg=sidebarFrameColor,
                fg=kuColor,
                padx=20,
                pady=5,
                cursor="hand2",  # Zeigt einen Hand-Cursor beim Hover
                anchor='w'       # Linksbündiger Text
            )
            label.pack(fill=tk.X, pady=2)
            
            # Diese Bindings müssen innerhalb der Schleife sein
            label.bind("<Enter>", lambda e, opt=option: self.OnHover(opt, True))
            label.bind("<Leave>", lambda e, opt=option: self.OnHover(opt, False))
            label.bind("<Button-1>", lambda e, opt=option: self.OnSelect(opt))
            
            # Jedes Label im Dictionary speichern
            self.navLabels[option] = label

        # Nach der Schleife, wenn alle Labels erstellt wurden
        if options:
            self.OnSelect(options[0])

    def OnHover(self, option, isHover):
        label = self.navLabels[option]
        # Nur highlighten wenn nicht ausgewählt
        if option != self.selectedOption:
            if isHover:
                label.configure(bg=hoverColor)  # Hervorgehobene Farbe beim Hovern
            else:
                label.configure(bg=sidebarFrameColor)  # Normale Farbe

    def OnSelect(self, option):
        # Wenn bereits eine Option ausgewählt ist, zurücksetzen
        if self.selectedOption:
            old_label = self.navLabels[self.selectedOption]
            old_label.configure(
                bg = sidebarFrameColor,
                font = ('Helvetica', 12)  # Normale Schrift
            )
        
        # Neue Auswahl setzen
        self.selectedOption = option
        selectedLabel = self.navLabels[option]
        selectedLabel.configure(
            bg = hoverColor,
            font = ('Helvetica', 12, 'bold')  # Fettschrift
        )
        
        # Methodenname angepasst
        self.updateContent(option)
    
    def updateContent(self, option):
        # Lösche bisherigen Inhalt
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        
        # Neuen Inhalt anzeigen
        label = tk.Label(
            self.contentFrame, 
            text = f"Inhalt von {option}", 
            font = ('Helvetica', 18, 'bold'),
            bg = visualisation_frame_color
        )
        label.pack(padx = 50, pady = 50)

if __name__ == '__main__':
    root = MainApp()
    root.mainloop()