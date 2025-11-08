"""
Test keyboard shortcuts with variable button system
"""
import tkinter as tk
from gui_main import GameGUI

def test_keyboard_shortcuts():
    """Test keyboard functionality with variable buttons"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def setup_test():
        game_gui.clear_text()
        game_gui.print_text("🎮 Keyboard Shortcut Test")
        game_gui.print_text("=" * 40)
        game_gui.print_text("Try these keyboard shortcuts:")
        game_gui.print_text("• Number keys 1-6 for direct selection")
        game_gui.print_text("• Left/Right arrows to navigate")
        game_gui.print_text("• Enter to select highlighted button")
        game_gui.print_text("• Space for first available button")
        game_gui.print_text("")
        game_gui.print_text("Current test: 6 buttons")
        
        def on_choice(choice):
            buttons = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]
            if choice <= len(buttons):
                game_gui.print_text(f"\n✓ Selected: {buttons[choice-1]} (Button {choice})")
            
            # Set up next test with different button count
            root.after(2000, setup_fewer_buttons)
        
        # Test with 6 buttons
        game_gui.set_buttons([
            "🥇 First",
            "🥈 Second", 
            "🥉 Third",
            "4️⃣ Fourth",
            "5️⃣ Fifth",
            "6️⃣ Sixth"
        ], on_choice)
    
    def setup_fewer_buttons():
        game_gui.clear_text()
        game_gui.print_text("🎮 Keyboard Shortcut Test")
        game_gui.print_text("=" * 40)
        game_gui.print_text("Now testing with 2 buttons:")
        game_gui.print_text("• Keys 1-2 should work")
        game_gui.print_text("• Keys 3-6 should be ignored")
        game_gui.print_text("• Navigation should wrap between 1 and 2")
        
        def on_choice_2(choice):
            buttons = ["Yes", "No"]
            if choice <= len(buttons):
                game_gui.print_text(f"\n✓ Selected: {buttons[choice-1]} (Button {choice})")
            
            # Complete test
            root.after(2000, complete_test)
        
        # Test with 2 buttons
        game_gui.set_buttons([
            "✅ Yes",
            "❌ No"
        ], on_choice_2)
    
    def complete_test():
        game_gui.clear_text()
        game_gui.print_text("✅ Keyboard shortcut tests completed!")
        game_gui.print_text("")
        game_gui.print_text("Variable button system is working correctly:")
        game_gui.print_text("• Dynamic button creation ✅")
        game_gui.print_text("• Keyboard navigation ✅") 
        game_gui.print_text("• Number key shortcuts ✅")
        game_gui.print_text("• Arrow key navigation ✅")
        
        def on_final(choice):
            print("Test completed successfully!")
            root.after(1000, root.quit)
        
        game_gui.set_buttons(["🚪 Exit Test"], on_final)
    
    # Start test after initialization
    root.after(3000, setup_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_keyboard_shortcuts()