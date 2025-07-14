import tkinter as tk
import logging

# --- Logging Setup ---
logging.basicConfig(
    filename='log.log',
    level=logging.NOTSET,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Farbdefinitionen ---
selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"

class TkinterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Fensterkonfiguration ---
        self.title('Prosop')
        self.geometry("1100x700")
        self.resizable(True, True)
        self.config(bg=selectionbar_color)

        icon = tk.PhotoImage(file='./KULogo.png')
        self.iconphoto(True, icon)

        # --- Grid Setup für Hauptlayout ---
        self.grid_columnconfigure(0, weight=0)   # Sidebar
        self.grid_columnconfigure(1, weight=10)   # Hauptbereich
        self.grid_rowconfigure(0, weight=0)      # Header
        self.grid_rowconfigure(1, weight=10)     # Main Content

        # --- Sidebar ---
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # --- Branding / Uni Logo ---
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.pack(fill="x", pady=10)

        uni = tk.PhotoImage(file='./KU.png')
        self.uni_logo = uni.subsample(17)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.pack(side="left", padx=10)

        # --- Submenu Frame (Platzhalter) ---
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.pack(fill="both", expand=True, pady=10)

        # --- Header ---
        self.header = tk.Frame(self, bg=header_color, height=80)
        self.header.grid(row=0, column=1, sticky="nsew")
        self.header.grid_propagate(False)

        header_label = tk.Label(
            self.header,
            text="Startseite",
            bg=header_color,
            fg="white",
            font=("Helvetica", 18, "bold")
        )
        header_label.pack(padx=20, pady=20, anchor="w")

        # --- Main Content Area ---
        self.main_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.main_frame.grid(row=1, column=1, sticky="nsew")

        # --- Beispielinhalt im Main Frame ---
        example_label = tk.Label(
            self.main_frame,
            text="Drusilla ist cool!",
            bg=visualisation_frame_color,
            font=("Arial", 14)
        )
        example_label.pack(pady=50)

if __name__ == '__main__':
    root = TkinterApp()
    root.mainloop()
