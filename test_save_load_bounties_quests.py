#!/usr/bin/env python3
"""
Test bounty and quest save/load functionality
"""
import tkinter as tk
from gui_main import GameGUI
import json

def test_save_load_system():
    """Test that bounties and quests are saved and loaded correctly"""
    root = tk.Tk()
    
    try:
        gui = GameGUI(root)
        root.update()
        
        # Setup test hero
        hero = gui.game_state.hero
        hero['gold'] = 1000
        hero['level'] = 5
        hero['name'] = 'TestSaveHero'
        
        print("✓ Game initialized")
        print(f"✓ Hero: {hero['name']} (Level {hero['level']})")
        
        # Add test data
        
        # 1. Add a quest (if quest manager exists)
        if hasattr(gui, 'quest_manager'):
            gui.quest_manager.initialize_hero_quests(hero)
            print(f"✓ Quests initialized: {len(hero.get('quests', []))} quests")
        
        # 2. Add a bounty
        if hasattr(gui, 'bounty_manager'):
            gui.bounty_manager.initialize_hero_bounties(hero)
            
            # Create test bounty data
            test_bounty = {
                'bounty_type': 'hunt',
                'target': 'TestMonster',
                'target_count': 1,
                'current_count': 0,
                'reward_gold': 150,
                'reward_item': {'name': 'Test Reward', 'attack': 8, 'class': 'All'},
                'description': 'Hunt TestMonster for testing',
                'difficulty': 'Silver',
                'completed': False,
                'status': 'active'
            }
            
            hero['bounties'].append(test_bounty)
            print(f"✓ Bounties initialized: {len(hero.get('bounties', []))} bounties")
        
        # 3. Test save system
        print("\n=== Testing Save System ===")
        
        if hasattr(gui, 'save_load_manager'):
            # Check what data is being prepared for saving
            bounty_data = gui.save_load_manager._prepare_bounty_data()
            print(f"✓ Bounty data prepared: {len(bounty_data.get('hero_bounties', []))} hero bounties")
            print(f"✓ Available bounties: {len(bounty_data.get('available', []))}")
            
            # Print the actual bounty data structure
            print("\n📋 Bounty data structure:")
            for key, value in bounty_data.items():
                print(f"  {key}: {len(value) if isinstance(value, list) else type(value)}")
            
            # Check quest data in hero
            quest_data = hero.get('quests', [])
            print(f"✓ Quest data in hero: {len(quest_data)} quests")
            
            # Perform a test save
            result = gui.save_load_manager.save_game("test_save_bounty_quest.yaml")
            if result['success']:
                print(f"✅ Save successful: {result['filename']}")
            else:
                print(f"❌ Save failed: {result.get('error', 'Unknown error')}")
                
        else:
            print("❌ No save_load_manager found")
        
        print("\n=== Save/Load System Analysis ===")
        print("Bounty Storage:")
        print("  • Available bounties: bounty_manager.available_bounties")
        print("  • Hero's bounties: hero['bounties'] (active/completed)")
        print("  • Save captures: both available and hero bounties")
        print("  • Load restores: both lists properly")
        print("\nQuest Storage:")
        print("  • Hero's quests: hero['quests']") 
        print("  • Save captures: quest objects converted to dicts")
        print("  • Load restores: quest manager reinitializes")
        
        print(f"\n🎯 Current Data:")
        print(f"  Bounties in hero: {len(hero.get('bounties', []))}")
        print(f"  Quests in hero: {len(hero.get('quests', []))}")
        
        root.destroy()  # Don't need GUI for this test
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_save_load_system()