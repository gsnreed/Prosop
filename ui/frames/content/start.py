import tkinter as tk
import sys
import os

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors
from ui.frames.content.base_content import BaseContentFrame

class StartseiteFrame(BaseContentFrame):
    """Content-Frame für die Startseite"""
    
    def _CreateUi(self):
        # Header
        header = tk.Label(
            self, 
            text="Willkommen zur Prosopographie der Julisch-Claudischen Kaiserzeit",
            font=('Helvetica', 16, 'bold'),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Beschreibung
        description = tk.Label(
            self,
            text="Hier finden Sie Informationen zu Personen, Orten und Ereignissen der Julisch-Claudischen Epoche.",
            font=('Helvetica', 12),
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR,
            wraplength=600,
            justify='left'
        )
        description.pack(pady=5, padx=20, anchor='w')