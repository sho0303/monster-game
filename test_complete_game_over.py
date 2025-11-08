"""
Comprehensive test for game over functionality
Simulates actual gameplay scenario where hero loses all lives
"""
import tkinter as tk
from gui_main import GameGUI

def test_complete_game_over_scenario():
    """Test complete game over scenario"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def simulate_multiple_deaths():
        print("=== Testing Game Over Scenario ===")
        
        # First, select a hero (simulate selecting the first hero)
        if not game_gui.game_state.hero or 'lives_left' not in game_gui.game_state.hero:
            hero_name = list(game_gui.game_state.heros.keys())[0]  # Get first hero
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 50
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
            print(f"Selected hero: {hero_name}")
        
        # Show initial lives
        initial_lives = game_gui.game_state.hero['lives_left']
        print(f"Initial lives: {initial_lives}")
        
        # Simulate losing lives one by one
        for i in range(initial_lives):
            current_lives = game_gui.game_state.hero['lives_left']
            print(f"Current lives before death #{i+1}: {current_lives}")
            
            # Reduce life by 1
            game_gui.game_state.hero['lives_left'] -= 1
            
            remaining_lives = game_gui.game_state.hero['lives_left']
            print(f"Lives after death #{i+1}: {remaining_lives}")
            
            # Check if this triggers game over
            if game_gui.check_game_over():
                print("GAME OVER TRIGGERED!")
                return
            else:
                print("Game continues...")
        
        print("Test completed - game should have ended by now")
    
    # Wait for game to initialize, then run test
    root.after(3000, simulate_multiple_deaths)
    
    root.mainloop()

if __name__ == "__main__":
    test_complete_game_over_scenario()