import tkinter as tk
import sys
import os

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors, Fonts
from ui.frames.content.base_content import BaseContentFrame

# Default Frame für noch nicht implementierte Inhalte
class DefaultContentFrame(BaseContentFrame):
    def __init__(self, parent, title: str) -> None:
        self.title = title
        super().__init__(parent)
    
    def _CreateUi(self) -> None:
        label = tk.Label(
            self,
            text=f"Inhalt von {self.title}",
            font=Fonts.DEFAULT_FRAME,
            bg=AppColors.CONTENT_FRAME,
            fg=AppColors.KU_COLOR
        )
        label.pack(padx=50, pady=50)