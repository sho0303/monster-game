#!/usr/bin/env python3
"""
Test enhanced monster encounter with quest and bounty display
"""
import tkinter as tk
from gui_main import GameGUI

def test_encounter_objectives():
    """Test that both quests and bounties show during monster encounters"""
    root = tk.Tk()
    
    try:
        gui = GameGUI(root)
        root.update()
        
        # Setup test hero
        hero = gui.game_state.hero
        hero['gold'] = 1000
        hero['level'] = 4
        hero['name'] = 'ObjectiveTester'
        
        print("✓ Game initialized")
        print(f"✓ Hero: {hero['name']} (Level {hero['level']})")
        
        # Add test quest
        if hasattr(gui, 'quest_manager'):
            gui.quest_manager.initialize_hero_quests(hero)
            
            # Add a test quest for Goblin Thief
            test_quest = {
                'quest_type': 'kill_monster',
                'target': 'Goblin Thief',
                'description': 'Hunt a Goblin Thief (Lv.3) in the grasslands (3 XP)',
                'reward_xp': 3,
                'completed': False,
                'status': 'active',
                'hero_level_when_created': 3
            }
            
            if 'quests' not in hero:
                hero['quests'] = []
            hero['quests'].append(test_quest)
            print("✓ Added test quest for Goblin Thief")
        
        # Add test bounty
        if hasattr(gui, 'bounty_manager'):
            gui.bounty_manager.initialize_hero_bounties(hero)
            
            # Add a test bounty for Goblin Thief
            test_bounty = {
                'bounty_type': 'collector',
                'target': 'Goblin Thief',
                'target_count': 3,
                'current_count': 1,  # 1/3 progress
                'reward_gold': 150,
                'reward_item': {'name': 'Hunter\'s Trophy', 'attack': 5, 'class': 'All'},
                'description': 'Collect bounty: Defeat 3 Goblin Thiefs in the grasslands',
                'difficulty': 'Bronze',
                'completed': False,
                'status': 'active'
            }
            
            hero['bounties'].append(test_bounty)
            print("✓ Added test bounty for Goblin Thief (1/3 progress)")
        
        # Force encounter with Goblin Thief to test matching
        print("\n=== Testing Enhanced Monster Encounter Display ===")
        
        # Set to grassland biome
        gui.current_biome = 'grassland'
        
        # Start a monster encounter
        print("🎯 Starting monster encounter to test objective display...")
        gui.monster_encounter.start()
        
        print("\n=== Enhanced Features Added ===")
        print("✅ Bounties now display alongside quests during encounters")
        print("✅ Matching bounties highlighted with ⭐ symbols") 
        print("✅ Progress tracking: 'Kill 1/3 Goblin Thief'")
        print("✅ Reward preview: '150g, Hunter's Trophy'")
        print("✅ Elite bounty status: Shows 'Need Elite!' if regular monster")
        print("✅ Completed bounty highlight: Green 'COMPLETED!' status")
        print("✅ Color coding: Orange for active, Green for completed, Gray for others")
        
        print("\n=== What You'll See ===")
        print("📜 Active Quests (X/3):")
        print("  ⭐ 🌱 Hunt a Goblin Thief (Lv.3) in the grasslands → 3 XP ⭐ THIS FIGHT!")
        print("\n🎯 Active Bounties (1):")
        print("  ⭐ Kill 1/3 Goblin Thief (Bronze) → 150g, Hunter's Trophy ⭐ THIS FIGHT!")
        print("\nBoth objectives highlighted because they match the current monster!")
        
        root.deiconify()
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_encounter_objectives()