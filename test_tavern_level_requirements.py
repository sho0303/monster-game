#!/usr/bin/env python3
"""
Test tavern quest level requirements
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_tavern_level_requirements():
    """Test that tavern quests show proper level requirements and restrictions"""
    root = tk.Tk()
    root.title("Tavern Quest Level Requirements Test")
    
    gui = GameGUI(root)
    
    def run_test():
        if not hasattr(gui, 'game_state') or gui.game_state is None:
            root.after(500, run_test)
            return
        
        print("🧪 TAVERN QUEST LEVEL REQUIREMENTS TEST")
        print("="*50)
        
        # Test with level 2 hero (like user's situation)
        gui.game_state.hero = {
            'name': 'Level 2 Hero',
            'hp': 25,
            'maxhp': 25,
            'attack': 12,
            'defense': 8,
            'level': 2,  # Level 2 - can only access grassland
            'class': 'Warrior',
            'weapon': 'Iron Sword',
            'armour': 'Leather Armor',
            'age': 20,
            'gold': 50,
            'quests': []
        }
        
        print(f"🧙 Test Hero Level: {gui.game_state.hero['level']}")
        print()
        print("🎯 BIOME ACCESS LEVELS:")
        print("   Grassland: Level 1+")
        print("   Desert: Level 3+")
        print("   Ocean: Level 5+")
        print("   Dungeons: Level 7+")
        print()
        
        # Test biome access checking
        biomes_to_test = ['grassland', 'desert', 'ocean', 'dungeon']
        
        print("🧪 Testing biome access for Level 2 hero:")
        for biome in biomes_to_test:
            can_access = gui.town._can_access_biome(biome)
            status = "✅ ACCESSIBLE" if can_access else "❌ BLOCKED"
            print(f"   {biome.title()}: {status}")
        
        print()
        print("🎮 MANUAL TEST:")
        print("   1. Visit the tavern")
        print("   2. Look for NPCs offering quests")
        print("   3. Try to accept quests for different biomes")
        print("   4. Level 2 should be blocked from desert/ocean/dungeon quests")
        print("   5. Quest descriptions should show level requirements")
        
        # Open town for manual testing
        root.after(2000, gui.town.enter_town)
    
    root.after(1000, run_test)
    root.mainloop()

if __name__ == '__main__':
    test_tavern_level_requirements()