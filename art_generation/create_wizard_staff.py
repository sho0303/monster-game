"""
Create a pixel art wizard's staff PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_wizard_staff():
    """Create a Minecraft-style wizard's staff"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BROWN = [101, 67, 33, 255]       # Wood staff
    DARK_BROWN = [60, 40, 20, 255]   # Dark wood shading
    LIGHT_BROWN = [139, 90, 43, 255] # Light wood highlights
    PURPLE = [128, 0, 128, 255]      # Magic crystal
    DARK_PURPLE = [75, 0, 75, 255]   # Crystal shading
    LIGHT_PURPLE = [200, 100, 200, 255] # Crystal highlights
    BLUE = [0, 100, 255, 255]        # Magic glow
    LIGHT_BLUE = [100, 200, 255, 255] # Bright glow
    WHITE = [255, 255, 255, 255]     # Sparkles
    GOLD = [255, 215, 0, 255]        # Golden accents
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    SILVER = [192, 192, 192, 255]    # Metal bands
    
    # STAFF SHAFT (main wooden pole, vertical through center)
    staff_x = 15  # Center column
    staff_start_y = 8
    staff_end_y = 28
    
    # Main wooden shaft
    for y in range(staff_start_y, staff_end_y):
        canvas[y][staff_x] = BROWN
        canvas[y][staff_x + 1] = BROWN
    
    # Add wood grain and shading
    for y in range(staff_start_y, staff_end_y, 3):
        if y < staff_end_y - 1:
            canvas[y][staff_x] = DARK_BROWN
            canvas[y + 1][staff_x + 1] = LIGHT_BROWN
    
    # Silver metal bands around staff
    for band_y in [12, 18, 24]:
        canvas[band_y][staff_x] = SILVER
        canvas[band_y][staff_x + 1] = SILVER
        canvas[band_y + 1][staff_x] = SILVER
        canvas[band_y + 1][staff_x + 1] = SILVER
    
    # CRYSTAL ORB (top of staff)
    orb_center_x = 15
    orb_center_y = 6
    orb_size = 3
    
    # Create crystal orb (diamond-like shape)
    # Top point
    canvas[orb_center_y - 2][orb_center_x] = PURPLE
    canvas[orb_center_y - 2][orb_center_x + 1] = PURPLE
    
    # Upper section
    for x in range(orb_center_x - 1, orb_center_x + 3):
        canvas[orb_center_y - 1][x] = PURPLE
    
    # Middle section (widest part)
    for x in range(orb_center_x - 2, orb_center_x + 4):
        canvas[orb_center_y][x] = PURPLE
    for x in range(orb_center_x - 2, orb_center_x + 4):
        canvas[orb_center_y + 1][x] = PURPLE
    
    # Lower section
    for x in range(orb_center_x - 1, orb_center_x + 3):
        canvas[orb_center_y + 2][x] = PURPLE
    
    # Crystal highlights and depth
    canvas[orb_center_y - 1][orb_center_x] = LIGHT_PURPLE
    canvas[orb_center_y][orb_center_x - 1] = DARK_PURPLE
    canvas[orb_center_y][orb_center_x + 3] = DARK_PURPLE
    canvas[orb_center_y + 1][orb_center_x] = LIGHT_PURPLE
    canvas[orb_center_y + 1][orb_center_x + 1] = LIGHT_PURPLE
    
    # GOLDEN STAFF HEAD (ornate mounting for crystal)
    head_y = 8
    
    # Golden prongs/claws holding the crystal
    canvas[head_y][orb_center_x - 3] = GOLD  # Left prong
    canvas[head_y][orb_center_x + 4] = GOLD  # Right prong
    canvas[head_y + 1][orb_center_x - 2] = GOLD
    canvas[head_y + 1][orb_center_x + 3] = GOLD
    canvas[head_y + 2][orb_center_x - 1] = DARK_GOLD
    canvas[head_y + 2][orb_center_x + 2] = DARK_GOLD
    
    # Golden base ring
    for x in range(orb_center_x - 1, orb_center_x + 3):
        canvas[head_y + 3][x] = GOLD
    canvas[head_y + 3][orb_center_x - 2] = DARK_GOLD
    canvas[head_y + 3][orb_center_x + 3] = DARK_GOLD
    
    # MAGIC EFFECTS
    # Sparkles around the crystal
    sparkle_positions = [
        (orb_center_y - 3, orb_center_x - 2),
        (orb_center_y - 3, orb_center_x + 3),
        (orb_center_y - 1, orb_center_x - 3),
        (orb_center_y - 1, orb_center_x + 4),
        (orb_center_y + 1, orb_center_x - 4),
        (orb_center_y + 1, orb_center_x + 5),
        (orb_center_y + 3, orb_center_x - 2),
        (orb_center_y + 3, orb_center_x + 3),
    ]
    
    for spark_y, spark_x in sparkle_positions:
        if 0 <= spark_y < size and 0 <= spark_x < size:
            canvas[spark_y][spark_x] = WHITE
    
    # Blue magic glow
    glow_positions = [
        (orb_center_y - 2, orb_center_x - 1),
        (orb_center_y - 2, orb_center_x + 2),
        (orb_center_y, orb_center_x - 3),
        (orb_center_y, orb_center_x + 4),
        (orb_center_y + 2, orb_center_x - 1),
        (orb_center_y + 2, orb_center_x + 2),
    ]
    
    for glow_y, glow_x in glow_positions:
        if 0 <= glow_y < size and 0 <= glow_x < size:
            canvas[glow_y][glow_x] = LIGHT_BLUE
    
    # STAFF BOTTOM (pointed end)
    bottom_y = staff_end_y
    if bottom_y < size - 2:
        canvas[bottom_y][staff_x] = DARK_BROWN
        canvas[bottom_y][staff_x + 1] = DARK_BROWN
        canvas[bottom_y + 1][staff_x] = DARK_BROWN
        canvas[bottom_y + 1][staff_x + 1] = DARK_BROWN
        
        # Pointed tip
        if bottom_y + 2 < size:
            canvas[bottom_y + 2][staff_x] = DARK_BROWN
            canvas[bottom_y + 2][staff_x + 1] = DARK_BROWN
    
    # ADDITIONAL MAGICAL RUNES (carved into staff)
    rune_positions = [
        (15, staff_x - 1),  # Left side runes
        (20, staff_x - 1),
        (26, staff_x - 1),
        (16, staff_x + 2),  # Right side runes  
        (22, staff_x + 2),
        (28, staff_x + 2),
    ]
    
    for rune_y, rune_x in rune_positions:
        if 0 <= rune_y < size and 0 <= rune_x < size:
            canvas[rune_y][rune_x] = BLUE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/wizard_staff.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art wizard's staff with crystal orb")
    print(f"   Features: Purple crystal, golden claws, wooden shaft, magic sparkles")
    print(f"   Magic effects: Blue runes, white sparkles, glowing aura")

if __name__ == '__main__':
    create_wizard_staff()