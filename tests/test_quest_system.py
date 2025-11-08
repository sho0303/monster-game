#!/usr/bin/env python3
"""
Test the quest system functionality
"""

import tkinter as tk
from gui_main import GameGUI

def test_quest_system():
    """Test the quest system"""
    root = tk.Tk()
    
    try:
        # Create game GUI
        game_gui = GameGUI(root)
        
        # Wait for initialization
        def check_initialization():
            if game_gui.game_state and game_gui.quest_manager:
                print("✅ Quest system initialized successfully")
                
                # Test quest generation
                test_quest = game_gui.quest_manager.generate_kill_monster_quest()
                if test_quest:
                    print(f"✅ Quest generation works: {test_quest.description}")
                else:
                    print("❌ Quest generation failed")
                
                # Close the window
                root.destroy()
            else:
                # Check again in 100ms
                root.after(100, check_initialization)
        
        root.after(100, check_initialization)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error testing quest system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_quest_system()