#!/usr/bin/env python3
"""
Test main menu display to ensure no debug output appears
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_main_menu_display():
    """Test that main menu only shows user-friendly stats, not debug data"""
    root = tk.Tk()
    root.title("Main Menu Display Test")
    
    gui = GameGUI(root)
    
    def run_test():
        if not hasattr(gui, 'game_state') or gui.game_state is None:
            root.after(500, run_test)
            return
        
        print("🧪 MAIN MENU DISPLAY TEST")
        print("="*40)
        
        # Set up test hero with debug fields
        gui.game_state.hero = {
            'name': 'Test Hero',
            'hp': 20,
            'maxhp': 20,
            'attack': 15,
            'defense': 10,
            'level': 3,
            'xp': 12,
            'class': 'Warrior',
            'weapon': 'Test Sword',
            'armour': 'Test Armor',
            'age': 25,
            'gold': 100,
            'lives_left': 3,
            'item': None,
            'items': {},
            'quests': [],  # This should NOT appear in main menu
            'quests_completed_by_level': {},  # This should NOT appear
            'bounties': [{'test': 'data'}]  # This should NOT appear
        }
        
        print(f"🧙 Test Hero: {gui.game_state.hero['name']} (Level {gui.game_state.hero['level']})")
        print()
        print("🧪 Testing main menu display...")
        print("   - Should show only user-friendly stats")
        print("   - Should NOT show: quests, quests_completed_by_level, bounties")
        print()
        
        # Display the main menu
        gui.main_menu()
        
        print("✅ Main menu displayed")
        print("Check the game window - it should show clean hero stats")
        print("without debug fields like 'quests_completed_by_level' or 'bounties'")
        print("\nClose window when done reviewing.")
    
    root.after(1000, run_test)
    root.mainloop()

if __name__ == '__main__':
    test_main_menu_display()