"""
Biome testing utility for the monster game.
This allows testing different biomes in the game.
"""

def test_desert_biome():
    """Test the desert biome by temporarily setting it as the main background"""
    import sys
    sys.path.append('..')
    
    try:
        from gui_main import GameGUI
        from game_state import GameState
        import tkinter as tk
        
        # Create a simple test window
        root = tk.Tk()
        root.title("Desert Biome Test")
        root.geometry("900x600")
        
        # Initialize game components
        gui = GameGUI(root)
        
        # Set desert biome
        gui.set_biome_background('desert')
        
        # Add some text to show the biome
        gui.print_text("🏜️ Desert Biome Test 🏜️")
        gui.print_text("You are now in the desert biome!")
        gui.print_text("Features:")
        gui.print_text("- Warm orange-golden sky")
        gui.print_text("- Rolling sand dunes")
        gui.print_text("- Desert cacti and rocks")
        gui.print_text("- Heat shimmer effects")
        
        # Add buttons to test other biomes
        def test_grassland():
            gui.set_biome_background('grassland')
            gui.clear_text()
            gui.print_text("🌱 Grassland Biome 🌱")
            gui.print_text("You are now in the grassland biome!")
        
        def test_desert():
            gui.set_biome_background('desert') 
            gui.clear_text()
            gui.print_text("🏜️ Desert Biome 🏜️")
            gui.print_text("You are now in the desert biome!")
        
        def test_dungeon():
            gui.set_biome_background('dungeon')
            gui.clear_text()
            gui.print_text("🏰 Dungeon Biome 🏰")
            gui.print_text("You are now in the dungeon biome!")
        
        def test_shop():
            gui.set_biome_background('shop')
            gui.clear_text()
            gui.print_text("🛒 Shop Interior 🛒")
            gui.print_text("You are now in the shop!")
        
        # Set up biome test buttons
        biome_buttons = [
            ("Grassland", test_grassland),
            ("Desert", test_desert), 
            ("Dungeon", test_dungeon),
            ("Shop", test_shop),
        ]
        
        gui.set_buttons([btn[0] for btn in biome_buttons], lambda choice: biome_buttons[choice-1][1]())
        
        print("Desert biome test started!")
        print("Use the buttons to test different biomes.")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"Could not import required modules: {e}")
        print("Make sure you're running this from the art_generation directory")
    except Exception as e:
        print(f"Error running biome test: {e}")

if __name__ == "__main__":
    test_desert_biome()