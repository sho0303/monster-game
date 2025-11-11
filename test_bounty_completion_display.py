#!/usr/bin/env python3
"""Test the improved bounty completion display"""

import tkinter as tk
from gui_main import GameGUI

def test_bounty_completion_display():
    """Test that bounty completion status is properly displayed"""
    print("🧪 Testing Bounty Completion Display")
    print("=" * 45)
    
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    hero = gui.game_state.hero
    
    # Add test bounties - one active, one completed
    test_bounties = [
        {
            'target': 'Elite Goblin Thief',
            'bounty_type': 'elite_boss',
            'target_count': 1,
            'current_count': 1,  # Completed
            'completed': True,   # Marked as completed
            'difficulty': 'Gold',
            'reward_gold': 125,
            'reward_item': 'Master Hunter Amulet',
            'status': 'active',
            'description': 'Defeat the Elite Goblin Thief in the grasslands'
        },
        {
            'target': 'Cyclops',
            'bounty_type': 'hunt',
            'target_count': 1,
            'current_count': 0,  # Not completed
            'completed': False,
            'difficulty': 'Silver',
            'reward_gold': 80,
            'reward_item': 'Iron Shield',
            'status': 'active',
            'description': 'Hunt the Cyclops in the desert'
        },
        {
            'target': 'Wild Boar',
            'bounty_type': 'collector',
            'target_count': 3,
            'current_count': 2,  # In progress
            'completed': False,
            'difficulty': 'Bronze',
            'reward_gold': 60,
            'reward_item': 'Health Potion',
            'status': 'active',
            'description': 'Hunt Wild Boars in the grasslands'
        }
    ]
    
    if 'bounties' not in hero:
        hero['bounties'] = []
    
    # Add test bounties
    hero['bounties'].extend(test_bounties)
    
    print(f"✅ Added test bounties:")
    print(f"  1. Elite Goblin Thief - COMPLETED ✅")
    print(f"  2. Cyclops - Active (0/1)")
    print(f"  3. Wild Boar - In Progress (2/3)")
    
    # Test the display logic
    print(f"\n🖥️  Testing main menu display logic:")
    
    active_bounties = gui.bounty_manager.get_active_bounties(hero)
    print(f"Active bounties found: {len(active_bounties)}")
    
    for i, bounty in enumerate(active_bounties, 1):
        progress = bounty.current_count
        target = bounty.target_count
        is_completed = bounty.completed or progress >= target
        
        status = "✅ COMPLETED" if is_completed else f"📍 {progress}/{target}"
        color_desc = "Green (completed)" if is_completed else "Yellow (active)"
        
        print(f"  {i}. {bounty.target} ({bounty.difficulty})")
        print(f"     Status: {status}")
        print(f"     Display Color: {color_desc}")
        print(f"     Show Claim Message: {'Yes' if is_completed else 'No'}")
        print()
    
    # Test the actual display by simulating what would appear
    print(f"🎯 Simulated Main Menu Display:")
    print(f"Active Bounties:")
    
    for i, bounty in enumerate(active_bounties[:3], 1):
        progress = bounty.current_count
        target = bounty.target_count
        is_completed = bounty.completed or progress >= target
        
        # Simulate the display logic
        completion_status = " ✅ COMPLETED" if is_completed else ""
        
        if bounty.bounty_type == 'hunt':
            bounty_desc = f"Hunt {bounty.target} ({bounty.difficulty}){completion_status}"
        elif bounty.bounty_type == 'collector':
            bounty_desc = f"Kill {progress}/{target} {bounty.target} ({bounty.difficulty}){completion_status}"
        elif bounty.bounty_type == 'elite_boss':
            bounty_desc = f"Elite Boss: {bounty.target} ({bounty.difficulty}){completion_status}"
        
        reward_desc = f"{bounty.reward_gold}g, {bounty.reward_item}"
        reward_suffix = " - Go to Tavern to Claim!" if is_completed else ""
        
        print(f"  {i}. {bounty_desc} (Reward: {reward_desc}){reward_suffix}")
    
    print(f"\n🎉 Bounty completion display test complete!")
    print(f"📋 Expected behavior:")
    print(f"  ✅ Completed bounties show 'COMPLETED' status")
    print(f"  🎨 Completed bounties display in green")  
    print(f"  📢 Completed bounties show 'Go to Tavern to Claim!'")
    print(f"  📊 In-progress bounties show progress (e.g. 2/3)")
    
    root.destroy()

if __name__ == '__main__':
    test_bounty_completion_display()