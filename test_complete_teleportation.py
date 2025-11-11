#!/usr/bin/env python3
"""
Test all teleportation and interface functionality after fountain fix
"""
import tkinter as tk
from gui_main import GameGUI

def test_all_teleportation():
    """Test all teleportation and interface functionality"""
    root = tk.Tk()
    root.title("Complete Teleportation Test")
    
    print("🧪 COMPLETE TELEPORTATION & INTERFACE TEST")
    print("="*50)
    
    gui = GameGUI(root)
    
    def run_comprehensive_test():
        """Run comprehensive test after initialization"""
        if not hasattr(gui, 'game_state') or gui.game_state is None:
            root.after(500, run_comprehensive_test)
            return
        
        print("✅ GUI fully initialized")
        
        # Test 1: Main menu navigation
        print("🧪 Test 1: Main menu interface")
        gui.main_menu()
        print(f"   Interface locked? {getattr(gui, '_interface_locked', 'Unknown')}")
        
        # Test 2: Biome cycling (B key)
        root.after(1000, test_biome_cycling)
    
    def test_biome_cycling():
        print("🧪 Test 2: Biome cycling (B key)")
        original_biome = gui.background_manager.current_biome
        print(f"   Original biome: {original_biome}")
        
        # Simulate B key press
        gui._handle_keypress({'keysym': 'b'})
        new_biome = gui.background_manager.current_biome
        print(f"   New biome: {new_biome}")
        print(f"   Interface locked? {getattr(gui, '_interface_locked', 'Unknown')}")
        
        root.after(1000, test_teleportation)
    
    def test_teleportation():
        print("🧪 Test 3: Random teleportation (T key)")
        original_biome = gui.background_manager.current_biome
        print(f"   Original biome: {original_biome}")
        
        # Simulate T key press
        gui._handle_keypress({'keysym': 't'})
        new_biome = gui.background_manager.current_biome
        print(f"   New biome after teleport: {new_biome}")
        print(f"   Interface locked? {getattr(gui, '_interface_locked', 'Unknown')}")
        
        # Go to town for fountain test
        root.after(1000, test_town_entry)
    
    def test_town_entry():
        print("🧪 Test 4: Town entry and fountain")
        
        # Navigate to town (option 5 in main menu)
        gui.main_menu()
        root.after(500, lambda: gui._handle_keypress({'keysym': '5'}))
        
        root.after(1000, test_fountain_specifically)
    
    def test_fountain_specifically():
        print("🧪 Test 5: Fountain visit")
        
        # If we're in town, try to visit fountain (option 4)
        try:
            if hasattr(gui, 'town') and gui.town:
                # Set up test hero
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
                
                print(f"   Hero HP before: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']}")
                
                # Visit fountain directly
                gui.town._visit_fountain()
                
                root.after(1000, check_fountain_results)
            else:
                print("   ❌ Town not accessible")
                finish_test()
        except Exception as e:
            print(f"   ❌ Fountain test error: {e}")
            finish_test()
    
    def check_fountain_results():
        print("🧪 Test 6: Check fountain results")
        print(f"   Hero HP after: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']}")
        print(f"   Interface locked? {getattr(gui, '_interface_locked', 'Unknown')}")
        
        # Test interface responsiveness
        root.after(500, test_final_navigation)
    
    def test_final_navigation():
        print("🧪 Test 7: Final navigation test")
        
        # Try to navigate back to main menu
        try:
            gui.main_menu()
            print("   ✅ Main menu accessible")
        except Exception as e:
            print(f"   ❌ Navigation error: {e}")
        
        finish_test()
    
    def finish_test():
        print("\n🎯 TEST SUMMARY")
        print("="*50)
        
        if hasattr(gui, '_interface_locked') and gui._interface_locked:
            print("❌ INTERFACE STILL LOCKED - BUG DETECTED!")
        else:
            print("✅ Interface appears to be working normally")
        
        print("Manual verification:")
        print("- Check if buttons show text instead of 'Processing...'")
        print("- Try clicking buttons to ensure they respond")
        print("- Test keyboard shortcuts (1-9, B, T)")
        print("\nClose window when done testing.")
    
    # Start test sequence
    root.after(1000, run_comprehensive_test)
    
    root.mainloop()

if __name__ == '__main__':
    test_all_teleportation()