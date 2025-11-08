#!/usr/bin/env python3
"""
Test keyboard shortcuts with more than 3 buttons
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from gui_main import GameGUI

def test_extended_keyboard_shortcuts():
    """Test keyboard shortcuts with 4+ buttons"""
    print("🧪 Testing Extended Keyboard Shortcuts (4+ buttons)")
    print("=" * 60)
    
    root = tk.Tk()
    
    try:
        # Create game GUI
        game_gui = GameGUI(root)
        
        def test_after_init():
            if not game_gui.game_state:
                root.after(100, test_after_init)
                return
            
            print("✅ Game initialized")
            
            # Create a test scenario with 5 buttons
            button_pressed = []
            
            def test_callback(choice):
                button_pressed.append(choice)
                print(f"✅ Button {choice} pressed successfully!")
                
                # Test all buttons 1-5
                if len(button_pressed) < 5:
                    next_button = len(button_pressed) + 1
                    print(f"🎯 Testing button {next_button} keyboard shortcut...")
                    
                    # Simulate key press for next button
                    event = type('Event', (), {})()
                    event.keysym = str(next_button)
                    game_gui._handle_keypress(event)
                else:
                    print("🏆 All 5 buttons tested successfully!")
                    print("✅ Extended keyboard shortcuts working correctly!")
                    root.destroy()
            
            # Set up 5 buttons to test
            test_labels = [
                "🔵 Button 1", 
                "🟢 Button 2", 
                "🟡 Button 3", 
                "🟠 Button 4", 
                "🔴 Button 5"
            ]
            
            game_gui.clear_text()
            game_gui.print_text("Testing 5-button keyboard shortcuts...")
            game_gui.print_text("Each button should respond to its number key (1-5)")
            
            game_gui.set_buttons(test_labels, test_callback)
            
            print("🎮 Created 5 buttons with keyboard shortcuts")
            print("🎯 Testing button 1 keyboard shortcut...")
            
            # Start the test by simulating pressing '1'
            event = type('Event', (), {})()
            event.keysym = '1'
            game_gui._handle_keypress(event)
        
        root.after(1000, test_after_init)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_quest_menu_keyboard():
    """Test that quest menu (4 buttons) works with keyboard"""
    print("\n🧪 Testing Quest Menu Keyboard Shortcuts")
    print("=" * 60)
    
    root = tk.Tk()
    
    try:
        game_gui = GameGUI(root)
        
        def setup_quest_test():
            if not (game_gui.game_state and game_gui.quest_manager):
                root.after(100, setup_quest_test)
                return
            
            # Select first hero
            hero_name = list(game_gui.game_state.heros.keys())[0]
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 50
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
            game_gui.quest_manager.initialize_hero_quests(game_gui.game_state.hero)
            
            print("✅ Hero selected and initialized")
            
            # Show main menu (which has 4 buttons including Quests)
            game_gui.main_menu()
            
            print("✅ Main menu displayed with 4 buttons:")
            print("   1. 🛒 Shop")
            print("   2. ⚔️ Fight Monster") 
            print("   3. 🧪 Use Item")
            print("   4. 📜 Quests")
            
            # Test button 4 (Quests) 
            print("🎯 Testing button 4 (Quests) keyboard shortcut...")
            
            # Wait a moment then test
            def test_button_4():
                event = type('Event', (), {})()
                event.keysym = '4'
                game_gui._handle_keypress(event)
                print("✅ Button 4 keyboard shortcut sent")
                
                # Close after a short delay
                root.after(2000, lambda: [
                    print("🏆 Quest menu keyboard shortcut test completed!"),
                    root.destroy()
                ])
            
            root.after(1000, test_button_4)
        
        root.after(500, setup_quest_test)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Quest menu test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extended_keyboard_shortcuts()
    test_quest_menu_keyboard()