#!/usr/bin/env python3
"""
Test bounty display in main menu
"""
import tkinter as tk
from gui_main import GameGUI
import logging

def test_bounty_display():
    """Test that bounties show up in the main menu"""
    root = tk.Tk()
    root.withdraw()  # Hide the window initially
    
    try:
        gui = GameGUI(root)
        root.update()
        
        # Setup test hero with some gold and level
        gui.game_state.hero['gold'] = 1000
        gui.game_state.hero['level'] = 5
        gui.game_state.hero['hp'] = gui.game_state.hero['maxhp']
        
        print("✓ Game initialized")
        
        # First, let's check if there are any existing bounties
        if hasattr(gui, 'bounty_manager'):
            existing_bounties = gui.bounty_manager.get_active_bounties(gui.game_state.hero)
            print(f"✓ Existing active bounties: {len(existing_bounties)}")
            
            # If no bounties, let's try to accept one via the town tavern
            if len(existing_bounties) == 0:
                print("No active bounties found. Opening town to accept one...")
                gui.town.enter_town()
                root.deiconify()  # Show window for manual testing
                print("Please go to Tavern > Bounty Board and accept a bounty, then return to main menu")
            else:
                # Show main menu to see bounty display
                gui.main_menu()
                root.deiconify()  # Show window
                print("✓ Main menu displayed with bounties")
        else:
            print("✗ No bounty_manager found")
            
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_bounty_display()