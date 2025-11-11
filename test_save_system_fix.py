#!/usr/bin/env python3
"""
Test save system to ensure no more attribute errors
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_save_system():
    """Test the save system to ensure it works without errors"""
    root = tk.Tk()
    root.title("Save System Test")
    
    gui = GameGUI(root)
    
    def run_test():
        if not hasattr(gui, 'save_load_manager') or gui.save_load_manager is None:
            root.after(500, run_test)
            return
        
        print("🧪 SAVE SYSTEM FIX TEST")
        print("="*40)
        
        # Set up test game state
        gui.game_state = initialize_game_state()
        gui.game_state.hero = {
            'name': 'Save Test Hero',
            'hp': 20,
            'maxhp': 20,
            'attack': 15,
            'defense': 10,
            'level': 3,
            'class': 'Warrior',
            'weapon': 'Test Sword',
            'armour': 'Test Armor',
            'age': 25,
            'gold': 100,
            'xp': 150,
            'lives_left': 3,
            'quests': [],
            'items': {}
        }
        
        print(f"🧙 Test Hero: {gui.game_state.hero['name']} (Level {gui.game_state.hero['level']})")
        
        # Test save system
        print("💾 Testing save system...")
        try:
            # Test the preparation methods individually
            print("  - Testing hero data preparation...")
            hero_data = gui.save_load_manager._prepare_hero_data(gui.game_state.hero)
            print("    ✅ Hero data prepared successfully")
            
            print("  - Testing achievement data preparation...")
            achievement_data = gui.save_load_manager._prepare_achievement_data()
            print("    ✅ Achievement data prepared successfully")
            
            print("  - Testing bounty data preparation...")
            bounty_data = gui.save_load_manager._prepare_bounty_data()
            print("    ✅ Bounty data prepared successfully")
            
            print("  - Testing full save operation...")
            result = gui.save_load_manager.save_game(gui.game_state.hero, 'grassland', 'test_save')
            
            if result['success']:
                print("    ✅ SAVE SUCCESSFUL!")
                print(f"    📁 File: {result['filename']}")
            else:
                print(f"    ❌ SAVE FAILED: {result['error']}")
                
        except Exception as e:
            print(f"    ❌ SAVE ERROR: {e}")
        
        print("\n🎯 TEST COMPLETE")
        print("If you see ✅ for all steps, the save system is fixed!")
        print("Close this window to finish the test.")
    
    root.after(1000, run_test)
    root.mainloop()

if __name__ == '__main__':
    test_save_system()