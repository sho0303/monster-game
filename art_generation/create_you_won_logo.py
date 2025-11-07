"""
Create a PNG logo for "YOU WON!!" in Minecraft pixel art style
Matches the style of create_you_lost_logo.py but with victory theme
"""
from PIL import Image, ImageDraw
import numpy as np

def create_you_won_logo():
    """Create a Minecraft-style YOU WON!! logo with pixel art"""
    # Create a larger canvas for pixel art logo (sized for YOU WON!!)
    width, height = 80, 32  # Slightly wider for extra exclamation marks
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (celebratory colors for victory theme)
    GOLD = [255, 215, 0, 255]        # Main text color (victory/treasure)
    DARK_GOLD = [184, 134, 11, 255]  # Gold shading
    LIGHT_GOLD = [255, 255, 100, 255] # Gold highlights
    BLACK = [0, 0, 0, 255]           # Deep shadows
    DARK_GRAY = [64, 64, 64, 255]    # Gray shading
    GRAY = [128, 128, 128, 255]      # Border elements
    WHITE = [255, 255, 255, 255]     # Highlights/sparkles
    GREEN = [0, 255, 0, 255]         # Victory/success effects
    YELLOW = [255, 255, 0, 255]      # Bright celebration effects
    BROWN = [101, 67, 33, 255]       # Frame color
    DARK_BROWN = [60, 40, 20, 255]   # Frame shading
    BLUE = [0, 150, 255, 255]        # Celebration accent
    SILVER = [192, 192, 192, 255]    # Trophy/medal color
    
    # Draw "YOU WON!!" in blocky Minecraft-style letters
    
    # Y (starting at x=2, y=8)
    y_pattern = [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,0,1,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
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
    
    # U (starting at x=14, y=8)
    u_pattern = [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # W (starting at x=22, y=8)
    w_pattern = [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,1,0,1,1],
        [1,0,0,0,1]
    ]
    
    # O (starting at x=28, y=8)
    o2_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # N (starting at x=34, y=8)
    n_pattern = [
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
    
    # ! (starting at x=42, y=8)
    exclamation1_pattern = [
        [1],
        [1],
        [1],
        [1],
        [1],
        [0],
        [1]
    ]
    
    # ! (starting at x=45, y=8)
    exclamation2_pattern = [
        [1],
        [1],
        [1],
        [1],
        [1],
        [0],
        [1]
    ]
    
    # Draw each letter with 3D effect (using gold for victory effect)
    letters = [
        (y_pattern, 2),    # Y
        (o_pattern, 8),    # O
        (u_pattern, 14),   # U
        (w_pattern, 22),   # W
        (o2_pattern, 28),  # O
        (n_pattern, 34),   # N
        (exclamation1_pattern, 42),  # !
        (exclamation2_pattern, 45)   # !
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
                            canvas[y + 1][x + 1] = BLACK
                        
                        # Draw main letter in victorious gold
                        canvas[y][x] = GOLD
                        
                        # Add highlights (top-left pixels)
                        if row_idx == 0 or (row_idx > 0 and pattern[row_idx-1][col_idx] == 0):
                            canvas[y][x] = LIGHT_GOLD
                        if col_idx == 0 or (col_idx > 0 and pattern[row_idx][col_idx-1] == 0):
                            canvas[y][x] = LIGHT_GOLD
    
    # Add decorative celebration frame
    frame_thickness = 1
    
    # Top and bottom borders (golden frame)
    for x in range(width):
        for t in range(frame_thickness):
            canvas[t][x] = GOLD
            canvas[height - 1 - t][x] = GOLD
    
    # Left and right borders
    for y in range(height):
        for t in range(frame_thickness):
            canvas[y][t] = GOLD
            canvas[y][width - 1 - t] = GOLD
    
    # Add corner decorations (victory laurels)
    corner_size = 3
    
    # Top-left laurel
    laurel_tl = [(0,2), (1,1), (1,2), (2,0), (2,1)]
    for dy, dx in laurel_tl:
        if dx < width and dy < height:
            canvas[dy][dx] = GREEN
    
    # Top-right laurel
    laurel_tr = [(0,width-3), (1,width-2), (1,width-3), (2,width-1), (2,width-2)]
    for dy, dx in laurel_tr:
        if dx >= 0 and dx < width and dy < height:
            canvas[dy][dx] = GREEN
    
    # Bottom-left laurel
    laurel_bl = [(height-3,0), (height-2,1), (height-2,2), (height-1,2)]
    for dy, dx in laurel_bl:
        if dx < width and dy >= 0 and dy < height:
            canvas[dy][dx] = GREEN
    
    # Bottom-right laurel
    laurel_br = [(height-3,width-1), (height-2,width-2), (height-2,width-3), (height-1,width-3)]
    for dy, dx in laurel_br:
        if dx >= 0 and dx < width and dy >= 0 and dy < height:
            canvas[dy][dx] = GREEN
    
    # Add victory symbols
    
    # Trophy icon (left side)
    trophy_x, trophy_y = 52, 4
    trophy_pixels = [
        (0, 1), (0, 2),              # trophy top
        (1, 0), (1, 1), (1, 2), (1, 3),  # trophy bowl
        (2, 1), (2, 2),              # trophy stem
        (3, 0), (3, 1), (3, 2), (3, 3)   # trophy base
    ]
    
    for dx, dy in trophy_pixels:
        x, y = trophy_x + dx, trophy_y + dy
        if x < width and y < height:
            if dy == 0:  # Trophy top
                canvas[y][x] = YELLOW
            elif dy in [1, 2]:  # Trophy bowl and stem
                canvas[y][x] = GOLD
            else:  # Trophy base
                canvas[y][x] = SILVER
    
    # Crown icon (right side)
    crown_x, crown_y = 58, 5
    crown_pixels = [
        (0, 0), (0, 2), (0, 4),      # crown points
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),  # crown band
    ]
    
    for dx, dy in crown_pixels:
        x, y = crown_x + dx, crown_y + dy
        if x < width and y < height:
            if dy == 0:  # Crown points
                canvas[y][x] = YELLOW
            else:  # Crown band
                canvas[y][x] = GOLD
    
    # Add celebration effects around the text
    # Star/sparkle effects (victory celebration)
    star_positions = [
        (4, 50), (6, 55), (10, 53), (12, 58),
        (4, 6), (6, 4), (10, 8), (12, 2)
    ]
    
    for sy, sx in star_positions:
        if sx < width and sy < height:
            canvas[sy][sx] = WHITE
            # Add star points
            if sx > 0:
                canvas[sy][sx-1] = YELLOW
            if sx < width-1:
                canvas[sy][sx+1] = YELLOW
            if sy > 0:
                canvas[sy-1][sx] = YELLOW
            if sy < height-1:
                canvas[sy+1][sx] = YELLOW
    
    # Confetti effects (celebration)
    confetti_positions = [
        (3, 52), (7, 56), (11, 54), (15, 58),
        (3, 8), (7, 6), (11, 10), (15, 4)
    ]
    
    for cy, cx in confetti_positions:
        if cx < width and cy < height:
            canvas[cy][cx] = GREEN
    
    # More confetti in different colors
    confetti2_positions = [
        (5, 51), (9, 57), (13, 55), (17, 59),
        (5, 7), (9, 5), (13, 9), (17, 3)
    ]
    
    for cy, cx in confetti2_positions:
        if cx < width and cy < height:
            canvas[cy][cx] = BLUE
    
    # Firework effects (victory celebration)
    firework_positions = [
        (2, 49), (18, 57), (2, 9), (18, 3)
    ]
    
    for fy, fx in firework_positions:
        if fx < width and fy < height:
            canvas[fy][fx] = WHITE
            # Add firework burst
            if fx > 0:
                canvas[fy][fx-1] = GREEN
            if fx < width-1:
                canvas[fy][fx+1] = GREEN
            if fy > 0:
                canvas[fy-1][fx] = YELLOW
            if fy < height-1:
                canvas[fy+1][fx] = YELLOW
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Save image
    output_path = 'art/you_won.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width * scale}x{height * scale} pixels")
    print(f"   Style: Minecraft-style pixel art victory message")
    print(f"   Features: YOU WON!! in golden text, 3D shading")
    print(f"   Details: Trophy, crown icons, stars/confetti effects")
    print(f"   Theme: Victory celebration with bright golden borders")

if __name__ == '__main__':
    create_you_won_logo()