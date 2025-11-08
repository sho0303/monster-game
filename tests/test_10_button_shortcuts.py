#!/usr/bin/env python3
"""
Quick test to verify keyboard shortcuts work up to 10 buttons
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from gui_main import GameGUI

def test_10_buttons():
    """Test keyboard shortcuts with up to 10 buttons"""
    print("🧪 Testing Maximum Keyboard Shortcuts (10 buttons)")
    print("Keys 1-9 and 0 (for button 10)")
    print("=" * 50)
    
    root = tk.Tk()
    
    try:
        game_gui = GameGUI(root)
        
        def test_after_init():
            if not game_gui.game_state:
                root.after(100, test_after_init)
                return
            
            # Test with 10 buttons
            results = []
            
            def test_callback(choice):
                results.append(choice)
                print(f"✅ Button {choice} keyboard shortcut working!")
                
                if len(results) >= 3:  # Test first 3 and last one
                    print(f"🏆 Tested {len(results)} buttons successfully!")
                    root.destroy()
            
            # Create 10 test buttons
            labels = [f"Button {i}" for i in range(1, 11)]
            
            game_gui.clear_text()
            game_gui.print_text("Testing 10-button keyboard shortcuts...")
            game_gui.set_buttons(labels, test_callback)
            
            # Test keys 1, 5, and 0 (button 10)
            def test_sequence():
                # Test button 1
                event1 = type('Event', (), {})()
                event1.keysym = '1'
                game_gui._handle_keypress(event1)
                
                # Test button 5
                root.after(500, lambda: [
                    setattr(event5 := type('Event', (), {})(), 'keysym', '5'),
                    game_gui._handle_keypress(event5)
                ])
                
                # Test button 10 (key '0')
                root.after(1000, lambda: [
                    setattr(event0 := type('Event', (), {})(), 'keysym', '0'),
                    game_gui._handle_keypress(event0)
                ])
            
            root.after(500, test_sequence)
        
        root.after(500, test_after_init)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_10_buttons()