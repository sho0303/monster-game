#!/usr/bin/env python3
"""
Test script for the "no suitable monsters" feature
"""

import tkinter as tk
import sys

def test_no_monsters_scenario():
    """Test the no monsters message functionality"""
    print("🧪 Testing 'No Suitable Monsters' scenario...")
    
    try:
        sys.path.append('.')
        import gui_main
        import gui_monster_encounter
        
        root = tk.Tk()
        root.withdraw()
        
        # Create game instance
        game = gui_main.GameGUI(root)
        
        # Fully initialize the game
        game.initialize_game()
        
        # Mock a scenario where no monsters are available
        # Create a mock hero at a very high level
        original_hero = game.game_state.hero.copy()
        game.game_state.hero['level'] = 50  # Very high level
        
        # Mock empty monsters dict to simulate no appropriate monsters
        original_monsters = game.game_state.monsters.copy()
        
        # Create a scenario with only low-level monsters in current biome
        test_monsters = {
            'TestWeakMonster': {
                'name': 'Weak Test Monster',
                'hp': 5,
                'maxhp': 5,
                'attack': 1,
                'defense': 1,
                'level': 1,
                'gold': 1,
                'biome': 'grassland'
            }
        }
        game.game_state.monsters = test_monsters
        
        print("   🎯 Testing monster selection with high-level hero vs low-level monsters...")
        
        # Test the selection logic
        encounter = game.monster_encounter
        result = encounter._select_random_monster()
        
        if result is None:
            print("   ✅ _select_random_monster() correctly returns None for out-of-range monsters")
        else:
            print("   ❌ _select_random_monster() should return None but returned:", result)
            return False
        
        print("   🎯 Testing no monsters message display...")
        
        # Mock the GUI methods to avoid actual display
        original_clear_text = game.clear_text
        original_print_colored_parts = game._print_colored_parts
        original_set_buttons = game.set_buttons
        
        messages_displayed = []
        
        def mock_clear_text():
            messages_displayed.append("CLEAR_TEXT")
        
        def mock_print_colored_parts(parts):
            text = "".join([part[0] for part in parts])
            messages_displayed.append(text)
        
        def mock_set_buttons(labels, callback):
            messages_displayed.append(f"BUTTONS: {labels}")
        
        game.clear_text = mock_clear_text
        game._print_colored_parts = mock_print_colored_parts
        game.set_buttons = mock_set_buttons
        
        # Test the no monsters message
        encounter._show_no_monsters_message()
        
        # Check that appropriate messages were displayed
        message_text = " ".join(messages_displayed)
        
        if "No Suitable Monsters Found" in message_text:
            print("   ✅ No monsters message displayed correctly")
        else:
            print("   ❌ No monsters message not found in output:", message_text)
            return False
        
        if "level range" in message_text:
            print("   ✅ Level range information included")
        else:
            print("   ❌ Level range information missing")
            return False
        
        if "teleporting" in message_text or "leveling up" in message_text:
            print("   ✅ Helpful suggestions provided")
        else:
            print("   ❌ Helpful suggestions missing")
            return False
        
        # Restore original state
        game.game_state.hero = original_hero
        game.game_state.monsters = original_monsters
        game.clear_text = original_clear_text
        game._print_colored_parts = original_print_colored_parts
        game.set_buttons = original_set_buttons
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_normal_monster_selection():
    """Test that normal monster selection still works"""
    print("\\n🧪 Testing normal monster selection...")
    
    try:
        sys.path.append('.')
        import gui_main
        
        root = tk.Tk()
        root.withdraw()
        
        # Create game instance
        game = gui_main.GameGUI(root)
        
        # Fully initialize the game
        game.initialize_game()
        
        # Ensure hero is at level 1 (should match most monsters)
        game.game_state.hero['level'] = 1
        
        # Test monster selection with normal conditions
        encounter = game.monster_encounter
        result = encounter._select_random_monster()
        
        if result is not None:
            monster_type, monster = result
            print(f"   ✅ Normal monster selection works: {monster['name']} (Level {monster['level']})")
        else:
            print("   ⚠️  No monsters found for level 1 hero - this might indicate a data issue")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

if __name__ == '__main__':
    print("🎯 NO SUITABLE MONSTERS FEATURE TEST SUITE")
    print("=" * 60)
    
    test1 = test_no_monsters_scenario()
    test2 = test_normal_monster_selection()
    
    print("\\n" + "=" * 60)
    print("🏆 TEST RESULTS:")
    print(f"   🚫 No Monsters Scenario: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   ⚔️ Normal Monster Selection: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if test1 and test2:
        print("\\n🎉 SUCCESS! No suitable monsters feature working correctly!")
        print("\\n📋 FEATURE SUMMARY:")
        print("   • Players get clear message when no level-appropriate monsters available")
        print("   • Level range information displayed (hero_level-1 to hero_level*2)")
        print("   • Helpful suggestions provided (teleport or level up)")
        print("   • No more fallback to grassland monsters")
        print("   • Normal monster selection preserved for appropriate levels")
    else:
        print("\\n❌ ISSUES DETECTED! Check the failure details above.")
        print("\\n🔧 Next steps:")
        print("   • Verify monster level ranges in YAML files")
        print("   • Check biome assignments for monsters")
        print("   • Test in-game with different hero levels")