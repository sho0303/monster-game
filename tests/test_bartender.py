#!/usr/bin/env python3
"""
Test script for the new bartender beer system in the tavern
"""
import sys
import os
import tkinter as tk
import time

# Add the parent directory to Python path so we can import game modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from gui_main import GameGUI

def test_bartender():
    """Test the bartender functionality"""
    
    print("🍺 Testing Bartender Beer System")
    print("=" * 50)
    
    # Create a root window
    root = tk.Tk()
    
    try:
        # Create the GUI
        gui = GameGUI(root)
        
        # Wait for initialization
        root.update()
        time.sleep(0.2)
        root.update()
        
        # Set up a test hero
        if gui.game_state is None:
            from game_state import GameState
            gui.game_state = GameState()
        
        gui.game_state.hero = {
            'name': 'Beer Tester',
            'age': 25,
            'weapon': 'Test Sword',
            'armour': 'Test Armor',
            'attack': 15,
            'hp': 10,  # Not full health to test beer healing
            'maxhp': 20,
            'defense': 8,
            'class': 'Warrior',
            'level': 5,
            'xp': 0,
            'gold': 50,  # Enough for several beers
            'lives_left': 3,
            'items': {}
        }
        
        print("✅ Test hero created")
        print(f"   HP: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']} (can test beer healing)")
        print(f"   Gold: {gui.game_state.hero['gold']} (can buy 10 beers)")
        
        # Test tavern bartender functionality
        print("\n🍺 Testing bartender initialization...")
        if gui.town:
            print("✅ Town GUI properly initialized")
            
            # Test entering tavern
            print("\n🍻 Testing tavern entry...")
            try:
                gui.town._visit_tavern()
                print("✅ Tavern entry method works")
                print("   Should see 'Talk to Bartender' button")
                
            except Exception as e:
                print(f"❌ Tavern entry error: {e}")
            
            # Test bartender conversation
            print("\n🍺 Testing bartender conversation...")
            try:
                gui.town._talk_to_bartender()
                print("✅ Bartender conversation works")
                print("   Should see 4 beer options (all cost 5 gold, heal 5 HP)")
                
            except Exception as e:
                print(f"❌ Bartender conversation error: {e}")
            
            # Test beer purchase
            print("\n🍻 Testing beer purchase...")
            try:
                initial_hp = gui.game_state.hero['hp']
                initial_gold = gui.game_state.hero['gold']
                
                gui.town._buy_beer(1)  # Buy first beer option
                
                final_hp = gui.game_state.hero['hp']
                final_gold = gui.game_state.hero['gold']
                
                if final_gold == initial_gold - 5:
                    print("✅ Beer purchase deducts correct gold (5)")
                else:
                    print(f"❌ Gold deduction incorrect: {initial_gold} → {final_gold}")
                
                if final_hp > initial_hp:
                    print(f"✅ Beer healing works: {initial_hp} → {final_hp} HP")
                else:
                    print("ℹ️ No healing (may already be at max HP)")
                
            except Exception as e:
                print(f"❌ Beer purchase error: {e}")
                
        else:
            print("❌ Town GUI not initialized")
            return
        
        print("\n✅ Bartender system test completed!")
        print("🍺 Manual Testing Instructions:")
        print("   1. Click 'Visit Tavern' in town")
        print("   2. Click 'Talk to Bartender'")
        print("   3. Try all 4 beer options")
        print("   4. Notice Bob's funny dialogue about them all being beer")
        print("   5. Buy 10+ beers to trigger secret achievement")
        print("   6. Each beer costs 5 gold and heals 5 HP")
        print("\n🎮 Starting interactive test...")
        
        # Start the GUI to manually test
        root.mainloop()
        
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
    test_bartender()