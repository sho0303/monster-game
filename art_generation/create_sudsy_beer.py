"""
Create a pixel art sudsy beer mug PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_sudsy_beer():
    """Create a Minecraft-style sudsy beer mug"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    AMBER = [255, 191, 0, 255]         # Main beer color (golden amber)
    DARK_AMBER = [204, 153, 0, 255]    # Beer shading
    LIGHT_AMBER = [255, 223, 102, 255] # Beer highlights
    FOAM_WHITE = [255, 255, 255, 255]  # Foam/head
    FOAM_CREAM = [255, 248, 220, 255]  # Foam shading
    FOAM_YELLOW = [255, 255, 224, 255] # Foam highlights
    GLASS = [220, 230, 240, 255]       # Glass mug
    DARK_GLASS = [180, 190, 200, 255]  # Glass shading
    LIGHT_GLASS = [245, 250, 255, 255] # Glass highlights
    WHITE = [255, 255, 255, 255]       # Bright reflections
    HANDLE_BROWN = [139, 69, 19, 255]  # Handle color
    DARK_BROWN = [101, 51, 13, 255]    # Handle shading
    LIGHT_BROWN = [205, 133, 63, 255]  # Handle highlights
    SILVER = [192, 192, 192, 255]      # Metal rim
    DARK_SILVER = [128, 128, 128, 255] # Metal shading
    BUBBLE = [255, 255, 255, 200]      # Beer bubbles
    GOLD_FOAM = [255, 215, 0, 150]     # Golden foam tint
    
    # MUG SHAPE (classic beer mug silhouette)
    mug_center_x = 14
    mug_bottom_y = 28
    mug_top_y = 6
    mug_width = 5
    
    # Main mug body (cylindrical shape)
    for y in range(mug_top_y + 2, mug_bottom_y):
        for x in range(mug_center_x - mug_width, mug_center_x + mug_width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = GLASS
    
    # Mug rim (slightly thicker at top)
    rim_y = mug_top_y
    for y in range(rim_y, rim_y + 2):
        for x in range(mug_center_x - mug_width - 1, mug_center_x + mug_width + 2):
            if x >= 0 and x < size:
                canvas[y][x] = SILVER
    
    # BEER LIQUID (fills most of the mug)
    beer_top_y = mug_top_y + 8  # Leave room for foam head
    beer_bottom_y = mug_bottom_y - 2
    
    # Main beer liquid
    for y in range(beer_top_y, beer_bottom_y):
        for x in range(mug_center_x - mug_width + 1, mug_center_x + mug_width):
            if x >= 0 and x < size:
                canvas[y][x] = AMBER
    
    # Beer surface (slightly curved)
    surface_y = beer_top_y
    canvas[surface_y][mug_center_x - 2] = LIGHT_AMBER
    canvas[surface_y][mug_center_x - 1] = LIGHT_AMBER
    canvas[surface_y][mug_center_x] = LIGHT_AMBER
    canvas[surface_y][mug_center_x + 1] = LIGHT_AMBER
    canvas[surface_y][mug_center_x + 2] = LIGHT_AMBER
    
    # Beer shading (left side darker)
    for y in range(beer_top_y + 1, beer_bottom_y):
        # Left side shading
        if mug_center_x - mug_width + 1 >= 0:
            canvas[y][mug_center_x - mug_width + 1] = DARK_AMBER
        # Right side highlights
        if mug_center_x + mug_width - 1 < size:
            canvas[y][mug_center_x + mug_width - 1] = LIGHT_AMBER
    
    # FOAM HEAD (thick, fluffy beer foam)
    foam_bottom_y = beer_top_y
    foam_top_y = mug_top_y + 2
    
    # Base foam layer
    for y in range(foam_top_y, foam_bottom_y + 2):
        foam_width = mug_width - 1
        if y < foam_top_y + 2:  # Foam overflows slightly
            foam_width = mug_width
        
        for x in range(mug_center_x - foam_width, mug_center_x + foam_width + 1):
            if x >= 0 and x < size:
                canvas[y][x] = FOAM_WHITE
    
    # Foam texture and bubbling
    foam_variations = [
        (foam_top_y, mug_center_x - 3, FOAM_CREAM),
        (foam_top_y, mug_center_x + 3, FOAM_CREAM),
        (foam_top_y + 1, mug_center_x - 2, FOAM_YELLOW),
        (foam_top_y + 1, mug_center_x + 2, FOAM_YELLOW),
        (foam_top_y + 2, mug_center_x - 4, FOAM_WHITE),
        (foam_top_y + 2, mug_center_x + 4, FOAM_WHITE),
        (foam_top_y + 3, mug_center_x - 1, FOAM_CREAM),
        (foam_top_y + 3, mug_center_x + 1, FOAM_CREAM),
        (foam_top_y + 4, mug_center_x, FOAM_YELLOW),
    ]
    
    for foam_y, foam_x, color in foam_variations:
        if 0 <= foam_y < size and 0 <= foam_x < size:
            canvas[foam_y][foam_x] = color
    
    # Overflowing foam drips
    drip_positions = [
        (foam_top_y + 5, mug_center_x - mug_width - 1),
        (foam_top_y + 6, mug_center_x + mug_width + 1),
        (foam_top_y + 7, mug_center_x - mug_width - 2),
    ]
    
    for drip_y, drip_x in drip_positions:
        if 0 <= drip_y < size and 0 <= drip_x < size:
            canvas[drip_y][drip_x] = FOAM_CREAM
    
    # MUG HANDLE (classic beer mug handle)
    handle_x_start = mug_center_x + mug_width + 2
    handle_y_start = mug_top_y + 8
    handle_y_end = mug_top_y + 18
    
    # Handle outer curve
    handle_positions = [
        (handle_y_start, handle_x_start),
        (handle_y_start + 1, handle_x_start + 1),
        (handle_y_start + 2, handle_x_start + 2),
        (handle_y_start + 3, handle_x_start + 2),
        (handle_y_start + 4, handle_x_start + 2),
        (handle_y_start + 5, handle_x_start + 2),
        (handle_y_start + 6, handle_x_start + 2),
        (handle_y_start + 7, handle_x_start + 1),
        (handle_y_start + 8, handle_x_start),
        (handle_y_start + 9, handle_x_start - 1),
        (handle_y_start + 10, handle_x_start),
    ]
    
    for handle_y, handle_x in handle_positions:
        if 0 <= handle_y < size and 0 <= handle_x < size:
            canvas[handle_y][handle_x] = HANDLE_BROWN
    
    # Handle shading
    handle_shade_positions = [
        (handle_y_start + 1, handle_x_start),
        (handle_y_start + 2, handle_x_start + 1),
        (handle_y_start + 3, handle_x_start + 1),
        (handle_y_start + 7, handle_x_start),
        (handle_y_start + 8, handle_x_start - 1),
    ]
    
    for shade_y, shade_x in handle_shade_positions:
        if 0 <= shade_y < size and 0 <= shade_x < size:
            canvas[shade_y][shade_x] = DARK_BROWN
    
    # MUG DETAILS
    # Glass shading (left side darker)
    for y in range(mug_top_y + 2, mug_bottom_y):
        # Left edge shading
        if mug_center_x - mug_width - 1 >= 0:
            canvas[y][mug_center_x - mug_width - 1] = DARK_GLASS
        # Right edge highlights
        if mug_center_x + mug_width + 1 < size:
            canvas[y][mug_center_x + mug_width + 1] = LIGHT_GLASS
    
    # Glass reflections (bright spots)
    reflection_positions = [
        (mug_top_y + 8, mug_center_x - 3),
        (mug_top_y + 14, mug_center_x - 3),
        (mug_top_y + 20, mug_center_x - 3),
    ]
    
    for refl_y, refl_x in reflection_positions:
        if 0 <= refl_y < size and 0 <= refl_x < size:
            canvas[refl_y][refl_x] = WHITE
    
    # Rim shading
    canvas[rim_y][mug_center_x - mug_width - 1] = DARK_SILVER
    canvas[rim_y + 1][mug_center_x - mug_width - 1] = DARK_SILVER
    
    # BEER BUBBLES (carbonation effects)
    bubble_positions = [
        (beer_top_y + 3, mug_center_x - 1),
        (beer_top_y + 6, mug_center_x + 2),
        (beer_top_y + 9, mug_center_x),
        (beer_top_y + 12, mug_center_x - 2),
        (beer_top_y + 15, mug_center_x + 1),
        (beer_top_y + 18, mug_center_x - 1),
        (beer_top_y + 5, mug_center_x + 3),
        (beer_top_y + 11, mug_center_x - 3),
        (beer_top_y + 16, mug_center_x + 2),
    ]
    
    for bubble_y, bubble_x in bubble_positions:
        if 0 <= bubble_y < size and 0 <= bubble_x < size:
            canvas[bubble_y][bubble_x] = BUBBLE
    
    # Foam sparkle (fresh foam effect)
    foam_sparkles = [
        (foam_top_y + 1, mug_center_x - 1),
        (foam_top_y + 2, mug_center_x + 1),
        (foam_top_y + 3, mug_center_x - 2),
        (foam_top_y + 4, mug_center_x + 2),
    ]
    
    for sparkle_y, sparkle_x in foam_sparkles:
        if 0 <= sparkle_y < size and 0 <= sparkle_x < size:
            canvas[sparkle_y][sparkle_x] = WHITE
    
    # MUG BASE (slight thickening at bottom)
    base_y = mug_bottom_y
    for x in range(mug_center_x - mug_width - 1, mug_center_x + mug_width + 2):
        if x >= 0 and x < size and base_y < size:
            canvas[base_y][x] = DARK_GLASS
    
    # Tavern atmosphere sparkles
    atmosphere_sparkles = [
        (mug_top_y - 2, mug_center_x - 4),
        (mug_top_y + 2, mug_center_x + 7),
        (mug_top_y + 10, mug_center_x - 7),
        (mug_top_y + 16, mug_center_x + 8),
        (mug_top_y + 22, mug_center_x - 6),
    ]
    
    for atm_y, atm_x in atmosphere_sparkles:
        if 0 <= atm_y < size and 0 <= atm_x < size:
            canvas[atm_y][atm_x] = GOLD_FOAM
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/sudsy_beer.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art sudsy beer mug with tavern atmosphere")
    print(f"   Features: Glass mug, golden amber beer, thick foam head")
    print(f"   Details: Curved handle, foam overflow, carbonation bubbles")
    print(f"   Effects: Glass reflections, foam sparkles, tavern ambiance")

if __name__ == '__main__':
    create_sudsy_beer()