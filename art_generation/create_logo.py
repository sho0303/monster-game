"""
Create a PNG logo for PYQUEST game title in Minecraft pixel art style
"""
from PIL import Image, ImageDraw
import numpy as np

def create_pyquest_logo():
    """Create a Minecraft-style MonsterGame logo with pixel art"""
    # Create a larger canvas for pixel art logo (wider to fit MonsterGame)
    width, height = 88, 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (Minecraft-style colors)
    GOLD = [255, 215, 0, 255]        # Gold text
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    LIGHT_GOLD = [255, 255, 100, 255] # Gold highlights
    BROWN = [101, 67, 33, 255]       # Brown outline
    DARK_BROWN = [60, 40, 20, 255]   # Brown shading
    BLACK = [0, 0, 0, 255]           # Shadow
    RED = [220, 20, 60, 255]         # Accent color
    GREEN = [34, 139, 34, 255]       # Green accents
    BLUE = [0, 100, 255, 255]        # Blue accents
    WHITE = [255, 255, 255, 255]     # Highlights
    GRAY = [128, 128, 128, 255]      # Border
    
    # Draw "MonsterGame" in blocky Minecraft-style letters
    
    # M (starting at x=2, y=8)
    m_pattern = [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # O (starting at x=8, y=8)
    o_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # N (starting at x=14, y=8)
    n_pattern = [
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # S (starting at x=20, y=8)
    s_pattern = [
        [0,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [0,1,1,1,0],
        [0,0,0,0,1],
        [0,0,0,0,1],
        [1,1,1,1,0]
    ]
    
    # T (starting at x=26, y=8)
    t_pattern = [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ]
    
    # E (starting at x=32, y=8)
    e_pattern = [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ]
    
    # R (starting at x=38, y=8)
    r_pattern = [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,1,0,0],
        [1,0,0,1,0],
        [1,0,0,0,1]
    ]
    
    # G (starting at x=45, y=8)
    g_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,0],
        [1,0,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # A (starting at x=51, y=8)
    a_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # M (starting at x=57, y=8)
    m2_pattern = [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # E (starting at x=63, y=8)
    e2_pattern = [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ]
    
    # Draw each letter with 3D effect
    letters = [
        (m_pattern, 2),    # M
        (o_pattern, 8),    # O
        (n_pattern, 14),   # N
        (s_pattern, 20),   # S
        (t_pattern, 26),   # T
        (e_pattern, 32),   # E
        (r_pattern, 38),   # R
        (g_pattern, 45),   # G
        (a_pattern, 51),   # A
        (m2_pattern, 57),  # M
        (e2_pattern, 63)   # E
    ]
    
    for pattern, start_x in letters:
        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == 1:
                    x = start_x + col_idx
                    y = 8 + row_idx
                    
                    if x < width and y < height:
                        # Draw shadow first (offset down and right)
                        if x + 1 < width and y + 1 < height:
                            canvas[y + 1][x + 1] = DARK_BROWN
                        
                        # Draw main letter
                        canvas[y][x] = GOLD
                        
                        # Add highlights (top-left pixels)
                        if row_idx == 0 or (row_idx > 0 and pattern[row_idx-1][col_idx] == 0):
                            canvas[y][x] = LIGHT_GOLD
                        if col_idx == 0 or (col_idx > 0 and pattern[row_idx][col_idx-1] == 0):
                            canvas[y][x] = LIGHT_GOLD
    
    # Add decorative border frame
    # Top border
    for x in range(width):
        canvas[0][x] = BROWN
        canvas[1][x] = DARK_BROWN
        canvas[height-2][x] = BROWN
        canvas[height-1][x] = DARK_BROWN
    
    # Side borders
    for y in range(height):
        canvas[y][0] = BROWN
        canvas[y][1] = DARK_BROWN
        canvas[y][width-2] = BROWN
        canvas[y][width-1] = DARK_BROWN
    
    # Add corner decorations (golden corner pieces)
    corner_positions = [(2, 2), (2, width-3), (height-3, 2), (height-3, width-3)]
    for cy, cx in corner_positions:
        if cx < width and cy < height:
            canvas[cy][cx] = LIGHT_GOLD
            canvas[cy][cx+1] = GOLD
            canvas[cy+1][cx] = GOLD
            canvas[cy+1][cx+1] = DARK_GOLD
    
    # Add subtitle decorative elements (small sword and shield icons)
    # Sword icon (left side)
    sword_x, sword_y = 4, 18
    # Simple sword shape
    sword_pixels = [
        (0, 2), (1, 2), (2, 2), (3, 2),  # blade
        (4, 1), (4, 2), (4, 3),          # crossguard
        (5, 2), (6, 2), (7, 2)           # handle
    ]
    
    for dx, dy in sword_pixels:
        x, y = sword_x + dx, sword_y + dy
        if x < width and y < height:
            canvas[y][x] = GRAY
    
    # Shield icon (right side)  
    shield_x, shield_y = width - 16, 18
    shield_pixels = [
        (0, 1), (0, 2), (0, 3),          # left edge
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),  # left side
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),  # center
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),  # right side
        (4, 1), (4, 2), (4, 3),          # right edge
        (2, 5)                           # bottom point
    ]
    
    for dx, dy in shield_pixels:
        x, y = shield_x + dx, shield_y + dy
        if x < width and y < height:
            canvas[y][x] = RED
    
    # Add sparkle effects around the logo
    sparkle_positions = [
        (6, 70), (12, 74), (18, 72), (24, 76),
        (6, 6), (12, 4), (18, 6), (24, 4)
    ]
    
    for sy, sx in sparkle_positions:
        if sx < width and sy < height:
            canvas[sy][sx] = WHITE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Save image
    output_path = 'art/pyquest.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width * scale}x{height * scale} pixels")
    print(f"   Style: Minecraft-style pixel art logo")
    print(f"   Features: MonsterGame branding, blocky gold text, 3D shading")
    print(f"   Details: Sword and shield icons, corner decorations, sparkles")

if __name__ == '__main__':
    create_pyquest_logo()
