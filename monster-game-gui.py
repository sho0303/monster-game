"""
PyQuest Monster Game - GUI Launcher
Main entry point for the graphical user interface version
"""
import tkinter as tk
from gui_main import GameGUI

if __name__ == '__main__':
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()
