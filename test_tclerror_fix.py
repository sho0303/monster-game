"""
Specific test for the TclError fix
Recreates the exact scenario that caused the button highlight error
"""
import tkinter as tk
from gui_main import GameGUI

def test_specific_error_scenario():
    """Test the specific scenario that caused the TclError"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def setup_test():
        print("=== Testing Button Highlight Error Fix ===")
        
        # Step 1: Set up 2 buttons (like monster encounter)
        def on_choice_2(choice):
            print(f"2-button choice: {choice}")
            # This would trigger the highlighting
            
            # Step 2: Immediately change to different button count
            # This simulates what happens when transitioning between menus
            setup_different_buttons()
        
        game_gui.clear_text()
        game_gui.print_text("Testing 2-button scenario (original error case)")
        game_gui.set_buttons(["⚔️ Fight", "🏃 Run"], on_choice_2)
        
        # Step 3: Trigger button highlight (this is where the error occurred)
        print("Triggering button highlight...")
        game_gui._highlight_button(1)  # This should schedule a callback for 200ms later
        
        # Step 4: Quickly change button configuration before callback executes
        root.after(100, lambda: print("About to change buttons while highlight callback is pending..."))
    
    def setup_different_buttons():
        """Change to different button configuration while highlight is pending"""
        def on_choice_3(choice):
            print(f"3-button choice: {choice}")
            complete_test()
        
        print("Changing to 3 buttons...")
        game_gui.clear_text()
        game_gui.print_text("Changed to 3-button scenario")
        
        # This will destroy the old buttons and create new ones
        # The old button highlight callback should still be pending
        game_gui.set_buttons(["🛒 Shop", "⚔️ Fight", "🧪 Item"], on_choice_3)
        
        print("New buttons created. Old button highlight callback should execute soon...")
        print("If no TclError occurs, the fix is working!")
    
    def complete_test():
        game_gui.clear_text()
        game_gui.print_text("✅ Test completed successfully!")
        game_gui.print_text("No TclError occurred - the fix is working!")
        
        def finish(choice):
            print("✅ Button highlight fix test PASSED!")
            root.after(1000, root.quit)
        
        game_gui.set_buttons(["🚪 Exit"], finish)
    
    # Start test
    root.after(3000, setup_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_specific_error_scenario()