#!/usr/bin/env python3
"""
Manual test for the quest integration in the monster game
"""

import tkinter as tk
from gui_main import GameGUI

def manual_test():
    """Manual test of quest integration"""
    print("🎮 Starting Monster Game with Quest System...")
    print("Instructions:")
    print("1. Select a hero when prompted")
    print("2. Click 'Quests' in the main menu")
    print("3. Accept a quest")
    print("4. Fight monsters until you complete the quest")
    print("5. Watch for quest completion messages!")
    
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
    except Exception as e:
        print(f"❌ Game error: {e}")

if __name__ == "__main__":
    manual_test()