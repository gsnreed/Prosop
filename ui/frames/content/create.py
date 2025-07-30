import tkinter as tk
import os
import sys

# Zwei Ebenen nach oben: von ui/frames/content/ → Prosop/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.config import AppColors
from ui.frames.content.base_content import BaseContentFrame
from utils.logger import logger

class CreateFrame(BaseContentFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__current_roman = None