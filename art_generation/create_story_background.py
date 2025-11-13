"""
Create an attractive background for story text display
"""
from PIL import Image, ImageDraw
import numpy as np

def create_story_background():
    """Create a visually appealing background for story text"""
    # Create canvas matching game canvas size
    width = 800
    height = 400
    
    # Create image with RGB mode
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create a dark gradient background (top to bottom)
    for y in range(height):
        # Gradient from dark blue-purple at top to darker at bottom
        progress = y / height
        
        # Dark mystical colors
        r = int(20 + (30 - 20) * progress)
        g = int(10 + (20 - 10) * progress)
        b = int(40 + (50 - 40) * progress)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add some atmospheric stars/sparkles
    np.random.seed(42)  # For consistent star positions
    num_stars = 100
    
    for _ in range(num_stars):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        size = np.random.choice([1, 2, 3])
        brightness = np.random.randint(150, 255)
        
        # Draw star as a small circle
        if size == 1:
            draw.point((x, y), fill=(brightness, brightness, brightness))
        elif size == 2:
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(brightness, brightness, 200))
        else:
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 200))
    
    # Add subtle vignette effect (darker edges)
    vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    
    # Draw darker rectangles at edges
    edge_darkness = 60
    edge_size = 80
    
    # Top edge
    for i in range(edge_size):
        alpha = int((edge_size - i) / edge_size * edge_darkness)
        vignette_draw.rectangle([0, i, width, i+1], fill=(0, 0, 0, alpha))
    
    # Bottom edge
    for i in range(edge_size):
        alpha = int((edge_size - i) / edge_size * edge_darkness)
        vignette_draw.rectangle([0, height-i-1, width, height-i], fill=(0, 0, 0, alpha))
    
    # Left edge
    for i in range(edge_size):
        alpha = int((edge_size - i) / edge_size * edge_darkness)
        vignette_draw.rectangle([i, 0, i+1, height], fill=(0, 0, 0, alpha))
    
    # Right edge
    for i in range(edge_size):
        alpha = int((edge_size - i) / edge_size * edge_darkness)
        vignette_draw.rectangle([width-i-1, 0, width-i, height], fill=(0, 0, 0, alpha))
    
    # Composite vignette onto main image
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, vignette)
    img = img_rgba.convert('RGB')
    
    # Add some subtle horizontal lines for a "parchment" or "mystical" feel
    draw = ImageDraw.Draw(img)
    for i in range(0, height, 40):
        # Very subtle lines
        draw.line([(0, i), (width, i)], fill=(40, 30, 60), width=1)
    
    # Save the image
    output_path = 'art/story_background.png'
    img.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width}x{height} pixels")
    print(f"   Style: Dark mystical gradient with stars")
    print(f"   Features: Blue-purple gradient, starfield, vignette edges, subtle texture")

if __name__ == '__main__':
    create_story_background()
