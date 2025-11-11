#!/usr/bin/env python3
"""
Test achievement tracking methods to ensure no more missing methods
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_achievement_methods():
    """Test all achievement tracking methods to ensure they exist and work"""
    root = tk.Tk()
    root.title("Achievement Methods Test")
    
    gui = GameGUI(root)
    
    def run_test():
        if not hasattr(gui, 'achievement_manager') or gui.achievement_manager is None:
            root.after(500, run_test)
            return
        
        print("🧪 ACHIEVEMENT METHODS COMPATIBILITY TEST")
        print("="*50)
        
        # Test all achievement tracking methods
        methods_to_test = [
            ('track_combat_win', []),
            ('track_monster_kill', ['Test Monster']),
            ('track_combat_loss', []),
            ('track_death', []),
            ('track_blacksmith_visit', []),
            ('track_side_quest_completion', []),
            ('track_gold_earned', [100]),
            ('track_bounty_completion', []),
            ('track_fountain_use', []),
            ('track_beer_consumption', []),
            ('track_level_gain', [5]),
            ('track_quest_completion', []),
            ('track_biome_visit', ['grassland']),
            ('track_secret_dungeon_discovery', []),
            ('track_tavern_npc_encounter', ['merchant']),
            ('track_monster_defeat', ['Goblin']),
        ]
        
        success_count = 0
        total_count = len(methods_to_test)
        
        for method_name, args in methods_to_test:
            try:
                method = getattr(gui.achievement_manager, method_name)
                method(*args)
                print(f"✅ {method_name}: SUCCESS")
                success_count += 1
            except AttributeError as e:
                print(f"❌ {method_name}: MISSING METHOD - {e}")
            except Exception as e:
                print(f"⚠️  {method_name}: ERROR - {e}")
        
        print(f"\n🎯 RESULTS: {success_count}/{total_count} methods working")
        
        if success_count == total_count:
            print("✅ ALL ACHIEVEMENT METHODS WORKING!")
            print("Combat system should now work without errors.")
        else:
            print("❌ Some methods still missing or broken.")
        
        print("\nClose this window to finish the test.")
    
    root.after(1000, run_test)
    root.mainloop()

if __name__ == '__main__':
    test_achievement_methods()