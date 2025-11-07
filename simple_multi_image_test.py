#!/usr/bin/env python3
"""
Simple test for multiple image display functionality
"""
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os

class MultiImageTester:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multiple Image Display Test")
        self.root.configure(bg='#1a1a1a')
        
        # Image display area
        self.image_frame = tk.Frame(self.root, bg='#1a1a1a', height=250)
        self.image_frame.pack(fill=tk.BOTH, pady=10)
        self.image_frame.pack_propagate(False)
        
        # Image labels - support for multiple images
        self.image_labels = []
        self.current_image_layout = "single"  # Track current layout mode
        
        # Default single image label for backwards compatibility
        self.image_label = tk.Label(self.image_frame, bg='#1a1a1a')
        self.image_label.pack(expand=True)
        self.image_labels.append(self.image_label)
        
        # Text area for output
        self.text_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD,
            width=80,
            height=10,
            bg='#2a2a2a',
            fg='#00ff00',
            font=('Courier', 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Test buttons
        self._create_test_buttons()
        
        # Add the multi-image methods
        self._add_multi_image_methods()
    
    def _create_test_buttons(self):
        """Create test buttons"""
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(pady=10)
        
        buttons = [
            ("Single Image", self.test_single),
            ("Two Horizontal", self.test_horizontal),
            ("Grid 2x2", self.test_grid),
            ("Auto Layout", self.test_auto),
            ("Show List", self.test_list)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame, 
                text=text, 
                command=command,
                bg='#333333',
                fg='white',
                width=12
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def print_text(self, text):
        """Print text to the text area"""
        self.text_area.insert(tk.END, text + '\n')
        self.text_area.see(tk.END)
        self.root.update()
    
    def test_single(self):
        """Test single image display"""
        self.show_image('art/strong_sword.png')
        self.print_text("✓ Single image: strong_sword.png")
    
    def test_horizontal(self):
        """Test horizontal layout"""
        images = ['art/strong_sword.png', 'art/weak_sword.png']
        self.show_images(images, "horizontal")
        self.print_text("✓ Horizontal: strong_sword + weak_sword")
    
    def test_grid(self):
        """Test grid layout"""
        images = [
            'art/strong_sword.png', 
            'art/magic_wand.png', 
            'art/wizard_staff.png', 
            'art/lightsaber.png'
        ]
        self.show_images(images, "grid")
        self.print_text("✓ Grid: 4 weapons in 2x2 layout")
    
    def test_auto(self):
        """Test auto layout"""
        images = ['art/health_potion.png', 'art/nunchucks.png', 'art/magic_wand.png']
        self.show_images(images)  # Auto layout
        self.print_text("✓ Auto: 3 items with automatic layout")
    
    def test_list(self):
        """Test passing list to show_image"""
        images = ['art/strong_sword.png', 'art/weak_sword.png']
        self.show_image(images)  # Pass list to show_image
        self.print_text("✓ List passed to show_image() - backwards compatible")
    
    def _add_multi_image_methods(self):
        """Add all the multi-image methods from gui_main.py"""
        
        def show_image(image_path):
            """Display a single image in the image area (backwards compatible)"""
            if isinstance(image_path, list):
                # If a list is passed, use show_images instead
                show_images(image_path)
                return
                
            # Reset to single image layout
            _reset_image_layout()
            
            try:
                # Handle text files (ASCII art)
                if image_path.endswith('.txt'):
                    # For text files, create a simple text display
                    with open(image_path, 'r', encoding='utf-8') as f:
                        ascii_art = f.read()
                    # Create an image from text (simple approach)
                    self.image_label.config(text=ascii_art, font=('Courier', 8), fg='#00ff00', bg='#1a1a1a')
                    return
                
                # Handle image files
                img = Image.open(image_path)
                # Resize to fit the frame while maintaining aspect ratio
                img.thumbnail((400, 250), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo, text='')
                self.image_label.image = photo  # Keep a reference
            except Exception as e:
                self.print_text(f"Could not load image: {e}")
        
        def show_images(image_paths, layout="auto"):
            """Display multiple images in the image area"""
            if not image_paths:
                return
            
            # If single image, fall back to show_image
            if len(image_paths) == 1:
                show_image(image_paths[0])
                return
            
            # Clear existing layout
            _clear_image_area()
            
            # Determine layout
            num_images = len(image_paths)
            if layout == "auto":
                if num_images <= 2:
                    layout = "horizontal"
                elif num_images <= 4:
                    layout = "grid"
                else:
                    layout = "grid"  # Handle more than 4 images in grid
            
            # Create layout
            if layout == "horizontal":
                _create_horizontal_layout(image_paths)
            elif layout == "vertical":
                _create_vertical_layout(image_paths)
            elif layout == "grid":
                _create_grid_layout(image_paths)
            
            self.current_image_layout = layout
        
        def _reset_image_layout():
            """Reset to single image layout"""
            if self.current_image_layout != "single":
                _clear_image_area()
                # Recreate single image label
                self.image_label = tk.Label(self.image_frame, bg='#1a1a1a')
                self.image_label.pack(expand=True)
                self.image_labels = [self.image_label]
                self.current_image_layout = "single"
        
        def _clear_image_area():
            """Clear all image widgets from the image frame"""
            for widget in self.image_frame.winfo_children():
                widget.destroy()
            self.image_labels.clear()
        
        def _create_horizontal_layout(image_paths):
            """Create horizontal layout for multiple images"""
            for i, image_path in enumerate(image_paths):
                label = tk.Label(self.image_frame, bg='#1a1a1a')
                label.pack(side=tk.LEFT, expand=True, padx=2)
                self.image_labels.append(label)
                _load_image_to_label(image_path, label, (180, 200))
        
        def _create_vertical_layout(image_paths):
            """Create vertical layout for multiple images"""
            for i, image_path in enumerate(image_paths):
                label = tk.Label(self.image_frame, bg='#1a1a1a')
                label.pack(side=tk.TOP, expand=True, pady=2)
                self.image_labels.append(label)
                _load_image_to_label(image_path, label, (350, 120))
        
        def _create_grid_layout(image_paths):
            """Create grid layout for multiple images"""
            import math
            
            # Calculate grid dimensions
            num_images = len(image_paths)
            cols = min(3, num_images)  # Max 3 columns
            rows = math.ceil(num_images / cols)
            
            # Create grid
            for i, image_path in enumerate(image_paths):
                row = i // cols
                col = i % cols
                
                label = tk.Label(self.image_frame, bg='#1a1a1a')
                label.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
                self.image_labels.append(label)
                
                # Configure grid weights for even distribution
                self.image_frame.grid_rowconfigure(row, weight=1)
                self.image_frame.grid_columnconfigure(col, weight=1)
                
                # Smaller images for grid layout
                _load_image_to_label(image_path, label, (120, 80))
        
        def _load_image_to_label(image_path, label, size=(200, 150)):
            """Load an image into a specific label with given size"""
            try:
                # Handle text files (ASCII art)
                if image_path.endswith('.txt'):
                    with open(image_path, 'r', encoding='utf-8') as f:
                        ascii_art = f.read()
                    label.config(text=ascii_art, font=('Courier', 6), fg='#00ff00', bg='#1a1a1a')
                    return
                
                # Handle image files
                img = Image.open(image_path)
                img.thumbnail(size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo, text='')
                label.image = photo  # Keep a reference
            except Exception as e:
                label.config(text=f"Error:\n{image_path}\n{str(e)}", fg='#ff0000', bg='#1a1a1a')
        
        # Bind methods to self
        self.show_image = show_image
        self.show_images = show_images
    
    def run(self):
        """Run the test"""
        self.print_text("Multiple Image Display Test")
        self.print_text("=" * 40)
        self.print_text("Click buttons to test different layouts:")
        self.print_text("- Single Image: Traditional display")
        self.print_text("- Two Horizontal: Side by side")
        self.print_text("- Grid 2x2: Four images in grid")
        self.print_text("- Auto Layout: Smart layout selection")
        self.print_text("- Show List: Backwards compatibility")
        self.print_text("")
        
        # Start with single image
        self.root.after(500, self.test_single)
        
        self.root.mainloop()

if __name__ == '__main__':
    tester = MultiImageTester()
    tester.run()