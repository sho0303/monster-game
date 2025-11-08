import tkinter as tk
from PIL import Image, ImageTk
import os

class TransparentImageCanvas:
    """A Canvas-based image display that properly handles background compositing"""
    
    def __init__(self, parent, width=512, height=256, background_image_path=None):
        self.parent = parent
        self.width = width
        self.height = height
        self.background_image = None
        self.foreground_objects = []  # Store references to canvas objects
        
        # Create the canvas
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            relief='flat',
            bd=0
        )
        
        # Load and set background image if provided
        if background_image_path and os.path.exists(background_image_path):
            self.set_background_image(background_image_path)
    
    def set_background_image(self, image_path):
        """Set the background image for the canvas"""
        try:
            # Load and resize background image
            bg_img = Image.open(image_path)
            bg_img = bg_img.resize((self.width, self.height), Image.Resampling.NEAREST)
            self.background_image = ImageTk.PhotoImage(bg_img)
            
            # Clear canvas and draw background
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.background_image, anchor='nw', tags="background")
            
        except Exception as e:
            print(f"Failed to set background image: {e}")
            # Set a solid background color as fallback
            self.canvas.configure(bg='#4a7c59')  # Forest green
    
    def add_image(self, image_path, x, y, width=None, height=None, tags="foreground"):
        """Add a foreground image to the canvas at specified position"""
        try:
            # Load the image
            img = Image.open(image_path)
            
            # Resize if dimensions provided
            if width and height:
                img = img.resize((width, height), Image.Resampling.NEAREST)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create canvas image object
            canvas_id = self.canvas.create_image(x, y, image=photo, anchor='nw', tags=tags)
            
            # Store reference to prevent garbage collection
            self.foreground_objects.append(photo)
            
            return canvas_id
            
        except Exception as e:
            print(f"Failed to add image {image_path}: {e}")
            return None
    
    def clear_foreground(self):
        """Clear all foreground images, keeping background"""
        self.canvas.delete("foreground")
        self.foreground_objects.clear()
    
    def pack(self, **kwargs):
        """Pack the canvas"""
        self.canvas.pack(**kwargs)
    
    def place(self, **kwargs):
        """Place the canvas"""
        self.canvas.place(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the canvas"""
        self.canvas.grid(**kwargs)

def test_transparent_canvas():
    """Test function for the transparent canvas"""
    root = tk.Tk()
    root.title("Transparent Canvas Test")
    root.geometry("600x400")
    
    # Create canvas with background
    canvas = TransparentImageCanvas(
        root, 
        width=512, 
        height=256,
        background_image_path="art/grassy_background.png"
    )
    canvas.pack(pady=20)
    
    # Add some test images if they exist
    test_images = [
        ("art/health_potion.png", 50, 50, 64, 64),
        ("art/magic_pouch.png", 150, 50, 64, 64),
    ]
    
    for img_path, x, y, w, h in test_images:
        if os.path.exists(img_path):
            canvas.add_image(img_path, x, y, w, h)
    
    # Add a test button to clear foreground
    def clear_fg():
        canvas.clear_foreground()
    
    clear_btn = tk.Button(root, text="Clear Foreground", command=clear_fg)
    clear_btn.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_transparent_canvas()