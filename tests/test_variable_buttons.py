"""
Test script to verify dynamic button functionality
Tests 1, 2, 3, 4, 5, and 6 button scenarios
"""
import tkinter as tk
from gui_main import GameGUI

def test_variable_buttons():
    """Test the variable button system"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    test_scenarios = [
        # (button_count, labels, description)
        (1, ["⚡ Single Action"], "Single button test"),
        (2, ["✅ Yes", "❌ No"], "Two button test"),
        (3, ["🛒 Shop", "⚔️ Fight", "🧪 Use Item"], "Three button test (classic)"),
        (4, ["🛒 Shop", "⚔️ Fight", "🧪 Use Item", "📊 Stats"], "Four button test"),
        (5, ["🛒 Shop", "⚔️ Fight", "🧪 Use Item", "📊 Stats", "⚙️ Settings"], "Five button test"),
        (6, ["🛒 Shop", "⚔️ Fight", "🧪 Use Item", "📊 Stats", "⚙️ Settings", "🚪 Exit"], "Six button test"),
        (0, [], "No button test (edge case)"),
    ]
    
    current_test = 0
    
    def run_next_test():
        nonlocal current_test
        
        if current_test >= len(test_scenarios):
            print("All tests completed!")
            return
            
        count, labels, description = test_scenarios[current_test]
        print(f"\n=== Test {current_test + 1}: {description} ===")
        print(f"Button count: {count}")
        print(f"Labels: {labels}")
        
        def test_callback(choice):
            print(f"Button {choice} clicked: {labels[choice-1] if choice <= len(labels) else 'Unknown'}")
            
            # Move to next test after a short delay
            current_test += 1
            root.after(2000, run_next_test)
        
        # Test the button system
        if labels:
            game_gui.set_buttons(labels, test_callback)
            print(f"Created {len(game_gui.buttons)} buttons")
        else:
            game_gui.set_buttons([], test_callback)
            print(f"Created {len(game_gui.buttons)} buttons")
        
        # Show test info
        game_gui.clear_text()
        game_gui.print_text(f"\n{description}")
        game_gui.print_text(f"Button Count: {len(game_gui.buttons)}")
        if labels:
            game_gui.print_text("Test navigation with arrow keys, then click any button...")
        else:
            game_gui.print_text("No buttons to test - this should handle gracefully")
            # Auto-advance no-button test
            root.after(2000, lambda: [setattr(test_callback, '__call__', lambda x: None), run_next_test()])
    
    # Wait for game to initialize, then start tests
    root.after(3000, run_next_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_variable_buttons()