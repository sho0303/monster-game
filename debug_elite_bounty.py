#!/usr/bin/env python3
"""Debug script to test elite bounty progress tracking"""

import tkinter as tk
from gui_main import GameGUI

def test_elite_bounty_progress():
    """Test elite bounty progress tracking"""
    print("🔍 Testing Elite Bounty Progress Tracking...")
    
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    hero = gui.game_state.hero
    
    # Create a test Elite Goblin Thief bounty
    print(f"\n📋 Creating Elite Goblin Thief bounty...")
    
    # Add a bounty manually to test
    test_bounty = {
        'target': 'Elite Goblin Thief',
        'bounty_type': 'elite_boss',
        'target_count': 1,
        'current_count': 0,
        'completed': False,
        'difficulty': 'Gold',
        'reward_gold': 125,
        'reward_item': 'Master Hunter Amulet',
        'status': 'active',
        'description': 'Defeat the Elite Goblin Thief in the grasslands - A legendary Gold ranked threat!'
    }
    
    if 'bounties' not in hero:
        hero['bounties'] = []
    hero['bounties'].append(test_bounty)
    
    print(f"✅ Added bounty: {test_bounty['target']}")
    
    # Test bounty progress with elite encounter
    print(f"\n🗡️  Testing elite encounter progress...")
    monster_killed = "Goblin Thief"
    is_elite_encounter = True
    
    print(f"Monster killed: '{monster_killed}'")
    print(f"Is elite encounter: {is_elite_encounter}")
    
    # Check bounty progress
    progressed = gui.bounty_manager.check_bounty_progress_with_elite(
        hero, monster_killed, is_elite_encounter
    )
    
    print(f"\n📊 Progress Results:")
    print(f"Progressed bounties: {len(progressed)}")
    
    for i, bounty in enumerate(progressed):
        print(f"  {i+1}. {bounty.target} - Progress: {bounty.current_count}/{bounty.target_count}")
        print(f"      Completed: {bounty.completed}")
    
    # Check hero's bounties status
    print(f"\n👤 Hero's bounties after progress:")
    for bounty in hero['bounties']:
        print(f"  Target: '{bounty['target']}'")
        print(f"  Progress: {bounty['current_count']}/{bounty['target_count']}")
        print(f"  Completed: {bounty['completed']}")
        print(f"  Type: {bounty['bounty_type']}")
        print()
    
    # Test with non-elite encounter (should not progress)
    print(f"\n🚫 Testing NON-elite encounter (should not progress)...")
    
    # Reset bounty
    hero['bounties'][0]['current_count'] = 0
    hero['bounties'][0]['completed'] = False
    
    progressed2 = gui.bounty_manager.check_bounty_progress_with_elite(
        hero, monster_killed, False  # is_elite_encounter = False
    )
    
    print(f"Progressed bounties (should be 0): {len(progressed2)}")
    print(f"Bounty completed: {hero['bounties'][0]['completed']}")
    
    root.destroy()

if __name__ == '__main__':
    test_elite_bounty_progress()