"""
Simple direct test for button highlight TclError fix
"""
import tkinter as tk
from gui_main import GameGUI
import time

def simple_highlight_test():
    """Simple test of button highlighting with destruction"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def run_test():
        print("\n=== Button Highlight Fix Test ===")
        
        # Create some buttons
        game_gui.set_buttons(["Button 1", "Button 2"], lambda x: None)
        print("✓ Created 2 buttons")
        
        # Highlight button 1 - this schedules a callback for 200ms later
        game_gui._highlight_button(1)
        print("✓ Highlighted button 1 (callback scheduled)")
        
        # Wait a bit, then destroy buttons before callback executes
        def destroy_and_recreate():
            print("✓ Destroying buttons while highlight callback is pending...")
            game_gui.set_buttons(["New 1", "New 2", "New 3"], lambda x: None)
            print("✓ Created 3 new buttons")
            print("✓ Waiting for old highlight callback to execute...")
            
            # Wait for callback to execute
            def check_result():
                print("✅ Test completed - no TclError means fix is working!")
                root.quit()
            
            root.after(300, check_result)  # Wait for the 200ms callback + some extra time
        
        # Destroy buttons after 50ms (before the 200ms highlight callback)
        root.after(50, destroy_and_recreate)
    
    # Start test after GUI initialization
    root.after(2000, run_test)
    
    # Set a maximum test time
    root.after(10000, root.quit)
    
    root.mainloop()
    print("Test finished.")

if __name__ == "__main__":
    simple_highlight_test()