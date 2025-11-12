#!/usr/bin/env python3
"""
Test script for goblin assault feature
Forces the goblin assault to happen for testing purposes
"""

import tkinter as tk
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from gui_main import GameGUI

def test_goblin_assault():
    """Test the goblin assault feature"""
    root = tk.Tk()
    gui = GameGUI(root)
    
    # Wait for initialization
    root.update()
    time.sleep(0.2)
    root.update()
    
    # Select a hero first (required for initialization)
    # This simulates choosing the first hero
    hero_name = list(gui.game_state.heros.keys())[0]
    gui.game_state.hero = gui.game_state.heros[hero_name].copy()
    
    # Boost the hero stats to ensure survival
    gui.game_state.hero['hp'] = 100
    gui.game_state.hero['maxhp'] = 100
    gui.game_state.hero['attack'] = 15
    gui.game_state.hero['defense'] = 10
    gui.game_state.hero['gold'] = 500
    gui.game_state.hero['level'] = 5
    
    print("Testing Goblin Assault Feature - FULL COMBAT")
    print("=" * 60)
    print("\nThis test will trigger the goblin assault with combat.")
    print("\nFeatures to test:")
    print("  1. Initial assault message with two goblin images")
    print("  2. Two button choices: Save the Town / Run")
    print("  3. If you choose 'Save the Town':")
    print("     - Fight Goblin Raider #1")
    print("     - Fight Goblin Raider #2")
    print("     - Receive Town Savior achievement")
    print("     - Receive 100 gold from the Mayor")
    print("  4. If you choose 'Run':")
    print("     - Return to main menu")
    print("\nStarting test...\n")
    
    # Force the goblin assault by calling it directly
    gui.town._goblin_assault()
    
    print("\n✓ Goblin assault triggered successfully!")
    print("✓ You should see two choices: 'Save the Town' or 'Run'")
    print("✓ Choose 'Save the Town' to fight both goblins!")
    
    root.mainloop()

if __name__ == '__main__':
    test_goblin_assault()
