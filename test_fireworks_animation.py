#!/usr/bin/env python3
"""
Direct test of the victory fireworks animation by simulating Dragon defeat
"""
import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_victory_animation():
    """Test the victory fireworks animation directly"""
    print("🎆 Testing Victory Fireworks Animation")
    
    # Create test GUI window
    root = tk.Tk()
    root.title("Victory Fireworks Test")
    root.geometry("600x600")
    root.configure(bg='black')
    
    # Create canvas for displaying images
    canvas = tk.Canvas(root, width=600, height=600, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Mock audio system
    class MockAudio:
        def play_sound_effect(self, sound_name):
            print(f"🔊 Playing: {sound_name}")
    
    # Mock GUI system
    class MockGUI:
        def __init__(self):
            self.root = root
            self.canvas = canvas
            self.audio = MockAudio()
            self._locked = False
        
        def lock_interface(self):
            self._locked = True
            print("🔒 Interface locked")
        
        def unlock_interface(self):
            self._locked = False
            print("🔓 Interface unlocked")
        
        def show_image(self, image_path):
            """Display image on canvas"""
            try:
                # Load and resize image
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((512, 512), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                self.current_image = ImageTk.PhotoImage(pil_image)
                
                # Clear canvas and show image centered
                self.canvas.delete("all")
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                x = (canvas_width - 512) // 2
                y = (canvas_height - 512) // 2
                
                self.canvas.create_image(x, y, image=self.current_image, anchor=tk.NW)
                self.canvas.update()
                
                print(f"📸 Displaying: {image_path}")
                
            except Exception as e:
                print(f"❌ Error loading image {image_path}: {e}")
                # Show placeholder text
                self.canvas.delete("all")
                self.canvas.create_text(300, 300, text=f"Image: {os.path.basename(image_path)}", 
                                      fill="white", font=("Arial", 16))
    
    # Import and test combat system
    try:
        from gui_combat import CombatGUI
        
        # Create mock GUI and combat system
        gui = MockGUI()
        combat = CombatGUI(gui)
        
        # Create mock final boss monster data
        combat.current_monster_data = {
            'name': 'Dragon Nightmare',
            'finalboss': True,
            'level': 10
        }
        
        # Mock fight callback
        def mock_callback(result):
            print(f"🏁 Fight callback: {result}")
            print("🎉 Victory fireworks animation complete!")
            # Close window after animation
            root.after(2000, root.quit)
        
        combat.fight_callback = mock_callback
        
        # Add test button
        def start_test():
            print("\n🎆 Starting victory fireworks animation...")
            combat._start_victory_fireworks_animation()
        
        test_button = tk.Button(root, text="🎆 Test Victory Fireworks", 
                              command=start_test, font=("Arial", 16),
                              bg='darkred', fg='white')
        test_button.pack(pady=20)
        
        # Add instructions
        instructions = tk.Label(root, text="Click button to test Dragon victory fireworks animation",
                              font=("Arial", 12), bg='black', fg='white')
        instructions.pack()
        
        # Wait for canvas to be ready
        root.after(100, lambda: None)
        
        print("🎮 Test window ready!")
        print("Click the button to trigger the victory fireworks animation")
        
        # Run the test
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_victory_animation()