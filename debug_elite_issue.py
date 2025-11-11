#!/usr/bin/env python3
"""Debug elite bounty issue - check current game state and bounty tracking"""

import sys
import os
import logging

# Add logging to see what's happening
logging.basicConfig(level=logging.DEBUG)

def check_elite_bounty_issue():
    """Check the current state of elite bounties in the game"""
    
    print("🔍 Elite Bounty Debug Check")
    print("=" * 50)
    
    # Check if we can import the game modules
    try:
        from gui_main import GameGUI
        from game_state import initialize_game_state
        import tkinter as tk
        print("✅ Successfully imported game modules")
    except Exception as e:
        print(f"❌ Failed to import: {e}")
        return
    
    # Initialize the game
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        gui = GameGUI(root)
        hero = gui.game_state.hero
        
        print(f"✅ Game initialized")
        print(f"Hero: {hero.get('name', 'Unknown')}")
        print(f"Level: {hero.get('level', 1)}")
        print(f"Current biome: {gui.background_manager.current_biome}")
    except Exception as e:
        print(f"❌ Failed to initialize game: {e}")
        return
    
    # Check bounty system
    print(f"\n📋 Bounty System Status:")
    
    if hasattr(gui, 'bounty_manager'):
        print(f"✅ Bounty manager exists")
        
        # Check available bounties
        available = gui.bounty_manager.available_bounties
        print(f"Available bounties: {len(available)}")
        
        # Check hero's bounties
        hero_bounties = hero.get('bounties', [])
        print(f"Hero's bounties: {len(hero_bounties)}")
        
        for i, bounty in enumerate(hero_bounties):
            print(f"  {i+1}. Target: '{bounty.get('target', 'Unknown')}'")
            print(f"      Type: {bounty.get('bounty_type', 'Unknown')}")
            print(f"      Progress: {bounty.get('current_count', 0)}/{bounty.get('target_count', 1)}")
            print(f"      Completed: {bounty.get('completed', False)}")
            print(f"      Status: {bounty.get('status', 'Unknown')}")
        
        # Test bounty progress logic
        if hero_bounties:
            print(f"\n🧪 Testing bounty progress logic...")
            
            # Simulate killing "Goblin Thief" in elite encounter
            monster_killed = "Goblin Thief"
            is_elite = True
            
            print(f"Simulating: Kill '{monster_killed}' as elite encounter")
            
            try:
                progressed = gui.bounty_manager.check_bounty_progress_with_elite(
                    hero, monster_killed, is_elite
                )
                print(f"Bounties progressed: {len(progressed)}")
                
                for bounty in progressed:
                    print(f"  - {bounty.target}: {bounty.current_count}/{bounty.target_count}")
                    
            except Exception as e:
                print(f"❌ Error testing bounty progress: {e}")
    else:
        print(f"❌ No bounty manager found")
    
    # Check monster data
    print(f"\n🐉 Monster Data Check:")
    monsters = gui.game_state.monsters
    
    goblin_monsters = [name for name in monsters.keys() if 'goblin' in name.lower()]
    print(f"Goblin-related monsters: {goblin_monsters}")
    
    if 'Goblin Thief' in monsters:
        goblin = monsters['Goblin Thief']
        print(f"Goblin Thief data:")
        print(f"  Name: {goblin.get('name')}")
        print(f"  Biome: {goblin.get('biome', 'grassland')}")
        print(f"  Level: {goblin.get('level', 1)}")
    
    # Check combat system
    print(f"\n⚔️  Combat System Check:")
    if hasattr(gui, 'combat'):
        print(f"✅ Combat system exists")
        elite_flag = getattr(gui.combat, 'is_elite_encounter', None)
        print(f"Current elite encounter flag: {elite_flag}")
    
    root.destroy()
    print(f"\n✅ Debug check complete")

if __name__ == '__main__':
    check_elite_bounty_issue()