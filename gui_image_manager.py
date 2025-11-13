"""
GUI Image & Layout Manager

Handles all image display, layout, and canvas management functionality.
Extracted from gui_main.py to reduce complexity and improve maintainability.
"""

import tkinter as tk
from PIL import Image, ImageTk

import config
from logger_utils import get_logger

logger = get_logger(__name__)


class ImageManager:
    """
    Manages image display, layout, and canvas operations for the Monster Game GUI.
    
    This class handles:
    - Single and multiple image display
    - Dynamic layout positioning (horizontal, vertical, grid)
    - Canvas image management and cleanup
    - ASCII art text rendering
    - Foreground/background image layering
    """
    
    def __init__(self, image_canvas, print_text_callback=None):
        """
        Initialize the Image Manager.
        
        Args:
            image_canvas: The tkinter Canvas widget for image display
            print_text_callback: Function to call for error messages (optional)
        """
        self.image_canvas = image_canvas
        self.canvas_images = []  # Keep references to prevent garbage collection
        self.current_image_layout = "single"
        self.print_text = print_text_callback or self._default_print_text
        
    def _default_print_text(self, text, color='#ff0000'):
        """Default print function if none provided"""
        logger.warning(f"ImageManager: {text}")
    
    def show_image(self, image_path):
        """Display a single image using canvas for proper background compositing"""
        if isinstance(image_path, list):
            # If a list is passed, use show_images instead
            self.show_images(image_path)
            return
            
        # Clear existing foreground images
        self.clear_foreground_images()
        
        try:
            # Get current canvas dimensions
            canvas_width, canvas_height = self.get_canvas_dimensions()
            
            # Handle text files (ASCII art) - convert to image or display as text
            if image_path.endswith('.txt'):
                with open(image_path, 'r', encoding='utf-8') as f:
                    ascii_art = f.read()
                # Create text on canvas (centered)
                self.image_canvas.create_text(canvas_width//2, canvas_height//2, text=ascii_art, 
                                            fill='#00ff00', font=('Courier', 8), 
                                            anchor='center', tags='foreground')
                return
            
            # Handle image files - center the image on the canvas at natural size
            # First, get the original image dimensions
            with Image.open(image_path) as img:
                img_width, img_height = img.size
            
            # Calculate center position based on actual canvas size
            center_x = (canvas_width - img_width) // 2
            center_y = (canvas_height - img_height) // 2
            # Use natural size (don't pass width/height to avoid resizing)
            self.add_canvas_image(image_path, center_x, center_y)
            
        except Exception as e:
            logger.error(f"Could not load image '{image_path}': {e}")
            self.print_text(f"Could not load image: {e}")
    
    def show_images(self, image_paths, layout="auto"):
        """Display multiple images using canvas for proper background compositing
        
        Args:
            image_paths: List of image file paths
            layout: "horizontal", "vertical", "grid", or "auto" (default)
        """
        if not image_paths:
            return
        
        # If single image, fall back to show_image
        if len(image_paths) == 1:
            self.show_image(image_paths[0])
            return
        
        # Clear existing images
        self.clear_foreground_images()
        
        # Get current canvas dimensions for dynamic positioning
        canvas_width, canvas_height = self.get_canvas_dimensions()
        
        # Determine layout and positions based on number of images and canvas size
        num_images = len(image_paths)
        
        if num_images == 2:
            # Side by side
            img_size = min(canvas_width // 3, canvas_height // 2, 120)
            spacing_x = canvas_width // 3
            start_y = (canvas_height - img_size) // 2
            positions = [(spacing_x - img_size//2, start_y), (2*spacing_x - img_size//2, start_y)]
            size = (img_size, img_size)
        elif num_images == 3:
            # Triangle layout
            img_size = min(canvas_width // 4, canvas_height // 3, 100)
            center_x = canvas_width // 2
            positions = [(center_x - img_size//2, 20), 
                        (center_x//2 - img_size//2, canvas_height - img_size - 20), 
                        (3*center_x//2 - img_size//2, canvas_height - img_size - 20)]
            size = (img_size, img_size)
        elif num_images == 4:
            # 2x2 grid
            img_size = min(canvas_width // 3, canvas_height // 3, 100)
            spacing_x = canvas_width // 3
            spacing_y = canvas_height // 2
            positions = [(spacing_x//2, spacing_y//2 - img_size//2), 
                        (3*spacing_x//2, spacing_y//2 - img_size//2),
                        (spacing_x//2, 3*spacing_y//2 - img_size//2), 
                        (3*spacing_x//2, 3*spacing_y//2 - img_size//2)]
            size = (img_size, img_size)
        else:
            # Grid layout for more images
            cols = 3 if num_images <= 6 else 4
            rows = (num_images + cols - 1) // cols
            img_size = min(canvas_width // (cols + 1), canvas_height // (rows + 1), 80)
            
            positions = []
            spacing_x = canvas_width // (cols + 1)
            spacing_y = canvas_height // (rows + 1)
            
            for i in range(num_images):
                row = i // cols
                col = i % cols
                x = (col + 1) * spacing_x - img_size // 2
                y = (row + 1) * spacing_y - img_size // 2
                positions.append((x, y))
            size = (img_size, img_size)
        
        # Place images on canvas
        for i, image_path in enumerate(image_paths[:len(positions)]):
            x, y = positions[i]
            self.add_canvas_image(image_path, x, y, size[0], size[1])
        
        self.current_image_layout = layout
    
    def add_canvas_image(self, image_path, x, y, width=None, height=None, tags="foreground"):
        """Add an image to the canvas at the specified position
        
        Args:
            image_path: Path to the image file
            x, y: Position on canvas
            width, height: Target size (if None, uses natural image size)
            tags: Canvas tags for the image
            
        Returns:
            Canvas item ID or None if failed
        """
        try:
            # Load image
            img = Image.open(image_path)
            
            # Resize only if dimensions are specified
            if width is not None and height is not None:
                img = img.resize((width, height), Image.Resampling.NEAREST)
            
            photo = ImageTk.PhotoImage(img)
            
            # Add to canvas
            canvas_id = self.image_canvas.create_image(x, y, image=photo, anchor='nw', tags=tags)
            
            # Keep reference to prevent garbage collection
            self.canvas_images.append(photo)
            
            return canvas_id
            
        except Exception as e:
            logger.error(f"Failed to add canvas image '{image_path}': {e}")
            self.print_text(f"Failed to add canvas image {image_path}: {e}")
            return None
    
    def clear_foreground_images(self):
        """Clear all foreground images from canvas"""
        self.image_canvas.delete("foreground")
        self.canvas_images.clear()
    
    def show_story_text(self, text_lines, font_size=24, text_color='#ffffff', 
                       shadow_color='#000000', line_spacing=40):
        """
        Display story text overlaid on the canvas foreground
        
        Args:
            text_lines: List of text strings to display (one per line)
            font_size: Size of the font (default: 24)
            text_color: Color of the text (default: white)
            shadow_color: Color of text shadow for readability (default: black)
            line_spacing: Vertical spacing between lines in pixels (default: 40)
        """
        # Clear existing foreground content
        self.clear_foreground_images()
        
        # Get canvas dimensions
        canvas_width, canvas_height = self.get_canvas_dimensions()
        
        # Calculate starting Y position to center the text block vertically
        total_text_height = len(text_lines) * line_spacing
        start_y = (canvas_height - total_text_height) // 2
        
        # Display each line of text
        for i, line in enumerate(text_lines):
            y_pos = start_y + (i * line_spacing)
            
            # Draw text shadow first (for readability against any background)
            self.image_canvas.create_text(
                canvas_width // 2 + 2, 
                y_pos + 2, 
                text=line,
                fill=shadow_color,
                font=('Arial', font_size, 'bold'),
                anchor='center',
                tags='foreground'
            )
            
            # Draw main text
            self.image_canvas.create_text(
                canvas_width // 2, 
                y_pos, 
                text=line,
                fill=text_color,
                font=('Arial', font_size, 'bold'),
                anchor='center',
                tags='foreground'
            )
    
    def clear_image_area(self):
        """Clear all foreground images from canvas, preserving background"""
        self.clear_foreground_images()
        
        # Note: Background handling is managed by BackgroundManager
        # This method focuses only on foreground image cleanup
    
    def reset_image_layout(self):
        """Reset to single image layout using canvas"""
        self.clear_foreground_images()
        self.current_image_layout = "single"
    
    def get_canvas_dimensions(self):
        """Get fixed canvas dimensions
        
        Returns:
            Tuple of (width, height) in pixels
        """
        # Return fixed canvas dimensions (no dynamic sizing)
        return config.CANVAS_WIDTH, config.CANVAS_HEIGHT
    
    def get_current_layout(self):
        """Get the current image layout mode
        
        Returns:
            String indicating current layout: "single", "auto", etc.
        """
        return self.current_image_layout
    
    def set_layout(self, layout):
        """Set the current image layout mode
        
        Args:
            layout: Layout string ("single", "auto", "horizontal", "vertical", "grid")
        """
        self.current_image_layout = layout
    
    # Legacy methods for backwards compatibility (now no-ops)
    def create_horizontal_layout(self, image_paths):
        """Legacy method - now handled by show_images canvas approach"""
        pass
    
    def create_vertical_layout(self, image_paths):
        """Legacy method - now handled by show_images canvas approach"""
        pass
    
    def create_grid_layout(self, image_paths):
        """Legacy method - now handled by show_images canvas approach"""
        pass
    
    def load_image_to_label(self, image_path, label, size=(200, 150)):
        """Legacy method - now using canvas for image display"""
        pass