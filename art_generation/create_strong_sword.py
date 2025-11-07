"""
Create a pixel art strong sword PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_strong_sword():
    """Create a Minecraft-style strong sword"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    STEEL = [192, 192, 192, 255]     # Main blade
    DARK_STEEL = [128, 128, 128, 255] # Blade shading
    LIGHT_STEEL = [230, 230, 230, 255] # Blade highlights
    GOLD = [255, 215, 0, 255]        # Golden hilt
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    LIGHT_GOLD = [255, 255, 100, 255] # Gold highlights
    RUBY = [139, 0, 0, 255]          # Ruby gem
    DARK_RUBY = [100, 0, 0, 255]     # Ruby shading
    LIGHT_RUBY = [220, 50, 50, 255]  # Ruby highlights
    BROWN = [101, 67, 33, 255]       # Leather grip
    DARK_BROWN = [60, 40, 20, 255]   # Leather shading
    BLACK = [0, 0, 0, 255]           # Outline/details
    WHITE = [255, 255, 255, 255]     # Shine effects
    
    # BLADE (main sword blade, vertical)
    blade_center_x = 16
    blade_start_y = 2
    blade_end_y = 20
    blade_width = 3
    
    # Main blade body (wide steel blade)
    for y in range(blade_start_y, blade_end_y):
        for x in range(blade_center_x - blade_width, blade_center_x + blade_width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = STEEL
    
    # Blade point (tapered tip)
    # Top point
    canvas[blade_start_y][blade_center_x] = STEEL
    
    # Tapered edges near tip
    canvas[blade_start_y + 1][blade_center_x - 1] = STEEL
    canvas[blade_start_y + 1][blade_center_x + 1] = STEEL
    canvas[blade_start_y + 2][blade_center_x - 2] = STEEL
    canvas[blade_start_y + 2][blade_center_x + 2] = STEEL
    
    # Blade shading (left side darker, right side lighter)
    for y in range(blade_start_y + 3, blade_end_y):
        # Dark shading on left
        canvas[y][blade_center_x - blade_width] = DARK_STEEL
        if blade_center_x - blade_width + 1 >= 0:
            canvas[y][blade_center_x - blade_width + 1] = DARK_STEEL
        
        # Light highlights on right
        canvas[y][blade_center_x + blade_width] = LIGHT_STEEL
        if blade_center_x + blade_width - 1 < size:
            canvas[y][blade_center_x + blade_width - 1] = LIGHT_STEEL
    
    # Central fuller (blood groove) for strength
    for y in range(blade_start_y + 4, blade_end_y - 2):
        canvas[y][blade_center_x] = DARK_STEEL
    
    # Blade edge highlights (sharp gleaming edges)
    for y in range(blade_start_y + 3, blade_end_y):
        # Left edge shine
        if blade_center_x - blade_width - 1 >= 0:
            canvas[y][blade_center_x - blade_width - 1] = WHITE
        # Right edge shine  
        if blade_center_x + blade_width + 1 < size:
            canvas[y][blade_center_x + blade_width + 1] = WHITE
    
    # CROSSGUARD (horizontal guard)
    guard_y = blade_end_y
    guard_width = 6
    
    # Main crossguard body
    for x in range(blade_center_x - guard_width, blade_center_x + guard_width + 1):
        if x >= 0 and x < size:
            canvas[guard_y][x] = GOLD
            canvas[guard_y + 1][x] = GOLD
    
    # Crossguard shading
    canvas[guard_y][blade_center_x - guard_width] = DARK_GOLD
    canvas[guard_y][blade_center_x + guard_width] = DARK_GOLD
    canvas[guard_y + 1][blade_center_x - guard_width] = DARK_GOLD
    canvas[guard_y + 1][blade_center_x + guard_width] = DARK_GOLD
    
    # Crossguard highlights
    canvas[guard_y][blade_center_x] = LIGHT_GOLD
    canvas[guard_y + 1][blade_center_x] = LIGHT_GOLD
    
    # Ornate crossguard ends (flared tips)
    canvas[guard_y][blade_center_x - guard_width - 1] = DARK_GOLD
    canvas[guard_y][blade_center_x + guard_width + 1] = DARK_GOLD
    canvas[guard_y - 1][blade_center_x - guard_width] = GOLD
    canvas[guard_y - 1][blade_center_x + guard_width] = GOLD
    
    # GRIP/HANDLE
    grip_start_y = guard_y + 2
    grip_end_y = grip_start_y + 5
    
    # Main grip (leather-wrapped)
    for y in range(grip_start_y, grip_end_y):
        canvas[y][blade_center_x - 1] = BROWN
        canvas[y][blade_center_x] = BROWN
        canvas[y][blade_center_x + 1] = BROWN
    
    # Leather grip texture (wrapped bands)
    for y in range(grip_start_y, grip_end_y, 2):
        canvas[y][blade_center_x - 1] = DARK_BROWN
        canvas[y][blade_center_x + 1] = DARK_BROWN
    
    # POMMEL (weighted end with gem)
    pommel_y = grip_end_y
    
    # Golden pommel base
    for x in range(blade_center_x - 2, blade_center_x + 3):
        canvas[pommel_y][x] = GOLD
        canvas[pommel_y + 1][x] = GOLD
    
    # Pommel shading
    canvas[pommel_y][blade_center_x - 2] = DARK_GOLD
    canvas[pommel_y][blade_center_x + 2] = DARK_GOLD
    canvas[pommel_y + 1][blade_center_x - 2] = DARK_GOLD
    canvas[pommel_y + 1][blade_center_x + 2] = DARK_GOLD
    
    # Central ruby gem in pommel
    canvas[pommel_y][blade_center_x] = RUBY
    canvas[pommel_y + 1][blade_center_x] = DARK_RUBY
    
    # Ruby highlight
    canvas[pommel_y][blade_center_x - 1] = LIGHT_RUBY
    
    # Pommel bottom (final weight)
    if pommel_y + 2 < size:
        canvas[pommel_y + 2][blade_center_x - 1] = DARK_GOLD
        canvas[pommel_y + 2][blade_center_x] = DARK_GOLD
        canvas[pommel_y + 2][blade_center_x + 1] = DARK_GOLD
    
    # DECORATIVE ELEMENTS
    # Blade runes/engravings for strength
    rune_positions = [
        (8, blade_center_x - 1),   # Left side runes
        (12, blade_center_x - 1),
        (16, blade_center_x - 1),
        (9, blade_center_x + 1),   # Right side runes
        (13, blade_center_x + 1),
        (17, blade_center_x + 1),
    ]
    
    for rune_y, rune_x in rune_positions:
        if 0 <= rune_y < size and 0 <= rune_x < size:
            canvas[rune_y][rune_x] = DARK_STEEL
    
    # Additional strength indicators (reinforcement lines)
    for y in range(blade_start_y + 5, blade_end_y - 3, 4):
        canvas[y][blade_center_x - 2] = LIGHT_STEEL
        canvas[y][blade_center_x + 2] = LIGHT_STEEL
    
    # Magical gleam effects (showing the sword's power)
    gleam_positions = [
        (blade_start_y + 1, blade_center_x - 2),
        (blade_start_y + 6, blade_center_x + 2),
        (blade_start_y + 11, blade_center_x - 2),
        (blade_start_y + 16, blade_center_x + 2),
    ]
    
    for gleam_y, gleam_x in gleam_positions:
        if 0 <= gleam_y < size and 0 <= gleam_x < size:
            canvas[gleam_y][gleam_x] = WHITE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/strong_sword.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art strong sword with detailed craftsmanship")
    print(f"   Features: Steel blade, golden crossguard, leather grip, ruby pommel")
    print(f"   Details: Fuller groove, runes, gleaming edges, reinforcement lines")

if __name__ == '__main__':
    create_strong_sword()