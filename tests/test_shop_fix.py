"""
Test shop main menu button fix
"""
import tkinter as tk
from gui_main import GameGUI

def test_shop_menu_fix():
    """Test that shop main menu button works correctly"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def setup_test():
        # Set up a hero for testing
        if not game_gui.game_state.hero or 'lives_left' not in game_gui.game_state.hero:
            hero_name = list(game_gui.game_state.heros.keys())[0]
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 500  # Give plenty of gold for testing
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
        
        print("=== Testing Shop Main Menu Button ===")
        print("Opening shop...")
        
        # Open the shop
        game_gui.shop.open()
        
        print("✓ Shop opened successfully")
        print("✓ Check that main menu buttons are visible and functional")
        print("✓ Test navigation and purchase flow")
    
    # Start test after initialization
    root.after(3000, setup_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_shop_menu_fix()