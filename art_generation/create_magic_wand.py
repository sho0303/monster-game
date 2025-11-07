"""
Create a pixel art magic wand PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_magic_wand():
    """Create a Minecraft-style magic wand"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BROWN = [101, 67, 33, 255]       # Wood handle
    DARK_BROWN = [60, 40, 20, 255]   # Wood shading
    LIGHT_BROWN = [139, 90, 43, 255] # Wood highlights
    PURPLE = [128, 0, 128, 255]      # Magic crystal/gem
    DARK_PURPLE = [75, 0, 75, 255]   # Purple shading
    LIGHT_PURPLE = [200, 100, 200, 255] # Purple highlights
    PINK = [255, 192, 203, 255]      # Magic glow
    MAGENTA = [255, 0, 255, 255]     # Bright magic
    WHITE = [255, 255, 255, 255]     # Sparkles
    GOLD = [255, 215, 0, 255]        # Golden accents
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    SILVER = [192, 192, 192, 255]    # Metal details
    BLUE = [0, 100, 255, 255]        # Magic energy
    LIGHT_BLUE = [173, 216, 230, 255] # Light magic
    BLACK = [0, 0, 0, 255]           # Shadow
    
    # WAND HANDLE (wooden shaft, diagonal for dynamic look)
    handle_start_x = 8
    handle_start_y = 22
    handle_end_x = 18
    handle_end_y = 12
    handle_width = 2
    
    # Main wooden handle (diagonal line with thickness)
    # Create diagonal handle using line drawing
    for i in range(11):  # Length of handle
        progress = i / 10.0
        x = int(handle_start_x + (handle_end_x - handle_start_x) * progress)
        y = int(handle_start_y + (handle_end_y - handle_start_y) * progress)
        
        # Main handle body
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                px, py = x + dx, y + dy
                if 0 <= px < size and 0 <= py < size:
                    canvas[py][px] = BROWN
    
    # Add wood grain and shading along the handle
    for i in range(0, 11, 2):
        progress = i / 10.0
        x = int(handle_start_x + (handle_end_x - handle_start_x) * progress)
        y = int(handle_start_y + (handle_end_y - handle_start_y) * progress)
        
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x-1] = DARK_BROWN  # Left side shading
            canvas[y][x+1] = LIGHT_BROWN  # Right side highlight
    
    # MAGIC STAR TIP (5-pointed star at the top of the wand)
    star_center_x = handle_end_x
    star_center_y = handle_end_y - 3
    
    # Create a proper 5-pointed star
    # Top point
    canvas[star_center_y - 2][star_center_x] = LIGHT_PURPLE
    canvas[star_center_y - 1][star_center_x] = PURPLE
    
    # Upper left and right points
    canvas[star_center_y - 1][star_center_x - 2] = LIGHT_PURPLE
    canvas[star_center_y - 1][star_center_x + 2] = LIGHT_PURPLE
    canvas[star_center_y][star_center_x - 1] = PURPLE
    canvas[star_center_y][star_center_x + 1] = PURPLE
    
    # Center of star
    canvas[star_center_y][star_center_x] = WHITE
    
    # Lower left and right points
    canvas[star_center_y + 1][star_center_x - 1] = PURPLE
    canvas[star_center_y + 1][star_center_x + 1] = PURPLE
    canvas[star_center_y + 2][star_center_x - 2] = LIGHT_PURPLE
    canvas[star_center_y + 2][star_center_x + 2] = LIGHT_PURPLE
    
    # Bottom point
    canvas[star_center_y + 1][star_center_x] = PURPLE
    canvas[star_center_y + 2][star_center_x] = LIGHT_PURPLE
    
    # Star outline for definition
    star_outline_pixels = [
        # Top point outline
        (star_center_x - 1, star_center_y - 2),
        (star_center_x + 1, star_center_y - 2),
        # Upper side outlines
        (star_center_x - 2, star_center_y - 2),
        (star_center_x + 2, star_center_y - 2),
        (star_center_x - 3, star_center_y - 1),
        (star_center_x + 3, star_center_y - 1),
        # Center sides
        (star_center_x - 2, star_center_y),
        (star_center_x + 2, star_center_y),
        # Lower sides
        (star_center_x - 3, star_center_y + 1),
        (star_center_x + 3, star_center_y + 1),
        (star_center_x - 2, star_center_y + 3),
        (star_center_x + 2, star_center_y + 3),
        # Bottom point outline
        (star_center_x - 1, star_center_y + 3),
        (star_center_x + 1, star_center_y + 3)
    ]
    
    for outline_x, outline_y in star_outline_pixels:
        if 0 <= outline_x < size and 0 <= outline_y < size:
            canvas[outline_y][outline_x] = DARK_PURPLE
    
    # GOLDEN SETTING (holding the star)
    setting_pixels = [
        (star_center_x - 1, star_center_y + 3),
        (star_center_x + 1, star_center_y + 3),
        (star_center_x, star_center_y + 4)
    ]
    
    for sx, sy in setting_pixels:
        if 0 <= sx < size and 0 <= sy < size:
            canvas[sy][sx] = GOLD
    
    # HANDLE GRIP DETAILS
    # Leather wrapping marks
    grip_positions = [
        (handle_start_x + 2, handle_start_y - 2),
        (handle_start_x + 4, handle_start_y - 4),
        (handle_start_x + 6, handle_start_y - 6)
    ]
    
    for gx, gy in grip_positions:
        if 0 <= gx < size and 0 <= gy < size:
            canvas[gy][gx] = DARK_BROWN
            canvas[gy][gx + 1] = LIGHT_BROWN
    
    # Metal band near the crystal (reinforcement)
    band_x = handle_end_x - 1
    band_y = handle_end_y + 1
    canvas[band_y][band_x] = SILVER
    canvas[band_y][band_x + 1] = SILVER
    canvas[band_y + 1][band_x] = SILVER
    
    # MAGICAL EFFECTS
    # Sparkles emanating from the star
    sparkle_positions = [
        (star_center_x - 4, star_center_y - 4),
        (star_center_x + 4, star_center_y - 4),
        (star_center_x - 5, star_center_y),
        (star_center_x + 5, star_center_y),
        (star_center_x - 3, star_center_y + 4),
        (star_center_x + 3, star_center_y + 4),
        (star_center_x, star_center_y - 5),
        (star_center_x, star_center_y + 5)
    ]
    
    for sparkle_x, sparkle_y in sparkle_positions:
        if 0 <= sparkle_x < size and 0 <= sparkle_y < size:
            canvas[sparkle_y][sparkle_x] = WHITE
    
    # Magic aura (colored energy field)
    aura_positions = [
        (star_center_x - 3, star_center_y - 3),
        (star_center_x + 3, star_center_y - 3),
        (star_center_x - 4, star_center_y + 1),
        (star_center_x + 4, star_center_y + 1),
        (star_center_x - 2, star_center_y + 4),
        (star_center_x + 2, star_center_y + 4)
    ]
    
    for aura_x, aura_y in aura_positions:
        if 0 <= aura_x < size and 0 <= aura_y < size:
            canvas[aura_y][aura_x] = PINK
    
    # Magic energy trails (showing active magic)
    energy_trail_positions = [
        (star_center_x - 6, star_center_y - 1),
        (star_center_x + 6, star_center_y - 1),
        (star_center_x - 1, star_center_y - 6),
        (star_center_x - 1, star_center_y + 6),
        (star_center_x - 5, star_center_y - 5),
        (star_center_x + 5, star_center_y + 5)
    ]
    
    for trail_x, trail_y in energy_trail_positions:
        if 0 <= trail_x < size and 0 <= trail_y < size:
            canvas[trail_y][trail_x] = MAGENTA
    
    # Magical runes on the handle (ancient symbols)
    rune_positions = [
        (handle_start_x + 1, handle_start_y - 1),
        (handle_start_x + 3, handle_start_y - 3),
        (handle_start_x + 5, handle_start_y - 5)
    ]
    
    for rune_x, rune_y in rune_positions:
        if 0 <= rune_x < size and 0 <= rune_y < size:
            canvas[rune_y][rune_x] = BLUE
    
    # WAND POMMEL (bottom end cap)
    pommel_x = handle_start_x - 1
    pommel_y = handle_start_y + 1
    
    if 0 <= pommel_x < size and 0 <= pommel_y < size:
        canvas[pommel_y][pommel_x] = GOLD
        canvas[pommel_y][pommel_x + 1] = DARK_GOLD
        canvas[pommel_y + 1][pommel_x] = DARK_GOLD
    
    # Additional magical energy wisps (flowing magic)
    wisp_positions = [
        (star_center_x - 7, star_center_y + 2),
        (star_center_x + 7, star_center_y - 2),
        (star_center_x + 2, star_center_y - 7),
        (star_center_x - 2, star_center_y + 7)
    ]
    
    for wisp_x, wisp_y in wisp_positions:
        if 0 <= wisp_x < size and 0 <= wisp_y < size:
            canvas[wisp_y][wisp_x] = LIGHT_BLUE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/magic_wand.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art magic wand with 5-pointed star")
    print(f"   Features: Wooden handle, purple star tip, golden setting")
    print(f"   Details: Magic sparkles, energy aura, runic inscriptions")
    print(f"   Magic: Pink glow, magenta trails, blue runes, flowing wisps")

if __name__ == '__main__':
    create_magic_wand()