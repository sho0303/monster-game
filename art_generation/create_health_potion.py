"""
Create a pixel art magic health potion PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_health_potion():
    """Create a Minecraft-style magic health potion"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    RED = [220, 20, 60, 255]         # Main potion color (health red)
    DARK_RED = [139, 0, 0, 255]      # Potion shading
    LIGHT_RED = [255, 105, 180, 255] # Potion highlights
    BRIGHT_RED = [255, 0, 0, 255]    # Magical glow
    GLASS = [200, 220, 255, 255]     # Glass bottle
    DARK_GLASS = [150, 170, 200, 255] # Glass shading
    LIGHT_GLASS = [240, 250, 255, 255] # Glass highlights
    WHITE = [255, 255, 255, 255]     # Bright reflections
    CORK = [160, 82, 45, 255]        # Cork stopper
    DARK_CORK = [101, 67, 33, 255]   # Cork shading
    LIGHT_CORK = [205, 133, 63, 255] # Cork highlights
    GOLD = [255, 215, 0, 255]        # Label/seal
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    SILVER = [192, 192, 192, 255]    # Metal details
    PINK = [255, 182, 193, 255]      # Magical sparkles
    MAGENTA = [255, 0, 255, 255]     # Magical effects
    
    # BOTTLE SHAPE (classic potion bottle silhouette)
    bottle_center_x = 16
    bottle_bottom_y = 28
    bottle_top_y = 8
    bottle_width = 4
    
    # Main bottle body (bulbous shape)
    for y in range(bottle_top_y + 4, bottle_bottom_y):
        # Bottle gets wider in the middle, narrower at top and bottom
        if y < bottle_top_y + 8:  # Upper section
            width = bottle_width - 1
        elif y < bottle_top_y + 16:  # Middle section (widest)
            width = bottle_width + 1
        else:  # Lower section
            width = bottle_width
        
        for x in range(bottle_center_x - width, bottle_center_x + width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = GLASS
    
    # Bottle neck (narrow top section)
    neck_width = 2
    for y in range(bottle_top_y, bottle_top_y + 4):
        for x in range(bottle_center_x - neck_width, bottle_center_x + neck_width + 1):
            canvas[y][x] = GLASS
    
    # POTION LIQUID (fills most of the bottle)
    liquid_top_y = bottle_top_y + 5
    liquid_bottom_y = bottle_bottom_y - 2
    
    # Main potion liquid
    for y in range(liquid_top_y, liquid_bottom_y):
        # Follow bottle shape but slightly smaller
        if y < bottle_top_y + 8:
            width = bottle_width - 2
        elif y < bottle_top_y + 16:
            width = bottle_width
        else:
            width = bottle_width - 1
        
        for x in range(bottle_center_x - width, bottle_center_x + width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = RED
    
    # Potion surface (slightly curved meniscus)
    surface_y = liquid_top_y
    canvas[surface_y][bottle_center_x - 1] = LIGHT_RED
    canvas[surface_y][bottle_center_x] = BRIGHT_RED
    canvas[surface_y][bottle_center_x + 1] = LIGHT_RED
    
    # Potion shading (left side darker)
    for y in range(liquid_top_y + 1, liquid_bottom_y):
        if y < bottle_top_y + 8:
            width = bottle_width - 2
        elif y < bottle_top_y + 16:
            width = bottle_width
        else:
            width = bottle_width - 1
        
        # Left side shading
        if bottle_center_x - width >= 0:
            canvas[y][bottle_center_x - width] = DARK_RED
        # Right side highlights
        if bottle_center_x + width < size:
            canvas[y][bottle_center_x + width] = LIGHT_RED
    
    # CORK STOPPER
    cork_y = bottle_top_y - 2
    cork_width = 2
    
    # Main cork body
    for y in range(cork_y, bottle_top_y + 1):
        for x in range(bottle_center_x - cork_width, bottle_center_x + cork_width + 1):
            canvas[y][x] = CORK
    
    # Cork shading and highlights
    for y in range(cork_y, bottle_top_y + 1):
        canvas[y][bottle_center_x - cork_width] = DARK_CORK
        canvas[y][bottle_center_x + cork_width] = LIGHT_CORK
        canvas[y][bottle_center_x] = LIGHT_CORK
    
    # Cork top (slightly wider)
    canvas[cork_y][bottle_center_x - cork_width - 1] = CORK
    canvas[cork_y][bottle_center_x + cork_width + 1] = CORK
    
    # BOTTLE DETAILS
    # Glass shading (left side darker)
    for y in range(bottle_top_y, bottle_bottom_y):
        # Bottle outline shading
        if y < bottle_top_y + 4:  # Neck
            width = neck_width
        elif y < bottle_top_y + 8:
            width = bottle_width - 1
        elif y < bottle_top_y + 16:
            width = bottle_width + 1
        else:
            width = bottle_width
        
        # Left edge shading
        if bottle_center_x - width - 1 >= 0:
            canvas[y][bottle_center_x - width - 1] = DARK_GLASS
        # Right edge highlights
        if bottle_center_x + width + 1 < size:
            canvas[y][bottle_center_x + width + 1] = LIGHT_GLASS
    
    # Glass reflections (bright spots)
    reflection_positions = [
        (bottle_top_y + 6, bottle_center_x - 2),
        (bottle_top_y + 10, bottle_center_x - 3),
        (bottle_top_y + 14, bottle_center_x - 2),
    ]
    
    for refl_y, refl_x in reflection_positions:
        if 0 <= refl_y < size and 0 <= refl_x < size:
            canvas[refl_y][refl_x] = WHITE
    
    # LABEL/SEAL
    label_y = bottle_top_y + 12
    label_width = 3
    
    # Golden label background
    for y in range(label_y, label_y + 4):
        for x in range(bottle_center_x - label_width, bottle_center_x + label_width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = GOLD
    
    # Label shading
    canvas[label_y][bottle_center_x - label_width] = DARK_GOLD
    canvas[label_y + 3][bottle_center_x - label_width] = DARK_GOLD
    
    # Health cross symbol on label (classic health potion marking)
    cross_center_x = bottle_center_x
    cross_center_y = label_y + 2
    
    # Vertical line of cross
    canvas[cross_center_y - 1][cross_center_x] = WHITE
    canvas[cross_center_y][cross_center_x] = WHITE
    canvas[cross_center_y + 1][cross_center_x] = WHITE
    
    # Horizontal line of cross
    canvas[cross_center_y][cross_center_x - 1] = WHITE
    canvas[cross_center_y][cross_center_x + 1] = WHITE
    
    # MAGICAL EFFECTS
    # Bubbles in the potion (active magic)
    bubble_positions = [
        (liquid_top_y + 3, bottle_center_x - 1),
        (liquid_top_y + 8, bottle_center_x + 1),
        (liquid_top_y + 12, bottle_center_x),
        (liquid_top_y + 16, bottle_center_x - 2),
    ]
    
    for bubble_y, bubble_x in bubble_positions:
        if 0 <= bubble_y < size and 0 <= bubble_x < size:
            canvas[bubble_y][bubble_x] = PINK
    
    # Magical aura around bottle
    aura_positions = [
        (bottle_top_y + 2, bottle_center_x - 4),
        (bottle_top_y + 6, bottle_center_x + 5),
        (bottle_top_y + 12, bottle_center_x - 6),
        (bottle_top_y + 16, bottle_center_x + 6),
        (bottle_top_y + 20, bottle_center_x - 5),
    ]
    
    for aura_y, aura_x in aura_positions:
        if 0 <= aura_y < size and 0 <= aura_x < size:
            canvas[aura_y][aura_x] = MAGENTA
    
    # Sparkles (healing magic emanating)
    sparkle_positions = [
        (bottle_top_y - 1, bottle_center_x - 2),
        (bottle_top_y + 1, bottle_center_x + 3),
        (bottle_top_y + 8, bottle_center_x - 5),
        (bottle_top_y + 14, bottle_center_x + 4),
        (bottle_top_y + 18, bottle_center_x - 4),
        (bottle_top_y + 22, bottle_center_x + 5),
    ]
    
    for sparkle_y, sparkle_x in sparkle_positions:
        if 0 <= sparkle_y < size and 0 <= sparkle_x < size:
            canvas[sparkle_y][sparkle_x] = WHITE
    
    # Potion glow effect (emanating health energy)
    glow_positions = [
        (bottle_top_y + 4, bottle_center_x - 3),
        (bottle_top_y + 10, bottle_center_x + 4),
        (bottle_top_y + 16, bottle_center_x - 4),
        (bottle_top_y + 20, bottle_center_x + 3),
    ]
    
    for glow_y, glow_x in glow_positions:
        if 0 <= glow_y < size and 0 <= glow_x < size:
            canvas[glow_y][glow_x] = LIGHT_RED
    
    # BOTTLE BASE (slight thickening at bottom)
    base_y = bottle_bottom_y
    for x in range(bottle_center_x - bottle_width - 1, bottle_center_x + bottle_width + 2):
        if x >= 0 and x < size and base_y < size:
            canvas[base_y][x] = DARK_GLASS
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'ascii_art/health_potion.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art magic health potion with mystical effects")
    print(f"   Features: Glass bottle, red healing liquid, cork stopper")
    print(f"   Details: Health cross label, magical bubbles, glass reflections")
    print(f"   Magic: Sparkles, aura glow, healing energy emanation")

if __name__ == '__main__':
    create_health_potion()