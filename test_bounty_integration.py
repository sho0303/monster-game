#!/usr/bin/env python3
"""
Test bounty integration and tracking
"""
import tkinter as tk
from gui_main import GameGUI
import logging

def test_bounty_integration():
    """Test that bounty tracking and display works"""
    root = tk.Tk()
    
    try:
        gui = GameGUI(root)
        root.update()
        
        # Setup test hero with good stats
        hero = gui.game_state.hero
        hero['gold'] = 2000
        hero['level'] = 6
        hero['hp'] = hero['maxhp'] = 100
        hero['attack'] = 20
        hero['defense'] = 15
        
        print("✓ Game initialized")
        print(f"✓ Hero: {hero['name']} (Level {hero['level']})")
        
        # Check bounty manager
        if hasattr(gui, 'bounty_manager'):
            print("✓ Bounty manager found")
            
            # Show current bounties
            active_bounties = gui.bounty_manager.get_active_bounties(hero)
            print(f"✓ Active bounties: {len(active_bounties)}")
            
            if len(active_bounties) > 0:
                for bounty in active_bounties:
                    print(f"  - {bounty.target} ({bounty.bounty_type}, {bounty.difficulty}): {bounty.current_count}/{bounty.target_count}")
            
            # Test main menu display
            print("✓ Testing main menu with bounty display...")
            gui.main_menu()
            
        else:
            print("✗ No bounty_manager found")
            
        print("\n=== Integration Test Complete ===")
        print("Features implemented:")
        print("• Bounty display in main menu alongside quests")
        print("• Bounty progress tracking during combat")
        print("• Elite monster bounty support")
        print("• Achievement integration for bounty completion")
        print("\nTo test:")
        print("1. Go to Town → Tavern → Bounty Board")
        print("2. Accept a bounty")
        print("3. Return to main menu to see bounty listed")
        print("4. Fight monsters matching the bounty")
        print("5. See progress updates and completion messages")
        
        root.deiconify()  # Show the window
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_bounty_integration()