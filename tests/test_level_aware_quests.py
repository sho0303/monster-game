"""
Test level-aware quest system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import tkinter as tk
from gui_main import GameGUI

def test_level_aware_quests():
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Manually initialize game state and hero
    from game_state import initialize_game_state
    gui.game_state = initialize_game_state()
    
    # Select first hero
    first_hero_name = list(gui.game_state.heros.keys())[0]
    gui.game_state.hero = gui.game_state.heros[first_hero_name].copy()
    gui.game_state.hero['name'] = first_hero_name
    gui.game_state.hero['quests'] = []
    
    # Test with hero
    hero = gui.game_state.hero
    hero['level'] = 1
    hero['quests'] = []
    
    print("="*70)
    print("LEVEL-AWARE QUEST SYSTEM TEST")
    print("="*70)
    
    # Test each biome
    biomes = ['grassland', 'desert', 'dungeon', 'ocean']
    
    for level in [1, 3, 5, 7, 10]:
        hero['level'] = level
        hero['quests'] = []
        
        print(f"\n{'='*70}")
        print(f"HERO LEVEL {level} (Can encounter monsters: Level {max(1, level-2)} to {level+1})")
        print('='*70)
        
        for biome in biomes:
            gui.current_biome = biome
            
            print(f"\n{biome.upper()}:")
            
            # Generate 3 quests
            for i in range(3):
                quest = gui.quest_manager.generate_kill_monster_quest()
                
                if quest and not isinstance(quest, str):
                    # Add quest to hero
                    gui.quest_manager.add_quest(hero, quest)
                    
                    # Get monster info
                    monster = gui.game_state.monsters.get(quest.target)
                    if monster:
                        monster_level = monster.get('level', 1)
                        monster_biome = monster.get('biome', 'grassland')
                        
                        # Check if level is appropriate
                        level_ok = (monster_level <= level + 1 and 
                                  monster_level >= max(1, level - 2))
                        biome_ok = monster_biome == biome
                        
                        status = "✓" if (level_ok and biome_ok) else "✗"
                        
                        print(f"  {status} Quest {i+1}: {quest.description}")
                        print(f"     Monster Level: {monster_level}, Biome: {monster_biome}")
                        
                        if not level_ok:
                            print(f"     ⚠️ WARNING: Level {monster_level} is outside range!")
                        if not biome_ok:
                            print(f"     ⚠️ WARNING: Monster in {monster_biome}, quest in {biome}!")
                else:
                    print(f"  - Quest {i+1}: {quest if isinstance(quest, str) else 'None'}")
            
            # Clear quests for next biome
            hero['quests'] = []
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    
    # Don't start mainloop for automated test
    root.destroy()

if __name__ == '__main__':
    test_level_aware_quests()
