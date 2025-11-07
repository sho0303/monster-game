"""
Create a PNG logo for MonsterMart in Minecraft pixel art style
"""
from PIL import Image, ImageDraw
import numpy as np

def create_monstermart_logo():
    """Create a Minecraft-style MonsterMart logo with pixel art"""
    # Create a larger canvas for pixel art logo (sized for MonsterMart)
    width, height = 88, 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (Minecraft-style colors with shop theme)
    GOLD = [255, 215, 0, 255]        # Gold text
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    LIGHT_GOLD = [255, 255, 100, 255] # Gold highlights
    GREEN = [34, 139, 34, 255]       # Shop/money green
    DARK_GREEN = [0, 100, 0, 255]    # Green shading
    LIGHT_GREEN = [144, 238, 144, 255] # Green highlights
    BROWN = [101, 67, 33, 255]       # Brown outline
    DARK_BROWN = [60, 40, 20, 255]   # Brown shading
    BLACK = [0, 0, 0, 255]           # Shadow
    RED = [220, 20, 60, 255]         # Accent color
    BLUE = [0, 100, 255, 255]        # Blue accents
    WHITE = [255, 255, 255, 255]     # Highlights
    GRAY = [128, 128, 128, 255]      # Border
    PURPLE = [128, 0, 128, 255]      # Magic shop accents
    
    # Draw "MonsterMart" in blocky Minecraft-style letters
    
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
    
    # M (starting at x=45, y=8) - second M
    m2_pattern = [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
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
    
    # R (starting at x=57, y=8) - second R
    r2_pattern = [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,1,0,0],
        [1,0,0,1,0],
        [1,0,0,0,1]
    ]
    
    # T (starting at x=63, y=8) - second T
    t2_pattern = [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ]
    
    # Draw each letter with 3D effect (using green for shop theme)
    letters = [
        (m_pattern, 2),    # M
        (o_pattern, 8),    # O
        (n_pattern, 14),   # N
        (s_pattern, 20),   # S
        (t_pattern, 26),   # T
        (e_pattern, 32),   # E
        (r_pattern, 38),   # R
        (m2_pattern, 45),  # M
        (a_pattern, 51),   # A
        (r2_pattern, 57),  # R
        (t2_pattern, 63)   # T
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
                        
                        # Draw main letter in shop green
                        canvas[y][x] = GREEN
                        
                        # Add highlights (top-left pixels)
                        if row_idx == 0 or (row_idx > 0 and pattern[row_idx-1][col_idx] == 0):
                            canvas[y][x] = LIGHT_GREEN
                        if col_idx == 0 or (col_idx > 0 and pattern[row_idx][col_idx-1] == 0):
                            canvas[y][x] = LIGHT_GREEN
    
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
    
    # Add corner decorations (golden coin symbols for shop theme)
    corner_positions = [(2, 2), (2, width-3), (height-3, 2), (height-3, width-3)]
    for cy, cx in corner_positions:
        if cx < width and cy < height:
            canvas[cy][cx] = GOLD
            canvas[cy][cx+1] = LIGHT_GOLD
            canvas[cy+1][cx] = DARK_GOLD
            canvas[cy+1][cx+1] = GOLD
    
    # Add shop-themed decorative elements
    # Coin stack icon (left side)
    coin_x, coin_y = 4, 18
    # Simple coin stack shape
    coin_pixels = [
        (0, 1), (0, 2), (0, 3),          # bottom coin
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),  # middle coin
        (2, 1), (2, 2), (2, 3),          # top coin
        (3, 1), (3, 2)                   # coin highlights
    ]
    
    for dx, dy in coin_pixels:
        x, y = coin_x + dx, coin_y + dy
        if x < width and y < height:
            if dy <= 1:  # Bottom coins
                canvas[y][x] = GOLD
            elif dy <= 3:  # Middle coins  
                canvas[y][x] = LIGHT_GOLD
            else:  # Top highlights
                canvas[y][x] = WHITE
    
    # Shopping bag icon (right side)  
    bag_x, bag_y = width - 16, 18
    bag_pixels = [
        (0, 2), (0, 3),                  # handle left
        (1, 1), (1, 2), (1, 3), (1, 4), # bag top
        (2, 1), (2, 2), (2, 3), (2, 4), # bag body
        (3, 1), (3, 2), (3, 3), (3, 4), # bag body
        (4, 1), (4, 2), (4, 3), (4, 4), # bag body
        (5, 2), (5, 3),                  # bag bottom
        (0, 0), (0, 5)                   # handle
    ]
    
    for dx, dy in bag_pixels:
        x, y = bag_x + dx, bag_y + dy
        if x < width and y < height:
            if dx == 0:  # Handle
                canvas[y][x] = BROWN
            else:  # Bag body
                canvas[y][x] = RED
    
    # Add dollar sign symbols (shop theme)
    dollar_positions = [
        (6, 70), (12, 74), (18, 72), (24, 76),
        (6, 6), (12, 4), (18, 6), (24, 4)
    ]
    
    for sy, sx in dollar_positions:
        if sx < width and sy < height:
            # Draw simple dollar sign
            canvas[sy][sx] = GOLD
            if sy + 1 < height:
                canvas[sy + 1][sx] = GOLD
            if sy + 2 < height:
                canvas[sy + 2][sx] = GOLD
    
    # Add magical shop sparkles (indicating magical items for sale)
    sparkle_positions = [
        (4, 72), (10, 76), (16, 74), (22, 78),
        (4, 8), (10, 6), (16, 8), (22, 6)
    ]
    
    for sy, sx in sparkle_positions:
        if sx < width and sy < height:
            canvas[sy][sx] = PURPLE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Save image
    output_path = 'ascii_art/monstermart.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width * scale}x{height * scale} pixels")
    print(f"   Style: Minecraft-style pixel art shop logo")
    print(f"   Features: MonsterMart branding, green shop text, 3D shading")
    print(f"   Details: Coin stack, shopping bag icons, dollar signs, magical sparkles")

if __name__ == '__main__':
    create_monstermart_logo()