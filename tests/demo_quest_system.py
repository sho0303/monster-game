#!/usr/bin/env python3
"""
Demonstration test of the quest system
"""

import tkinter as tk
from gui_main import GameGUI

def demo_quest_system():
    """Demonstrate the quest system functionality"""
    print("🎮 Monster Game Quest System Demo")
    print("=" * 50)
    print("✨ Features Added:")
    print("  📜 New 'Quests' button in main menu")  
    print("  🎯 Kill monster quests with 10 XP rewards")
    print("  🏆 Quest completion detection during combat")
    print("  📊 Quest status display on main menu")
    print("  💾 Quest data stored in hero object")
    print("\n🎮 How to use:")
    print("  1. Start game and select hero")
    print("  2. Click 'Quests' button to get a quest")
    print("  3. Fight monsters - if you kill the quest target, you get 10 XP!")
    print("  4. Quest automatically completes and clears from your list")
    print("\n" + "=" * 50)
    
    # Test that we can create the GUI without errors
    root = tk.Tk()
    try:
        game_gui = GameGUI(root)
        print("✅ Quest system loaded successfully!")
        print("✅ Ready to play - close the game window when done testing")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    demo_quest_system()