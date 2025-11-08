"""
Test the button highlighting fix
Rapidly switches between different button counts to trigger the error scenario
"""
import tkinter as tk
from gui_main import GameGUI

def test_button_highlight_fix():
    """Test button highlighting with rapid button changes"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    test_count = 0
    
    def rapid_button_test():
        nonlocal test_count
        test_count += 1
        
        if test_count > 10:
            print("✅ Test completed - no errors!")
            root.after(1000, root.quit)
            return
        
        # Alternate between different button counts rapidly
        if test_count % 2 == 0:
            # 2 buttons
            def callback1(choice):
                print(f"2-button test: Button {choice} clicked")
                # Immediately switch to different button count
                root.after(50, rapid_button_test)
            
            game_gui.clear_text()
            game_gui.print_text(f"\nTest {test_count}: 2 buttons")
            game_gui.set_buttons(["⚔️ Fight", "🏃 Run"], callback1)
            
            # Trigger highlight on first button
            game_gui._highlight_button(1)
            
        else:
            # 4 buttons  
            def callback2(choice):
                print(f"4-button test: Button {choice} clicked")
                # Immediately switch to different button count
                root.after(50, rapid_button_test)
            
            game_gui.clear_text()
            game_gui.print_text(f"\nTest {test_count}: 4 buttons")
            game_gui.set_buttons([
                "🛒 Shop", "⚔️ Fight", "🧪 Item", "📊 Stats"
            ], callback2)
            
            # Trigger highlight on second button
            game_gui._highlight_button(2)
    
    # Start test after initialization
    root.after(3000, rapid_button_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_button_highlight_fix()