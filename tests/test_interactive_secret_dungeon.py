#!/usr/bin/env python3
"""
Test the interactive secret dungeon discovery system
"""
import sys
import os
import tkinter as tk

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from gui_main import GameGUI

def test_interactive_secret_dungeon():
    """Test the new interactive secret dungeon discovery"""
    
    print("🎭 Testing Interactive Secret Dungeon Discovery")
    print("=" * 60)
    
    root = tk.Tk()
    gui = GameGUI(root)
    
    # Wait for initialization
    print("⏳ Initializing game...")
    while gui.game_state is None or gui.town is None:
        root.update()
        
    print("✅ Game initialized")
    
    # Set up test hero
    gui.game_state.hero = {
        'name': 'Story Tester',
        'age': 30,
        'weapon': 'Test Sword',
        'armour': 'Test Armor',
        'attack': 15,
        'hp': 50,
        'maxhp': 50,
        'defense': 12,
        'class': 'Warrior',
        'level': 8,
        'xp': 0,
        'gold': 500,
        'lives_left': 3,
        'items': {},
        'beers_consumed': 3  # Enough to trigger discovery
    }
    
    hero = gui.game_state.hero
    print(f"🧙 Test Hero: {hero['name']} (Lv.{hero['level']}, {hero['beers_consumed']} beers consumed)")
    
    # Manually trigger the secret dungeon story
    print("\n🍺 Triggering Secret Dungeon Discovery Story...")
    
    gui.current_biome = 'town'
    gui.town._show_secret_dungeon_story()
    
    print("\n✅ Interactive Secret Dungeon Story Activated!")
    print("📋 Features Available:")
    print("   ✅ Full story with immersive dialogue")
    print("   ✅ Quest acceptance buttons")
    print("   ✅ Option to ask more questions")
    print("   ✅ Option to decline and try again later")
    print("   ✅ Detailed information about risks and rewards")
    print("\n🎮 Use the buttons in the GUI to interact with the story!")
    
    # Let the user interact with the GUI
    root.mainloop()

if __name__ == '__main__':
    test_interactive_secret_dungeon()