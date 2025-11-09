#!/usr/bin/env python3
"""Test script to investigate the biome monster selection bug"""

import sys
import os
import yaml

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from gui_monster_encounter import MonsterEncounterGUI

def load_monsters():
    """Load all monsters from YAML files"""
    monsters = {}
    monsters_dir = 'monsters'
    
    if os.path.exists(monsters_dir):
        for filename in os.listdir(monsters_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                filepath = os.path.join(monsters_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        monster_data = yaml.safe_load(file)
                        if monster_data:
                            monsters.update(monster_data)
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    
    return monsters

def test_monster_selection_by_biome():
    """Test monster selection for each biome"""
    
    # Load monsters
    monsters = load_monsters()
    print(f"Loaded {len(monsters)} monsters total")
    
    # Group monsters by biome
    biomes = {}
    for name, data in monsters.items():
        biome = data.get('biome', 'grassland')
        if biome not in biomes:
            biomes[biome] = []
        biomes[biome].append((name, data))
    
    print(f"\nMonsters by biome:")
    for biome, monster_list in sorted(biomes.items()):
        print(f"\n{biome}:")
        for name, data in sorted(monster_list):
            level = data.get('level', 1)
            print(f"  {name}: level {level}")
    
    # Test monster selection for different hero levels and biomes
    print(f"\n{'='*50}")
    print("TESTING MONSTER SELECTION")
    print(f"{'='*50}")
    
    # Create a mock GUI with game state
    class MockGUI:
        def __init__(self):
            self.game_state = GameState()
            self.game_state.monsters = monsters
            self.current_biome = 'grassland'
    
    # Test different scenarios
    test_cases = [
        {'hero_level': 1, 'biome': 'grassland'},
        {'hero_level': 1, 'biome': 'ocean'},
        {'hero_level': 5, 'biome': 'grassland'},
        {'hero_level': 5, 'biome': 'ocean'},
        {'hero_level': 10, 'biome': 'grassland'},
        {'hero_level': 10, 'biome': 'ocean'},
        {'hero_level': 1, 'biome': 'desert'},
        {'hero_level': 5, 'biome': 'desert'},
        {'hero_level': 10, 'biome': 'desert'},
    ]
    
    for test_case in test_cases:
        print(f"\n--- Testing Hero Level {test_case['hero_level']}, Biome: {test_case['biome']} ---")
        
        mock_gui = MockGUI()
        mock_gui.current_biome = test_case['biome']
        mock_gui.game_state.hero = {'level': test_case['hero_level']}
        
        # Create monster encounter instance
        encounter = MonsterEncounterGUI(mock_gui)
        
        # Test monster selection multiple times
        selections = []
        for i in range(5):
            result = encounter._select_random_monster()
            if result:
                monster_name, monster_data = result
                selections.append((monster_name, monster_data['level'], monster_data.get('biome', 'grassland')))
        
        print(f"Selected monsters:")
        for monster_name, monster_level, monster_biome in selections:
            correct_biome = "✅" if monster_biome == test_case['biome'] else "❌"
            print(f"  {monster_name} (level {monster_level}, biome: {monster_biome}) {correct_biome}")

if __name__ == '__main__':
    test_monster_selection_by_biome()