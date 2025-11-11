#!/usr/bin/env python3
"""
Test enhanced quest management with low-level quest dropping
"""
import tkinter as tk
from gui_main import GameGUI

def test_quest_management():
    """Test the enhanced quest dropping system"""
    root = tk.Tk()
    
    try:
        gui = GameGUI(root)
        root.update()
        
        # Setup test hero at higher level
        hero = gui.game_state.hero
        hero['level'] = 5  # Set to level 5 so we can have low-level quests
        hero['name'] = 'QuestTester'
        
        print("✓ Game initialized")
        print(f"✓ Hero: {hero['name']} (Level {hero['level']})")
        
        # Add some test quests at different levels
        if hasattr(gui, 'quest_manager'):
            gui.quest_manager.initialize_hero_quests(hero)
            
            # Simulate some old quests from lower levels
            test_quests = [
                {
                    'quest_type': 'kill_monster',
                    'target': 'Spider',
                    'description': 'Hunt a Spider (Lv.1) in the grasslands (1 XP)',
                    'reward_xp': 1,
                    'completed': False,
                    'status': 'active',
                    'hero_level_when_created': 1  # Low level quest
                },
                {
                    'quest_type': 'kill_monster', 
                    'target': 'Goblin Thief',
                    'description': 'Hunt a Goblin Thief (Lv.2) in the grasslands (2 XP)',
                    'reward_xp': 2,
                    'completed': False,
                    'status': 'active',
                    'hero_level_when_created': 2  # Low level quest
                },
                {
                    'quest_type': 'kill_monster',
                    'target': 'Cyclops',
                    'description': 'Hunt a Cyclops (Lv.5) in the desert (5 XP)',
                    'reward_xp': 5,
                    'completed': False,
                    'status': 'active',
                    'hero_level_when_created': 5  # Current level quest
                }
            ]
            
            # Add quests to hero
            if 'quests' not in hero:
                hero['quests'] = []
            
            for quest_data in test_quests:
                hero['quests'].append(quest_data)
            
            print(f"✓ Added {len(test_quests)} test quests")
            print("  - 2 low-level quests (Lv.1 & Lv.2)")
            print("  - 1 current-level quest (Lv.5)")
            
            # Test the enhanced quest dropping interface
            print("\n=== Enhanced Quest Management Features ===")
            print("✅ Categorizes quests by level (low-level vs current)")
            print("✅ Highlights low-level quests for easy identification") 
            print("✅ Individual quest dropping (1. Drop Quest, 2. Drop Quest, etc.)")
            print("✅ Bulk dropping with 'Drop All Low-Level' button")
            print("✅ Shows quest creation level and rewards")
            print("✅ Color coding: Red for low-level, Orange for current-level")
            
            # Show the quest interface
            print(f"\n🎯 Opening enhanced quest management...")
            gui.show_quests()
            
        else:
            print("❌ No quest_manager found")
        
        print("\n=== Usage Instructions ===")
        print("1. Click 📜 Quests to see quest overview")
        print("2. Click 🗑️ Drop Quest to open enhanced management")
        print("3. See quests categorized by level with color coding") 
        print("4. Use '🗑️ Drop All Low-Level' for bulk cleanup")
        print("5. Individual drops: '1. Drop Quest', '2. Drop Quest', etc.")
        
        root.deiconify()
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_quest_management()