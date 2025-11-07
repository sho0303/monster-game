"""
Create a pixel art nunchucks PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_nunchucks():
    """Create a Minecraft-style nunchucks"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BROWN = [101, 67, 33, 255]       # Main wood color
    DARK_BROWN = [60, 40, 20, 255]   # Wood shading
    LIGHT_BROWN = [139, 90, 43, 255] # Wood highlights
    BLACK = [0, 0, 0, 255]           # Chain links / deep shadows
    DARK_GRAY = [64, 64, 64, 255]    # Chain shading
    SILVER = [192, 192, 192, 255]    # Chain highlights
    LIGHT_SILVER = [230, 230, 230, 255] # Bright chain
    GOLD = [255, 215, 0, 255]        # Metal caps/fittings
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    RED = [139, 0, 0, 255]           # Accent wrapping
    DARK_RED = [100, 0, 0, 255]      # Red shading
    
    # LEFT STICK (first nunchuck handle)
    left_stick_x = 8
    left_stick_start_y = 4
    left_stick_end_y = 16
    stick_width = 2
    
    # Main wooden handle body
    for y in range(left_stick_start_y, left_stick_end_y):
        for x in range(left_stick_x, left_stick_x + stick_width + 1):
            canvas[y][x] = BROWN
    
    # Wood grain and shading
    for y in range(left_stick_start_y, left_stick_end_y):
        canvas[y][left_stick_x] = DARK_BROWN  # Left edge shadow
        canvas[y][left_stick_x + stick_width] = LIGHT_BROWN  # Right edge highlight
    
    # Wood grain texture (vertical lines)
    for y in range(left_stick_start_y + 1, left_stick_end_y, 3):
        canvas[y][left_stick_x + 1] = LIGHT_BROWN
    
    # Metal cap at bottom (weighted end)
    cap_y = left_stick_end_y - 2
    for x in range(left_stick_x, left_stick_x + stick_width + 1):
        canvas[cap_y][x] = GOLD
        canvas[cap_y + 1][x] = DARK_GOLD
    
    # Red grip wrapping (traditional)
    wrap_positions = [
        left_stick_start_y + 3,
        left_stick_start_y + 5,
        left_stick_start_y + 7,
        left_stick_start_y + 9,
    ]
    
    for wrap_y in wrap_positions:
        canvas[wrap_y][left_stick_x] = RED
        canvas[wrap_y][left_stick_x + stick_width] = DARK_RED
    
    # RIGHT STICK (second nunchuck handle)
    right_stick_x = 22
    right_stick_start_y = 18
    right_stick_end_y = 30
    
    # Main wooden handle body
    for y in range(right_stick_start_y, right_stick_end_y):
        for x in range(right_stick_x, right_stick_x + stick_width + 1):
            canvas[y][x] = BROWN
    
    # Wood grain and shading
    for y in range(right_stick_start_y, right_stick_end_y):
        canvas[y][right_stick_x] = DARK_BROWN  # Left edge shadow
        canvas[y][right_stick_x + stick_width] = LIGHT_BROWN  # Right edge highlight
    
    # Wood grain texture
    for y in range(right_stick_start_y + 1, right_stick_end_y, 3):
        canvas[y][right_stick_x + 1] = LIGHT_BROWN
    
    # Metal cap at top
    cap_y = right_stick_start_y
    for x in range(right_stick_x, right_stick_x + stick_width + 1):
        canvas[cap_y][x] = GOLD
        canvas[cap_y + 1][x] = DARK_GOLD
    
    # Red grip wrapping
    wrap_positions = [
        right_stick_start_y + 4,
        right_stick_start_y + 6,
        right_stick_start_y + 8,
        right_stick_start_y + 10,
    ]
    
    for wrap_y in wrap_positions:
        canvas[wrap_y][right_stick_x] = RED
        canvas[wrap_y][right_stick_x + stick_width] = DARK_RED
    
    # CHAIN CONNECTION (linking the two handles)
    # Chain connection points
    left_connect_x = left_stick_x + stick_width + 1
    left_connect_y = left_stick_end_y - 1
    right_connect_x = right_stick_x
    right_connect_y = right_stick_start_y + 1
    
    # Metal eyelets where chain attaches
    canvas[left_connect_y][left_connect_x] = SILVER
    canvas[left_connect_y + 1][left_connect_x] = DARK_GRAY
    canvas[right_connect_y][right_connect_x - 1] = SILVER
    canvas[right_connect_y + 1][right_connect_x - 1] = DARK_GRAY
    
    # CHAIN LINKS (curved path between handles)
    # Create a curved chain path
    chain_points = [
        # Starting from left handle
        (left_connect_y, left_connect_x + 1),
        (left_connect_y + 1, left_connect_x + 2),
        (left_connect_y + 2, left_connect_x + 3),
        (left_connect_y + 3, left_connect_x + 4),
        (left_connect_y + 4, left_connect_x + 5),
        # Middle curve
        (left_connect_y + 5, left_connect_x + 6),
        (left_connect_y + 6, left_connect_x + 7),
        (left_connect_y + 7, left_connect_x + 8),
        (left_connect_y + 8, left_connect_x + 7),
        (left_connect_y + 9, left_connect_x + 6),
        # Approaching right handle
        (left_connect_y + 10, left_connect_x + 5),
        (left_connect_y + 11, left_connect_x + 4),
        (right_connect_y - 2, right_connect_x - 2),
        (right_connect_y - 1, right_connect_x - 1),
    ]
    
    # Draw chain links
    for i, (chain_y, chain_x) in enumerate(chain_points):
        if 0 <= chain_y < size and 0 <= chain_x < size:
            # Alternate between different chain link appearances
            if i % 3 == 0:
                canvas[chain_y][chain_x] = SILVER  # Bright link
            elif i % 3 == 1:
                canvas[chain_y][chain_x] = DARK_GRAY  # Shadow link
            else:
                canvas[chain_y][chain_x] = BLACK  # Dark link center
    
    # Add chain link detail (oval shapes)
    chain_detail_points = [
        (left_connect_y + 2, left_connect_x + 2),
        (left_connect_y + 4, left_connect_x + 4),
        (left_connect_y + 6, left_connect_x + 6),
        (left_connect_y + 8, left_connect_x + 6),
        (left_connect_y + 10, left_connect_x + 4),
    ]
    
    for detail_y, detail_x in chain_detail_points:
        if 0 <= detail_y < size and 0 <= detail_x < size:
            canvas[detail_y][detail_x] = LIGHT_SILVER
            # Add link shadows
            if detail_y + 1 < size:
                canvas[detail_y + 1][detail_x] = DARK_GRAY
    
    # MOTION BLUR EFFECTS (showing nunchucks in action)
    # Left stick motion trail
    motion_trail_left = [
        (left_stick_start_y, left_stick_x - 1),
        (left_stick_start_y + 2, left_stick_x - 2),
        (left_stick_start_y + 4, left_stick_x - 1),
    ]
    
    for trail_y, trail_x in motion_trail_left:
        if 0 <= trail_y < size and 0 <= trail_x < size:
            canvas[trail_y][trail_x] = LIGHT_BROWN
    
    # Right stick motion trail
    motion_trail_right = [
        (right_stick_end_y - 1, right_stick_x + stick_width + 2),
        (right_stick_end_y - 3, right_stick_x + stick_width + 3),
        (right_stick_end_y - 5, right_stick_x + stick_width + 2),
    ]
    
    for trail_y, trail_x in motion_trail_right:
        if 0 <= trail_y < size and 0 <= trail_x < size:
            canvas[trail_y][trail_x] = LIGHT_BROWN
    
    # DECORATIVE ELEMENTS
    # Traditional martial arts symbols on handles
    # Left handle symbol (small dot pattern)
    canvas[left_stick_start_y + 6][left_stick_x + 1] = DARK_BROWN
    
    # Right handle symbol
    canvas[right_stick_start_y + 7][right_stick_x + 1] = DARK_BROWN
    
    # Handle end caps detail
    canvas[left_stick_start_y][left_stick_x + 1] = GOLD
    canvas[right_stick_end_y - 1][right_stick_x + 1] = GOLD
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'ascii_art/nunchucks.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art nunchucks with dynamic motion")
    print(f"   Features: Wooden handles, metal chain, grip wrapping")
    print(f"   Details: Wood grain, gold caps, motion trails, chain links")
    print(f"   Action: Positioned mid-swing showing martial arts movement")

if __name__ == '__main__':
    create_nunchucks()