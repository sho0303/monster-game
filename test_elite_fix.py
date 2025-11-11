#!/usr/bin/env python3
"""Test the elite bounty progress fix"""

import tkinter as tk
from gui_main import GameGUI

def test_elite_bounty_fix():
    """Test that elite bounty progress now works correctly"""
    print("🧪 Testing Elite Bounty Progress Fix")
    print("=" * 40)
    
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    hero = gui.game_state.hero
    
    # Add a test elite bounty
    elite_bounty = {
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
    hero['bounties'].append(elite_bounty)
    
    print(f"✅ Added elite bounty: {elite_bounty['target']}")
    
    # Test 1: Elite encounter (should work)
    print(f"\n🗡️  Test 1: Elite Encounter")
    monster_killed = "Elite Goblin Thief"  # This is what combat system will pass now
    is_elite = True
    
    progressed = gui.bounty_manager.check_bounty_progress_with_elite(
        hero, monster_killed, is_elite
    )
    
    print(f"Monster killed: '{monster_killed}'")
    print(f"Is elite encounter: {is_elite}")
    print(f"Bounties progressed: {len(progressed)}")
    print(f"Bounty completed: {hero['bounties'][0]['completed']}")
    
    # Reset for next test
    hero['bounties'][0]['current_count'] = 0
    hero['bounties'][0]['completed'] = False
    
    # Test 2: Non-elite encounter (should not work)
    print(f"\n🚫 Test 2: Non-Elite Encounter")
    monster_killed = "Goblin Thief"  # Regular monster name
    is_elite = False
    
    progressed2 = gui.bounty_manager.check_bounty_progress_with_elite(
        hero, monster_killed, is_elite
    )
    
    print(f"Monster killed: '{monster_killed}'")
    print(f"Is elite encounter: {is_elite}")
    print(f"Bounties progressed: {len(progressed2)}")
    print(f"Bounty completed: {hero['bounties'][0]['completed']}")
    
    # Test 3: Wrong monster elite encounter (should not work)
    print(f"\n❌ Test 3: Wrong Elite Monster")
    monster_killed = "Elite Wild Boar"  # Different monster
    is_elite = True
    
    progressed3 = gui.bounty_manager.check_bounty_progress_with_elite(
        hero, monster_killed, is_elite
    )
    
    print(f"Monster killed: '{monster_killed}'")
    print(f"Is elite encounter: {is_elite}")
    print(f"Bounties progressed: {len(progressed3)}")
    print(f"Bounty completed: {hero['bounties'][0]['completed']}")
    
    # Summary
    print(f"\n📋 Test Summary:")
    print(f"✅ Elite Goblin Thief + Elite = {len(progressed) > 0}")
    print(f"🚫 Goblin Thief + Non-Elite = {len(progressed2) == 0}")
    print(f"❌ Elite Wild Boar + Elite = {len(progressed3) == 0}")
    
    if len(progressed) > 0 and len(progressed2) == 0 and len(progressed3) == 0:
        print(f"\n🎉 ALL TESTS PASSED! Elite bounty fix works correctly.")
    else:
        print(f"\n💥 SOME TESTS FAILED! Check the logic.")
    
    root.destroy()

if __name__ == '__main__':
    test_elite_bounty_fix()