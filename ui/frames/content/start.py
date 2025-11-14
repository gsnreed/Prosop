import tkinter as tk
import sys
import os
from PIL import Image, ImageTk

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors, Fonts
from ui.frames.content.base_content import BaseContentFrame

class StartseiteFrame(BaseContentFrame):
    """Content-Frame für die Startseite"""
    def __init__(self, parent):
        super().__init__(parent)
        self.CreateUi()
    
    def CreateUi(self):
        # Header
        header = tk.Label(
            self, 
            text="Willkommen zur grafischen Oberfläche zur Bearbeitung des prosopografischen Katalogs",
            font=Fonts.HEADER,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor=tk.W)
        
        # Beschreibung
        # Beschreibung - Haupttext
        main_description = tk.Label(
            self,
            text="Dieses innovative Tool ermöglicht eine benutzerfreundliche Verwaltung und Visualisierung von Daten zu Frauen an den römischen Kaiserhöfen im 1. Jahrhundert n. Chr.\n\n" \
                "Nutzen Sie die Navigation links, um verschiedene Ansichten und Funktionen zu erkunden.",
            font=Fonts.STANDARD,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        main_description.pack(pady=(5, 10), padx=20, anchor=tk.W)

        # Überschrift 1 - Fett
        heading1 = tk.Label(
            self,
            text="FORSCHUNGSRELEVANZ UND INNOVATION:",
            font=(Fonts.STANDARD[0], Fonts.STANDARD[1], "bold"),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        heading1.pack(pady=(0, 2), padx=20, anchor=tk.W)

        # Text 1 - Normal
        text1 = tk.Label(
            self,
            text="Das Projekt verbindet historische Forschung mit moderner Datenanalyse und schafft neue Möglichkeiten für die systematische Erforschung von Frauen in der Antike. Durch den interdisziplinären Ansatz werden bisher schwer zugängliche historische Zusammenhänge sichtbar gemacht.",
            font=Fonts.STANDARD,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        text1.pack(pady=(0, 10), padx=20, anchor=tk.W)

        # Überschrift 2 - Fett
        heading2 = tk.Label(
            self,
            text="TECHNISCHE FEATURES:",
            font=(Fonts.STANDARD[0], Fonts.STANDARD[1], "bold"),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        heading2.pack(pady=(0, 2), padx=20, anchor=tk.W)

        # Text 2 - Normal
        text2 = tk.Label(
            self,
            text="Die Datenbank wird in Form einer JSON-Datei gespeichert, die Sie bei Bedarf auch in anderen Formaten exportieren oder importieren können. Damit wird es möglich, völlig automatisiert wissenschaftliche Texte zu sämtlichen Frauen zu generieren (z. B. in LaTeX).",
            font=Fonts.STANDARD,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        text2.pack(pady=(0, 10), padx=20, anchor=tk.W)

        # Überschrift 3 - Fett
        heading3 = tk.Label(
            self,
            text="EFFIZIENZGEWINN FÜR DIE FORSCHUNG:",
            font=(Fonts.STANDARD[0], Fonts.STANDARD[1], "bold"),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        heading3.pack(pady=(0, 2), padx=20, anchor=tk.W)

        # Text 3 - Normal
        text3 = tk.Label(
            self,
            text="Das Tool ermöglicht eine erhebliche Zeitersparnis bei der Datenauswertung und Textgenerierung, wodurch mehr Kapazitäten für die inhaltliche Analyse und Interpretation zur Verfügung stehen. Die systematische Datenerfassung schafft zudem die Grundlage für weiterführende Forschungsprojekte.",
            font=Fonts.STANDARD,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        text3.pack(pady=(0, 10), padx=20, anchor=tk.W)

        # Abschluss
        final_text = tk.Label(
            self,
            text="Viel Erfolg bei Ihrer Arbeit!",
            font=Fonts.STANDARD,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=1200,
            justify=tk.LEFT
        )
        final_text.pack(pady=(0, 5), padx=20, anchor=tk.W)

        try:
            # Bild laden und skalieren
            pil_image = Image.open("Konvertierung.png")
            pil_image = pil_image.resize((400, 300), Image.Resampling.LANCZOS)  # Größe anpassen
            photo = ImageTk.PhotoImage(pil_image)
            
            # Bild-Label erstellen
            image_label = tk.Label(
                self,
                image=photo,
                bg=AppColors.CONTENT_FRAME
            )
            image_label.image = photo  # Referenz behalten
            image_label.pack(pady=20, padx=20)
            
        except Exception as e:
            print(f"Bild konnte nicht geladen werden: {e}")