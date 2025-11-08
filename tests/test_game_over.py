"""
Test script to verify game over functionality
"""
import tkinter as tk
from gui_main import GameGUI

def test_game_over():
    """Test the game over functionality"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    # Wait for game to initialize
    def setup_test():
        # Set lives to 0 to trigger game over
        game_gui.game_state.hero['lives_left'] = 0
        print(f"Lives set to: {game_gui.game_state.hero['lives_left']}")
        
        # Trigger game over check
        game_gui.check_game_over()
    
    # Schedule test after GUI is initialized
    root.after(2000, setup_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_game_over()