import os
import sys
import tkinter as tk

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from application.app import MainApp
from utils.logger import logger

def main():
    """App start"""
    try:
        app = MainApp()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Unbehandelte Ausnahme: {e}")
        raise

if __name__ == "__main__":
    main()