#!/usr/bin/env python3
"""
Test script for multiple image display functionality
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui_main import GameGUI
import tkinter as tk

def test_multiple_images():
    """Test the multiple image display functionality"""
    
    # Create GUI instance - just for testing the image functionality
    import tempfile
    import yaml
    
    # Create minimal test data
    test_hero_data = {
        'Billy': {'class': 'Ninja', 'attack': 5, 'hp': 15, 'maxhp': 15, 'defense': 10}
    }
    
    # Create temporary yaml files for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(test_hero_data, f)
        temp_hero_file = f.name
    
    # Mock the GUI initialization to skip game logic
    root = tk.Tk()
    gui = GameGUI()
    
    # Override some initialization to focus on image testing
    gui.heros = test_hero_data
    
    # Test different image combinations
    def test_single():
        gui.show_image('art/strong_sword.png')
        gui.print_text("Showing single image: strong_sword.png")
    
    def test_horizontal():
        images = ['art/strong_sword.png', 'art/weak_sword.png']
        gui.show_images(images, "horizontal")
        gui.print_text("Showing horizontal layout: strong_sword + weak_sword")
    
    def test_grid():
        images = [
            'art/strong_sword.png', 
            'art/magic_wand.png', 
            'art/wizard_staff.png', 
            'art/lightsaber.png'
        ]
        gui.show_images(images, "grid")
        gui.print_text("Showing grid layout: 4 weapons")
    
    def test_auto():
        images = ['art/health_potion.png', 'art/nunchucks.png', 'art/magic_wand.png']
        gui.show_images(images)  # Auto layout
        gui.print_text("Showing auto layout: 3 items")
    
    def test_list_in_show_image():
        images = ['art/strong_sword.png', 'art/weak_sword.png']
        gui.show_image(images)  # Pass list to show_image
        gui.print_text("Testing list passed to show_image()")
    
    # Add test buttons
    test_frame = tk.Frame(root, bg='#1a1a1a')
    test_frame.pack(pady=10)
    
    tk.Button(test_frame, text="Single Image", command=test_single, bg='#333', fg='white').pack(side=tk.LEFT, padx=5)
    tk.Button(test_frame, text="Horizontal", command=test_horizontal, bg='#333', fg='white').pack(side=tk.LEFT, padx=5)
    tk.Button(test_frame, text="Grid", command=test_grid, bg='#333', fg='white').pack(side=tk.LEFT, padx=5)
    tk.Button(test_frame, text="Auto", command=test_auto, bg='#333', fg='white').pack(side=tk.LEFT, padx=5)
    tk.Button(test_frame, text="List in show_image", command=test_list_in_show_image, bg='#333', fg='white').pack(side=tk.LEFT, padx=5)
    
    # Start with single image test
    gui.root.after(1000, test_single)
    
    print("Multiple image display test GUI started!")
    print("Use the test buttons to try different image layouts:")
    print("- Single Image: Traditional single image display")
    print("- Horizontal: Two images side by side") 
    print("- Grid: Four images in 2x2 grid")
    print("- Auto: Three images with automatic layout selection")
    print("- List in show_image: Test backwards compatibility")
    
    root.mainloop()

if __name__ == '__main__':
    test_multiple_images()