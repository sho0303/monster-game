#!/usr/bin/env python3
"""
Test that quest rewards use monster XP values instead of fixed 10 XP
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from gui_main import GameGUI

def test_dynamic_quest_rewards():
    """Test that quest rewards match monster XP values"""
    print("🧪 Testing Dynamic Quest Rewards")
    print("Verifying quest rewards use monster XP values")
    print("=" * 50)
    
    root = tk.Tk()
    
    try:
        game_gui = GameGUI(root)
        
        def test_after_init():
            if not (game_gui.game_state and game_gui.quest_manager):
                root.after(100, test_after_init)
                return
            
            print("✅ Game systems initialized")
            
            # Setup hero
            hero_name = list(game_gui.game_state.heros.keys())[0]
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 50
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
            game_gui.quest_manager.initialize_hero_quests(game_gui.game_state.hero)
            
            print(f"✅ Hero initialized: {hero_name}")
            
            # Test multiple quest generations to see different XP rewards
            print("\n🎯 Testing Quest Generation with Monster XP Values:")
            
            quest_count = 5
            for i in range(quest_count):
                quest = game_gui.quest_manager.generate_kill_monster_quest()
                if quest:
                    # Get the actual monster data to compare
                    monster_data = game_gui.game_state.monsters.get(quest.target)
                    if monster_data:
                        monster_xp = monster_data.get('xp', 1)
                        
                        print(f"  Quest {i+1}: {quest.description}")
                        print(f"    Target: {quest.target}")
                        print(f"    Monster XP: {monster_xp}")
                        print(f"    Quest Reward: {quest.reward_xp}")
                        
                        if quest.reward_xp == monster_xp:
                            print(f"    ✅ Reward matches monster XP!")
                        else:
                            print(f"    ❌ Reward mismatch! Expected {monster_xp}, got {quest.reward_xp}")
                        print()
            
            # Test quest completion with dynamic XP
            print("🏆 Testing Quest Completion with Dynamic XP:")
            
            # Generate a quest and complete it
            test_quest = game_gui.quest_manager.generate_kill_monster_quest()
            if test_quest:
                game_gui.quest_manager.add_quest(game_gui.game_state.hero, test_quest)
                
                original_xp = game_gui.game_state.hero['xp']
                print(f"  Hero XP before: {original_xp}")
                print(f"  Quest target: {test_quest.target}")
                print(f"  Quest reward: {test_quest.reward_xp} XP")
                
                # Complete the quest
                completed = game_gui.quest_manager.check_quest_completion(
                    game_gui.game_state.hero, test_quest.target
                )
                
                final_xp = game_gui.game_state.hero['xp']
                xp_gained = final_xp - original_xp
                
                print(f"  Hero XP after: {final_xp}")
                print(f"  XP gained: {xp_gained}")
                
                if completed and xp_gained == test_quest.reward_xp:
                    print(f"  ✅ Quest completion XP matches expected reward!")
                else:
                    print(f"  ❌ XP mismatch on completion!")
            
            print("\n🏆 Dynamic quest reward testing completed!")
            root.destroy()
        
        root.after(500, test_after_init)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_monster_xp_values():
    """Show some example monster XP values for reference"""
    print("\n📊 Sample Monster XP Values:")
    print("=" * 30)
    
    root = tk.Tk()
    
    try:
        game_gui = GameGUI(root)
        
        def show_monster_xp():
            if not game_gui.game_state:
                root.after(100, show_monster_xp)
                return
            
            # Show XP values for first few monsters
            monsters = game_gui.game_state.monsters
            monster_list = list(monsters.items())[:8]  # Show first 8
            
            for name, data in monster_list:
                xp = data.get('xp', 1)
                level = data.get('level', 1)
                print(f"  {name}: {xp} XP (Level {level})")
            
            print("\n✅ Now quest rewards will match these XP values!")
            root.destroy()
        
        root.after(500, show_monster_xp)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to show monster XP: {e}")

if __name__ == "__main__":
    test_monster_xp_values()
    test_dynamic_quest_rewards()