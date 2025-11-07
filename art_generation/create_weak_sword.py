"""
Create a pixel art weak thin sword PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_weak_sword():
    """Create a Minecraft-style weak thin sword"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette (cheaper, weaker materials)
    IRON = [160, 160, 160, 255]      # Main blade (duller than steel)
    DARK_IRON = [100, 100, 100, 255] # Blade shading
    LIGHT_IRON = [180, 180, 180, 255] # Blade highlights (less shine)
    BRONZE = [205, 127, 50, 255]     # Bronze hilt (cheaper than gold)
    DARK_BRONZE = [139, 69, 19, 255] # Bronze shading
    LIGHT_BRONZE = [222, 184, 135, 255] # Bronze highlights
    COPPER = [184, 115, 51, 255]     # Copper details
    DARK_COPPER = [120, 80, 40, 255] # Copper shading
    WOOD = [139, 90, 43, 255]        # Wooden grip
    DARK_WOOD = [80, 50, 25, 255]    # Wood grain
    BLACK = [0, 0, 0, 255]           # Outline/details
    GRAY = [128, 128, 128, 255]      # Dull effects
    
    # BLADE (thin, weak blade - much narrower than strong sword)
    blade_center_x = 16
    blade_start_y = 2
    blade_end_y = 18  # Shorter blade
    blade_width = 1   # Much thinner blade
    
    # Main blade body (thin iron blade)
    for y in range(blade_start_y, blade_end_y):
        # Just the center line and one pixel on each side
        canvas[y][blade_center_x] = IRON
        if y > blade_start_y + 2:  # Not at the very tip
            canvas[y][blade_center_x - 1] = IRON
            canvas[y][blade_center_x + 1] = IRON
    
    # Blade point (simple tapered tip)
    canvas[blade_start_y][blade_center_x] = IRON
    canvas[blade_start_y + 1][blade_center_x] = IRON
    canvas[blade_start_y + 2][blade_center_x - 1] = IRON
    canvas[blade_start_y + 2][blade_center_x + 1] = IRON
    
    # Minimal blade shading (left side darker, right side lighter)
    for y in range(blade_start_y + 3, blade_end_y):
        # Dark shading on left (only one pixel)
        canvas[y][blade_center_x - 1] = DARK_IRON
        
        # Light highlights on right (only one pixel)
        canvas[y][blade_center_x + 1] = LIGHT_IRON
    
    # No fuller (blood groove) - too thin and weak for that feature
    
    # Minimal edge definition (dull blade, less sharp)
    for y in range(blade_start_y + 4, blade_end_y - 1):
        # Very subtle edge shine (not bright white like strong sword)
        if blade_center_x - 2 >= 0:
            canvas[y][blade_center_x - 2] = GRAY
        if blade_center_x + 2 < size:
            canvas[y][blade_center_x + 2] = GRAY
    
    # SIMPLE CROSSGUARD (smaller, less ornate)
    guard_y = blade_end_y
    guard_width = 3  # Much smaller than strong sword
    
    # Simple bronze crossguard
    for x in range(blade_center_x - guard_width, blade_center_x + guard_width + 1):
        if x >= 0 and x < size:
            canvas[guard_y][x] = BRONZE
    
    # Basic crossguard shading
    canvas[guard_y][blade_center_x - guard_width] = DARK_BRONZE
    canvas[guard_y][blade_center_x + guard_width] = DARK_BRONZE
    canvas[guard_y][blade_center_x] = LIGHT_BRONZE
    
    # No ornate ends - just simple functional guard
    
    # SIMPLE GRIP/HANDLE
    grip_start_y = guard_y + 1
    grip_end_y = grip_start_y + 4  # Shorter grip
    
    # Basic wooden grip (no leather wrapping)
    for y in range(grip_start_y, grip_end_y):
        canvas[y][blade_center_x] = WOOD
    
    # Simple wood grain texture
    canvas[grip_start_y + 1][blade_center_x] = DARK_WOOD
    canvas[grip_start_y + 3][blade_center_x] = DARK_WOOD
    
    # BASIC POMMEL (simple, no gem)
    pommel_y = grip_end_y
    
    # Simple copper pommel (cheaper metal)
    canvas[pommel_y][blade_center_x - 1] = COPPER
    canvas[pommel_y][blade_center_x] = COPPER
    canvas[pommel_y][blade_center_x + 1] = COPPER
    
    # Basic pommel shading
    canvas[pommel_y][blade_center_x - 1] = DARK_COPPER
    canvas[pommel_y][blade_center_x + 1] = DARK_COPPER
    
    # No gem - just functional metal knob
    if pommel_y + 1 < size:
        canvas[pommel_y + 1][blade_center_x] = DARK_COPPER
    
    # MINIMAL DECORATIVE ELEMENTS
    # No runes or engravings - this is a basic, weak sword
    # Just some nicks and wear marks to show it's battle-worn
    
    # Battle damage/nicks on blade edges
    damage_positions = [
        (6, blade_center_x - 1),   # Left side nicks
        (10, blade_center_x + 1),  # Right side nicks
        (14, blade_center_x - 1),
    ]
    
    for y, x in damage_positions:
        if x >= 0 and x < size and y >= 0 and y < size:
            canvas[y][x] = DARK_IRON  # Dark nicks showing damage
    
    # Rust spots (showing poor maintenance)
    rust_positions = [
        (8, blade_center_x),
        (12, blade_center_x),
        (15, blade_center_x)
    ]
    
    for y, x in rust_positions:
        if x >= 0 and x < size and y >= 0 and y < size:
            canvas[y][x] = DARK_BRONZE  # Brownish rust color
    
    # Worn grip areas
    canvas[grip_start_y + 2][blade_center_x] = DARK_WOOD
    
    # Tarnished metal on crossguard
    canvas[guard_y][blade_center_x - 1] = DARK_BRONZE
    canvas[guard_y][blade_center_x + 1] = DARK_BRONZE
    
    # WEAK SWORD CHARACTERISTICS:
    # - Much thinner blade (1 pixel wide vs 3)
    # - Shorter overall length
    # - Cheaper materials (iron instead of steel, bronze instead of gold)
    # - No decorative elements (no gems, runes, or ornate details)
    # - Battle damage and wear
    # - Simpler construction
    # - Dull appearance (less shine and highlights)
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'art/weak_sword.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft pixel art weak sword")
    print(f"   Blade: Thin iron blade (1px wide) with battle damage")
    print(f"   Materials: Iron blade, bronze guard, wooden grip, copper pommel")
    print(f"   Condition: Battle-worn with nicks, rust spots, and tarnish")
    print(f"   Quality: Basic functional weapon, no decorative elements")

if __name__ == '__main__':
    create_weak_sword()