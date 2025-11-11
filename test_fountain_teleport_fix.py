#!/usr/bin/env python3
"""
Test fountain and teleportation functionality to ensure interface works properly
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_fountain_and_teleportation():
    """Test fountain visit and teleportation to ensure no interface locking issues"""
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Wait for GUI to initialize properly
    def wait_for_initialization():
        if gui.town is None:
            root.after(100, wait_for_initialization)
            return
        start_actual_test()
    
    def start_actual_test():
        # Initialize game state with a hero that needs healing
        gui.game_state = initialize_game_state()
    
    # Set up test hero with partial HP to test fountain healing
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
    
    print("🧪 TESTING FOUNTAIN AND TELEPORTATION")
    print("="*50)
    print(f"Test Hero HP: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']}")
    print()
    
    # Test sequence
    print("✅ Test 1: Visit Town")
    gui.town.enter_town()
    
    def test_fountain():
        print("✅ Test 2: Visit Fountain (should heal and unlock interface)")
        gui.town._visit_fountain()
        
        # Check if interface is properly unlocked after fountain visit
        root.after(1000, check_interface_state)
    
    def check_interface_state():
        print(f"✅ Test 3: Interface locked? {gui._interface_locked}")
        print(f"✅ Test 3: Hero HP after fountain: {gui.game_state.hero['hp']}/{gui.game_state.hero['maxhp']}")
        
        if gui._interface_locked:
            print("❌ INTERFACE STILL LOCKED - THIS IS THE BUG!")
        else:
            print("✅ Interface properly unlocked")
        
        root.after(1000, test_teleportation)
    
    def test_teleportation():
        print("✅ Test 4: Testing teleportation from town")
        
        # First go back to main menu
        gui.main_menu()
        root.after(500, test_teleport_function)
    
    def test_teleport_function():
        print("✅ Test 5: Testing teleport to random biome")
        original_biome = gui.background_manager.current_biome
        print(f"Current biome: {original_biome}")
        
        # Test teleportation
        gui.teleport_to_random_biome()
        root.after(500, verify_teleport)
    
    def verify_teleport():
        new_biome = gui.background_manager.current_biome
        print(f"✅ Test 6: New biome after teleport: {new_biome}")
        
        if gui._interface_locked:
            print("❌ INTERFACE LOCKED AFTER TELEPORT - BUG!")
        else:
            print("✅ Interface working after teleport")
        
        # Test biome cycling
        root.after(500, test_biome_cycling)
    
    def test_biome_cycling():
        print("✅ Test 7: Testing biome cycling (B key functionality)")
        original_biome = gui.background_manager.current_biome
        
        # Simulate B key press for biome cycling
        gui._handle_keypress({'keysym': 'b'})
        root.after(500, verify_biome_cycle)
    
    def verify_biome_cycle():
        new_biome = gui.background_manager.current_biome
        print(f"✅ Test 8: Biome after cycling: {new_biome}")
        
        if gui._interface_locked:
            print("❌ INTERFACE LOCKED AFTER BIOME CYCLE - BUG!")
        else:
            print("✅ Interface working after biome cycle")
        
        print("🎯 TESTING COMPLETE")
        print("="*50)
        print("If you see any ❌ errors above, there are still interface bugs.")
        print("If all ✅ tests pass, fountain and teleportation are fixed!")
        print("Close window when done reviewing results.")
    
        # Start the test sequence
        root.after(2000, test_fountain)
    
    # Wait for initialization then start test
    root.after(500, wait_for_initialization)
    
    root.mainloop()

if __name__ == '__main__':
    test_fountain_and_teleportation()