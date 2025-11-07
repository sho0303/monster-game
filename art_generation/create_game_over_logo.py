"""
Create a PNG logo for "GAME OVER!!" in Minecraft pixel art style
"""
from PIL import Image, ImageDraw
import numpy as np

def create_game_over_logo():
    """Create a Minecraft-style GAME OVER!! logo with pixel art"""
    # Create a larger canvas for pixel art logo (sized for GAME OVER!!)
    width, height = 88, 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (dramatic dark colors for final game over theme)
    DARK_RED = [139, 0, 0, 255]      # Main text color (final defeat)
    BLACK = [0, 0, 0, 255]           # Deep shadows and death
    BLOOD_RED = [180, 0, 0, 255]     # Slightly lighter red
    CRIMSON = [220, 20, 60, 255]     # Bright red highlights
    MAROON = [80, 0, 0, 255]         # Darker red shading
    DARK_GRAY = [32, 32, 32, 255]    # Ominous gray
    GRAY = [64, 64, 64, 255]         # Border elements
    WHITE = [255, 255, 255, 255]     # Skull/bone elements
    ORANGE = [255, 69, 0, 255]       # Fire effects
    YELLOW = [255, 215, 0, 255]      # Flame highlights
    PURPLE = [75, 0, 130, 255]       # Dark magic/evil
    DARK_PURPLE = [48, 0, 80, 255]   # Deep evil magic
    
    # Draw "GAME OVER!!" in blocky Minecraft-style letters
    
    # G (starting at x=2, y=8)
    g_pattern = [
        [0,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # A (starting at x=8, y=8)
    a_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # M (starting at x=14, y=8)
    m_pattern = [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # E (starting at x=20, y=8)
    e_pattern = [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ]
    
    # Space (2 pixels) then O (starting at x=28, y=8)
    o_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # V (starting at x=34, y=8)
    v_pattern = [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,0,1,0],
        [0,0,1,0,0]
    ]
    
    # E (starting at x=40, y=8) - second E
    e2_pattern = [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ]
    
    # R (starting at x=46, y=8)
    r_pattern = [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,1,0,0],
        [1,0,0,1,0],
        [1,0,0,0,1]
    ]
    
    # ! (starting at x=52, y=8)
    exclamation1_pattern = [
        [1],
        [1],
        [1],
        [1],
        [1],
        [0],
        [1]
    ]
    
    # ! (starting at x=54, y=8) - second exclamation
    exclamation2_pattern = [
        [1],
        [1],
        [1],
        [1],
        [1],
        [0],
        [1]
    ]
    
    # Draw each letter with 3D effect (using dark red for final doom)
    letters = [
        (g_pattern, 2),    # G
        (a_pattern, 8),    # A
        (m_pattern, 14),   # M
        (e_pattern, 20),   # E
        (o_pattern, 28),   # O
        (v_pattern, 34),   # V
        (e2_pattern, 40),  # E
        (r_pattern, 46),   # R
        (exclamation1_pattern, 52),  # !
        (exclamation2_pattern, 54)   # !
    ]
    
    for pattern, start_x in letters:
        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == 1:
                    x = start_x + col_idx
                    y = 8 + row_idx
                    
                    if x < width and y < height:
                        # Draw deep shadow first (offset down and right)
                        if x + 1 < width and y + 1 < height:
                            canvas[y + 1][x + 1] = BLACK
                        if x + 2 < width and y + 2 < height:
                            canvas[y + 2][x + 2] = MAROON
                        
                        # Draw main letter in dark red (final doom)
                        canvas[y][x] = DARK_RED
                        
                        # Add dramatic highlights (top-left edges)
                        if row_idx == 0 or (row_idx > 0 and pattern[row_idx-1][col_idx] == 0):
                            canvas[y][x] = CRIMSON
                        if col_idx == 0 or (col_idx > 0 and pattern[row_idx][col_idx-1] == 0):
                            canvas[y][x] = BLOOD_RED
    
    # Add ominous border frame (death/doom theme)
    # Outer dark border
    for x in range(width):
        canvas[0][x] = BLACK
        canvas[1][x] = DARK_GRAY
        canvas[height-2][x] = DARK_GRAY
        canvas[height-1][x] = BLACK
    
    # Side borders
    for y in range(height):
        canvas[y][0] = BLACK
        canvas[y][1] = DARK_GRAY
        canvas[y][width-2] = DARK_GRAY
        canvas[y][width-1] = BLACK
    
    # Add corner death symbols
    death_corners = [(2, 2), (2, width-3), (height-3, 2), (height-3, width-3)]
    for cy, cx in death_corners:
        if cx < width and cy < height:
            # Skull and crossbones motif
            canvas[cy][cx] = WHITE        # Skull
            canvas[cy][cx+1] = DARK_GRAY  # Shadow
            canvas[cy+1][cx] = DARK_GRAY  # Crossbones
            canvas[cy+1][cx+1] = WHITE
    
    # Add dramatic game over themed decorative elements
    
    # Gravestone (left side) - representing permanent death
    grave_x, grave_y = 4, 18
    gravestone_pixels = [
        (0, 1), (0, 2), (0, 3),      # Gravestone top
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),  # Gravestone body
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),  # Gravestone body
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),  # Gravestone base
        (4, 1), (4, 2), (4, 3)       # Ground mound
    ]
    
    for dx, dy in gravestone_pixels:
        x, y = grave_x + dx, grave_y + dy
        if x < width and y < height:
            if dx <= 3:  # Gravestone
                canvas[y][x] = GRAY
            else:  # Ground
                canvas[y][x] = DARK_GRAY
    
    # Add "RIP" text on gravestone
    rip_pixels = [(1, 1), (1, 3), (2, 2)]  # Simple R.I.P pattern
    for dx, dy in rip_pixels:
        x, y = grave_x + dx, grave_y + dy + 1
        if x < width and y < height:
            canvas[y][x] = BLACK
    
    # Grim reaper scythe (right side) - representing death incarnate
    scythe_x, scythe_y = width - 12, 18
    scythe_pixels = [
        (0, 0), (0, 1), (0, 2),      # Scythe blade
        (1, 0),                      # Blade edge
        (2, 1),                      # Blade connection
        (3, 2), (4, 3), (5, 4),      # Long handle
        (6, 5)                       # Handle end
    ]
    
    for dx, dy in scythe_pixels:
        x, y = scythe_x + dx, scythe_y + dy
        if x < width and y < height:
            if dy <= 2:  # Blade
                canvas[y][x] = GRAY
            else:  # Handle
                canvas[y][x] = DARK_GRAY
    
    # Add evil magical aura effects around the text
    # Dark magic energy (purple/black swirls)
    magic_positions = [
        (4, 58), (10, 62), (16, 60), (22, 64),
        (4, 4), (10, 2), (16, 4), (22, 2),
        (26, 58), (32, 62), (38, 60), (44, 64)
    ]
    
    for my, mx in magic_positions:
        if mx < width and my < height:
            canvas[my][mx] = DARK_PURPLE
            if my + 1 < height:
                canvas[my + 1][mx] = PURPLE
    
    # Hellfire effects (showing eternal punishment)
    fire_positions = [
        (6, 56), (12, 60), (18, 58), (24, 62),
        (6, 6), (12, 4), (18, 6), (24, 4),
        (28, 56), (34, 60), (40, 58), (46, 62)
    ]
    
    for fy, fx in fire_positions:
        if fx < width and fy < height:
            canvas[fy][fx] = ORANGE
            if fy - 1 >= 0:
                canvas[fy - 1][fx] = YELLOW
    
    # Death lightning (final judgment strikes)
    lightning_positions = [
        (5, 54), (11, 58), (17, 56), (23, 60),
        (5, 8), (11, 6), (17, 8), (23, 6),
        (27, 54), (33, 58), (39, 56), (45, 60)
    ]
    
    for ly, lx in lightning_positions:
        if lx < width and ly < height:
            canvas[ly][lx] = WHITE
    
    # Bone fragments (scattered remains)
    bone_positions = [
        (7, 52), (13, 56), (19, 54), (25, 58),
        (7, 10), (13, 8), (19, 10), (25, 8),
        (29, 52), (35, 56), (41, 54), (47, 58)
    ]
    
    for by, bx in bone_positions:
        if bx < width and by < height:
            canvas[by][bx] = WHITE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Save image
    output_path = 'art/game_over.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width * scale}x{height * scale} pixels")
    print(f"   Style: Minecraft-style pixel art final game over message")
    print(f"   Features: GAME OVER!! in dark red text, deep shadows")
    print(f"   Details: Gravestone with RIP, grim reaper scythe, death symbols")
    print(f"   Effects: Dark magic aura, hellfire, death lightning, bone fragments")
    print(f"   Theme: Ultimate defeat/final death with ominous black borders")

if __name__ == '__main__':
    create_game_over_logo()