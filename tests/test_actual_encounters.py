#!/usr/bin/env python3
"""Test actual monster encounters through the GUI system"""

import sys
import os
import tkinter as tk

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_main import GameGUI
import time

def test_explore_encounters():
    """Test actual explore encounters to see if biome restriction works"""
    
    print("Starting GUI test...")
    
    # Create the GUI but don't show it
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create game instance
    gui = GameGUI(root)
    
    # Wait for initialization to complete
    print("Waiting for initialization...")
    root.update()  # Process initial events
    time.sleep(0.1)  # Short delay for async initialization
    root.update()  # Process more events
    
    # Initialize with a hero
    print("Setting up test hero...")
    if gui.game_state is None:
        from game_state import GameState
        gui.game_state = GameState()
    
    gui.game_state.hero = {
        'name': 'Test Hero',
        'age': 25,
        'weapon': 'Test Sword',
        'armour': 'Test Armor',
        'attack': 10,
        'hp': 15,
        'maxhp': 15,
        'defense': 5,
        'class': 'Warrior',
        'level': 1,
        'xp': 0,
        'gold': 100,
        'items': {}
    }
    
    # Test encounters in different biomes
    biomes_to_test = ['grassland', 'ocean', 'desert', 'dungeon']
    
    for biome in biomes_to_test:
        print(f"\n{'='*50}")
        print(f"TESTING BIOME: {biome}")
        print(f"{'='*50}")
        
        # Set the biome
        gui.current_biome = biome
        print(f"Set gui.current_biome = '{biome}'")
        
        # Test multiple encounters
        print(f"\nTesting 5 encounters in {biome}:")
        
        for i in range(5):
            try:
                # Import and create monster encounter
                from gui_monster_encounter import MonsterEncounterGUI
                encounter = MonsterEncounterGUI(gui)
                
                # Get a monster
                result = encounter._select_random_monster()
                
                if result:
                    monster_name, monster_data = result
                    monster_biome = monster_data.get('biome', 'unknown')
                    monster_level = monster_data.get('level', 'unknown')
                    
                    # Check if the biome matches
                    biome_match = "✅" if monster_biome == biome else "❌"
                    print(f"  {i+1}. {monster_name} (level {monster_level}, biome: {monster_biome}) {biome_match}")
                    
                    if monster_biome != biome:
                        print(f"     ⚠️  BIOME MISMATCH! Expected {biome}, got {monster_biome}")
                else:
                    print(f"  {i+1}. No monster returned!")
                    
            except Exception as e:
                print(f"  {i+1}. Error: {e}")
    
    print(f"\n{'='*50}")
    print("Test completed!")
    root.destroy()

if __name__ == '__main__':
    test_explore_encounters()