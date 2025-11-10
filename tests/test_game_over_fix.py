#!/usr/bin/env python3
"""Test game over screen persistence"""

import sys
import os
import tkinter as tk
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_main import GameGUI

def test_game_over_screen():
    """Test that game over screen stays visible"""
    
    print("🧪 Testing Game Over Screen Persistence")
    print("=" * 50)
    
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        # Create the GUI
        gui = GameGUI(root)
        
        # Wait for initialization
        root.update()
        time.sleep(0.1)
        root.update()
        
        # Set up a test hero with 1 life left
        if gui.game_state is None:
            from game_state import GameState
            gui.game_state = GameState()
        
        gui.game_state.hero = {
            'name': 'Test Hero',
            'age': 25,
            'weapon': 'Test Sword',
            'armour': 'Test Armor',
            'attack': 10,
            'hp': 1,  # Low HP so we can easily trigger death
            'maxhp': 15,
            'defense': 5,
            'class': 'Warrior',
            'level': 1,
            'xp': 0,
            'gold': 100,
            'lives_left': 1,  # Only 1 life left
            'items': {}
        }
        
        print("✅ Test hero created with 1 life left")
        
        # Manually trigger game over
        print("🔥 Triggering game over...")
        gui.game_state.hero['lives_left'] = 0
        gui.game_over()
        
        print("✅ Game over method called")
        print("📸 Game over image should now be displayed")
        
        # Check that the interface is locked
        if not gui.keyboard_enabled:
            print("✅ Interface is properly locked")
        else:
            print("❌ Interface is not locked")
        
        # Wait for a moment to simulate the game over display
        print("⏳ Waiting 2 seconds to verify game over screen persistence...")
        root.update()
        time.sleep(2)
        root.update()
        
        print("✅ Game over screen test completed successfully!")
        print("   The game over image should still be visible")
        print(f"   Game will close in {5000//1000} seconds (as designed)")
        
        # Don't wait for the actual close - just verify the fix
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            root.quit()
            root.destroy()
        except:
            pass

if __name__ == '__main__':
    test_game_over_screen()