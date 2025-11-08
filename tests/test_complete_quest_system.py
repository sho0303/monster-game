#!/usr/bin/env python3
"""
Test the complete quest system functionality
"""

import tkinter as tk
from gui_main import GameGUI

def test_complete_quest_system():
    """Test the complete quest system"""
    root = tk.Tk()
    
    try:
        # Create game GUI
        game_gui = GameGUI(root)
        
        def test_after_init():
            if not (game_gui.game_state and game_gui.quest_manager):
                root.after(100, test_after_init)
                return
                
            print("🧪 Testing Quest System...")
            
            # Select first hero
            hero_name = list(game_gui.game_state.heros.keys())[0]
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 50
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
            game_gui.quest_manager.initialize_hero_quests(game_gui.game_state.hero)
            
            print(f"✅ Hero selected: {hero_name}")
            
            # Test quest generation
            quest1 = game_gui.quest_manager.generate_kill_monster_quest()
            if quest1:
                print(f"✅ Quest 1 generated: {quest1.description}")
                game_gui.quest_manager.add_quest(game_gui.game_state.hero, quest1)
                print(f"✅ Quest 1 added to hero")
            
            # Test another quest
            quest2 = game_gui.quest_manager.generate_kill_monster_quest()
            if quest2:
                print(f"✅ Quest 2 generated: {quest2.description}")
                game_gui.quest_manager.add_quest(game_gui.game_state.hero, quest2)
            
            # Show active quests
            active_quests = game_gui.quest_manager.get_active_quests(game_gui.game_state.hero)
            print(f"✅ Active quests: {len(active_quests)}")
            
            for i, quest in enumerate(active_quests, 1):
                print(f"   {i}. {quest.description} (Target: {quest.target}, Reward: {quest.reward_xp} XP)")
            
            # Test quest completion
            if active_quests:
                test_monster_name = active_quests[0].target
                print(f"🎯 Testing quest completion for: {test_monster_name}")
                
                completed = game_gui.quest_manager.check_quest_completion(
                    game_gui.game_state.hero, test_monster_name
                )
                
                if completed:
                    print(f"✅ Quest completed! Rewards given.")
                    print(f"   Hero XP: {game_gui.game_state.hero['xp']}")
                    
                    # Clean up completed quests
                    game_gui.quest_manager.clear_completed_quests(game_gui.game_state.hero)
                    
                    remaining_quests = game_gui.quest_manager.get_active_quests(game_gui.game_state.hero)
                    print(f"✅ Remaining active quests: {len(remaining_quests)}")
            
            print("🏆 Quest system test completed successfully!")
            root.destroy()
        
        root.after(100, test_after_init)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error testing quest system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_quest_system()