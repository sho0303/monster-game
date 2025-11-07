"""
Create a pixel art crossed swords icon
"""
from PIL import Image
import numpy as np

def create_crossed_swords():
    """Create pixel art crossed swords"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    SILVER = [192, 192, 192, 255]        # Blade
    LIGHT_SILVER = [220, 220, 220, 255]  # Blade highlight
    DARK_SILVER = [140, 140, 140, 255]   # Blade shadow
    GOLD = [255, 215, 0, 255]            # Hilt
    DARK_GOLD = [200, 160, 0, 255]       # Hilt shadow
    BROWN = [101, 67, 33, 255]           # Handle
    DARK_BROWN = [70, 45, 20, 255]       # Handle shadow
    RED = [180, 0, 0, 255]               # Gem accent
    
    # FIRST SWORD (top-left to bottom-right diagonal)
    # Handle (bottom-left)
    for i in range(6):
        x = 8 + i
        y = 26 - i
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BROWN
            # Handle shadow
            if x + 1 < size:
                canvas[y][x + 1] = DARK_BROWN
    
    # Guard/crossguard (horizontal)
    for i in range(-2, 3):
        x = 13 + i
        y = 21
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD
            canvas[y + 1][x] = DARK_GOLD
    
    # Pommel (end of handle)
    canvas[27][7] = RED
    canvas[27][8] = RED
    canvas[28][7] = DARK_GOLD
    
    # Blade (diagonal from guard to top-right)
    for i in range(15):
        x = 14 + i
        y = 20 - i
        if 0 <= x < size and 0 <= y < size:
            # Main blade (2 pixels wide)
            canvas[y][x] = SILVER
            if x + 1 < size:
                canvas[y][x + 1] = LIGHT_SILVER
            # Blade edge/shadow
            if y + 1 < size:
                canvas[y + 1][x] = DARK_SILVER
    
    # Blade tip (pointed)
    canvas[5][28] = SILVER
    canvas[4][29] = LIGHT_SILVER
    canvas[3][30] = DARK_SILVER
    
    # SECOND SWORD (top-right to bottom-left diagonal)
    # Handle (bottom-right)
    for i in range(6):
        x = 23 - i
        y = 26 - i
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BROWN
            # Handle shadow
            if x - 1 >= 0:
                canvas[y][x - 1] = DARK_BROWN
    
    # Guard/crossguard (horizontal)
    for i in range(-2, 3):
        x = 18 + i
        y = 21
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD
            canvas[y + 1][x] = DARK_GOLD
    
    # Pommel (end of handle)
    canvas[27][23] = RED
    canvas[27][24] = RED
    canvas[28][24] = DARK_GOLD
    
    # Blade (diagonal from guard to top-left)
    for i in range(15):
        x = 17 - i
        y = 20 - i
        if 0 <= x < size and 0 <= y < size:
            # Main blade (2 pixels wide)
            canvas[y][x] = SILVER
            if x - 1 >= 0:
                canvas[y][x - 1] = LIGHT_SILVER
            # Blade edge/shadow
            if y + 1 < size:
                canvas[y + 1][x] = DARK_SILVER
    
    # Blade tip (pointed)
    canvas[5][3] = SILVER
    canvas[4][2] = LIGHT_SILVER
    canvas[3][1] = DARK_SILVER
    
    # Add intersection glow/highlight where swords cross
    canvas[21][15] = LIGHT_SILVER
    canvas[21][16] = LIGHT_SILVER
    canvas[20][15] = LIGHT_SILVER
    canvas[20][16] = LIGHT_SILVER
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/crossed_swords.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art crossed swords")
    print(f"   Features: Silver blades, gold hilts, brown handles, red gems")

if __name__ == '__main__':
    create_crossed_swords()
