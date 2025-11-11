#!/usr/bin/env python3
"""
Test monster data loading for bee to verify attack_sound is properly loaded
"""
import sys
import os
import tkinter as tk
import time

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from gui_main import GameGUI

def test_bee_monster_data():
    """Test that bee monster data loads correctly with attack_sound"""
    
    print("🐝 Testing Bee Monster Data Loading")
    print("=" * 50)
    
    root = tk.Tk()
    root.withdraw()  # Hide window for testing
    
    try:
        # Create the GUI
        gui = GameGUI(root)
        root.update()
        time.sleep(0.2)
        root.update()
        
        # Check if bee monster is loaded
        monsters = gui.game_state.monsters
        
        # Look for bee monster (might have different key names)
        bee_names = ["Angry Bee Swarm", "Bee Swarm", "Bees"]
        
        bee_monster = None
        bee_key = None
        
        for monster_name in monsters:
            if any(bee_name.lower() in monster_name.lower() for bee_name in bee_names):
                bee_monster = monsters[monster_name]
                bee_key = monster_name
                break
        
        if bee_monster:
            print(f"✅ Found bee monster: {bee_key}")
            print("📋 Monster data:")
            for key, value in bee_monster.items():
                print(f"   {key}: {value}")
                
            # Check attack_sound specifically
            if 'attack_sound' in bee_monster:
                print(f"\n🔊 Attack sound configured: {bee_monster['attack_sound']}")
                
                # Test if the combat system would use this sound
                from gui_combat import CombatGUI
                combat = CombatGUI(gui)
                attack_sound = combat._get_monster_attack_sound(bee_monster)
                print(f"🎵 Combat system would use: {attack_sound}")
                
                if attack_sound == bee_monster['attack_sound']:
                    print("✅ Combat system correctly uses monster's attack_sound")
                else:
                    print("❌ Combat system using fallback instead of monster sound")
                    
            else:
                print("❌ No attack_sound field in bee monster data!")
        else:
            print("❌ Bee monster not found!")
            print("Available monsters:")
            for name in monsters.keys():
                print(f"   - {name}")
        
        print(f"\n📊 Total monsters loaded: {len(monsters)}")
        
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
    test_bee_monster_data()