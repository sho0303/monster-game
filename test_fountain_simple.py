#!/usr/bin/env python3
"""
Direct test for fountain interface locking fix
"""
import tkinter as tk
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui_main import GameGUI

def test_fountain_fix():
    """Direct test of fountain functionality"""
    root = tk.Tk()
    root.title("Fountain Fix Test")
    
    # Wait for full GUI initialization
    def run_test():
        print("🧪 FOUNTAIN INTERFACE FIX TEST")
        print("="*40)
        
        # Check if town is initialized
        if hasattr(gui, 'town') and gui.town is not None:
            print("✅ Town GUI initialized")
            
            # Set up a test hero manually
            if hasattr(gui, 'game_state') and gui.game_state is not None:
                gui.game_state.hero = {
                    'name': 'Test Hero',
                    'hp': 10,
                    'maxhp': 20,
                    'attack': 15,
                    'defense': 10,
                    'level': 3,
                    'class': 'Warrior',
                    'weapon': 'Test Sword',
                    'armour': 'Test Armor',
                    'age': 25,
                    'gold': 100
                }
                print("✅ Test hero created")
                print(f"   Hero HP: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']}")
                
                # Test the fountain directly
                print("🧪 Testing fountain visit...")
                gui.town._visit_fountain()
                
                # Check interface state after 1 second
                root.after(1000, check_interface)
            else:
                print("❌ Game state not initialized")
        else:
            print("❌ Town GUI not initialized")
            root.after(500, run_test)  # Try again
    
    def check_interface():
        """Check if interface is properly unlocked"""
        if hasattr(gui, '_interface_locked'):
            if gui._interface_locked:
                print("❌ BUG: Interface is still locked after fountain visit!")
            else:
                print("✅ SUCCESS: Interface properly unlocked")
        else:
            print("⚠️  Interface lock state unknown")
        
        print(f"✅ Hero HP after fountain: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']}")
        
        print("\n🎯 TEST COMPLETE")
        print("Close the game window to see if buttons work normally")
        print("Look for 'Return to Town' button instead of 'Processing...'")
    
    # Create GUI and wait for initialization
    gui = GameGUI(root)
    
    # Start test after initialization delay
    root.after(1000, run_test)
    
    root.mainloop()

if __name__ == '__main__':
    test_fountain_fix()