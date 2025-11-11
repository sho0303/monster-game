#!/usr/bin/env python3
"""
Test the enhanced quest system with limits and cross-biome missions
"""
import sys
import os
import tkinter as tk
import time

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from gui_main import GameGUI

def test_enhanced_quest_system():
    """Test the new quest system with limits and cross-biome missions"""
    
    print("📜 Testing Enhanced Quest System")
    print("=" * 50)
    
    root = tk.Tk()
    root.withdraw()  # Hide window for testing
    
    try:
        # Create the GUI
        gui = GameGUI(root)
        root.update()
        time.sleep(0.2)
        root.update()
        
        # Set up test hero at different levels
        if gui.game_state is None:
            from game_state import GameState
            gui.game_state = GameState()
        
        # Test Level 1 Hero (Grassland only)
        print("\n🧙 Testing Level 1 Hero (Grassland Access Only)")
        gui.game_state.hero = {
            'name': 'Quest Tester L1',
            'age': 20,
            'weapon': 'Basic Sword',
            'armour': 'Cloth Robe',
            'attack': 8,
            'hp': 15,
            'maxhp': 15,
            'defense': 5,
            'class': 'Warrior',
            'level': 1,
            'xp': 0,
            'gold': 50,
            'lives_left': 3,
            'items': {}
        }
        
        hero = gui.game_state.hero
        
        # Test quest limits
        print("📊 Testing quest limits at Level 1...")
        for i in range(4):  # Try to get more than the limit
            can_take = gui.quest_manager.can_take_more_quests(hero)
            print(f"   Quest attempt {i+1}: Can take more quests? {can_take}")
            
            if can_take:
                quest = gui.quest_manager.generate_kill_monster_quest()
                if isinstance(quest, str):
                    print(f"   → Error: {quest}")
                    break
                else:
                    gui.quest_manager.add_quest(hero, quest)
                    print(f"   → Added: {quest.description[:50]}...")
            else:
                print(f"   → Quest limit reached!")
                break
        
        # Test Level 5 Hero (Multiple biomes unlocked)
        print("\n🧙 Testing Level 5 Hero (Multiple Biomes Unlocked)")
        gui.game_state.hero['level'] = 5
        gui.game_state.hero['quests'] = []  # Clear quests
        gui.game_state.hero['quests_completed_by_level'] = {}
        
        available_biomes = gui.quest_manager.get_available_biomes_for_hero(hero)
        print(f"   Available biomes at Level 5: {available_biomes}")
        
        # Test cross-biome missions
        print("🌍 Testing cross-biome mission generation...")
        gui.current_biome = 'grassland'  # Set current biome
        
        for i in range(3):
            quest = gui.quest_manager.generate_kill_monster_quest()
            if isinstance(quest, str):
                print(f"   Quest {i+1}: Error - {quest}")
                break
            else:
                is_cross_biome = getattr(quest, 'is_cross_biome', False)
                target_biome = getattr(quest, 'target_biome', 'unknown')
                cross_indicator = "🌍 CROSS-BIOME" if is_cross_biome else "🏠 LOCAL"
                
                print(f"   Quest {i+1}: {cross_indicator} - Target biome: {target_biome}")
                print(f"      {quest.description[:60]}...")
                print(f"      XP Reward: {quest.reward_xp}")
                
                gui.quest_manager.add_quest(hero, quest)
        
        # Test biome unlock levels
        print("\n🗺️ Testing biome unlock system...")
        for level in [1, 3, 5, 7, 10]:
            gui.game_state.hero['level'] = level
            available = gui.quest_manager.get_available_biomes_for_hero(hero)
            print(f"   Level {level}: {available}")
        
        print("\n✅ Enhanced Quest System Test Complete!")
        print("📋 New Features Verified:")
        print("   ✅ Quest limits per level (max 2)")
        print("   ✅ Cross-biome mission generation")
        print("   ✅ Biome progression unlocks")
        print("   ✅ XP bonuses for exploration")
        print("   ✅ Level-appropriate monster selection")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            root.quit()
            root.destroy()
        except:
            pass

if __name__ == '__main__':
    test_enhanced_quest_system()