"""
Create a PNG logo for "YOU LOST!" in Minecraft pixel art style
"""
from PIL import Image, ImageDraw
import numpy as np

def create_you_lost_logo():
    """Create a Minecraft-style YOU LOST! logo with pixel art"""
    # Create a larger canvas for pixel art logo (sized for YOU LOST!)
    width, height = 72, 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (dramatic colors for game over theme)
    RED = [220, 20, 60, 255]         # Main text color (defeat/danger)
    DARK_RED = [139, 0, 0, 255]      # Red shading
    LIGHT_RED = [255, 100, 100, 255] # Red highlights
    BLACK = [0, 0, 0, 255]           # Deep shadows
    DARK_GRAY = [64, 64, 64, 255]    # Gray shading
    GRAY = [128, 128, 128, 255]      # Border elements
    WHITE = [255, 255, 255, 255]     # Highlights/sparkles
    ORANGE = [255, 165, 0, 255]      # Fire/explosion effects
    YELLOW = [255, 255, 0, 255]      # Bright effects
    BROWN = [101, 67, 33, 255]       # Frame color
    DARK_BROWN = [60, 40, 20, 255]   # Frame shading
    PURPLE = [128, 0, 128, 255]      # Accent color
    
    # Draw "YOU LOST!" in blocky Minecraft-style letters
    
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
    
    # Space (2 pixels) then L (starting at x=22, y=8)
    l_pattern = [
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1]
    ]
    
    # O (starting at x=28, y=8) - second O
    o2_pattern = [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ]
    
    # S (starting at x=34, y=8)
    s_pattern = [
        [0,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [0,1,1,1,0],
        [0,0,0,0,1],
        [0,0,0,0,1],
        [1,1,1,1,0]
    ]
    
    # T (starting at x=40, y=8)
    t_pattern = [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ]
    
    # ! (starting at x=46, y=8)
    exclamation_pattern = [
        [1],
        [1],
        [1],
        [1],
        [1],
        [0],
        [1]
    ]
    
    # Draw each letter with 3D effect (using red for dramatic effect)
    letters = [
        (y_pattern, 2),    # Y
        (o_pattern, 8),    # O
        (u_pattern, 14),   # U
        (l_pattern, 22),   # L
        (o2_pattern, 28),  # O
        (s_pattern, 34),   # S
        (t_pattern, 40),   # T
        (exclamation_pattern, 46)  # !
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
                        
                        # Draw main letter in dramatic red
                        canvas[y][x] = RED
                        
                        # Add highlights (top-left pixels)
                        if row_idx == 0 or (row_idx > 0 and pattern[row_idx-1][col_idx] == 0):
                            canvas[y][x] = LIGHT_RED
                        if col_idx == 0 or (col_idx > 0 and pattern[row_idx][col_idx-1] == 0):
                            canvas[y][x] = LIGHT_RED
    
    # Add decorative border frame (darker/more ominous)
    # Top border
    for x in range(width):
        canvas[0][x] = DARK_GRAY
        canvas[1][x] = BLACK
        canvas[height-2][x] = DARK_GRAY
        canvas[height-1][x] = BLACK
    
    # Side borders
    for y in range(height):
        canvas[y][0] = DARK_GRAY
        canvas[y][1] = BLACK
        canvas[y][width-2] = DARK_GRAY
        canvas[y][width-1] = BLACK
    
    # Add corner decorations (skull/danger symbols)
    danger_corners = [(2, 2), (2, width-3), (height-3, 2), (height-3, width-3)]
    for cy, cx in danger_corners:
        if cx < width and cy < height:
            # Simple danger/skull motif
            canvas[cy][cx] = YELLOW
            canvas[cy][cx+1] = ORANGE
            canvas[cy+1][cx] = ORANGE
            canvas[cy+1][cx+1] = RED
    
    # Add game over themed decorative elements
    # Broken sword icon (left side) - representing defeat
    sword_x, sword_y = 4, 18
    broken_sword_pixels = [
        (0, 2), (1, 2),              # blade fragment 1
        (3, 2),                     # blade fragment 2 (broken)
        (4, 1), (4, 2), (4, 3),     # crossguard
        (5, 2), (6, 2)              # handle stub
    ]
    
    for dx, dy in broken_sword_pixels:
        x, y = sword_x + dx, sword_y + dy
        if x < width and y < height:
            if dx <= 1:  # First fragment
                canvas[y][x] = GRAY
            elif dx == 3:  # Broken piece
                canvas[y][x] = DARK_GRAY
            else:  # Handle
                canvas[y][x] = BROWN
    
    # Skull icon (right side) - representing death/defeat
    skull_x, skull_y = width - 12, 18
    skull_pixels = [
        (0, 1), (0, 2), (0, 3),      # skull top
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),  # skull body
        (2, 1), (2, 3),              # eye sockets
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),  # jaw
        (4, 1), (4, 2), (4, 3)       # bottom
    ]
    
    for dx, dy in skull_pixels:
        x, y = skull_x + dx, skull_y + dy
        if x < width and y < height:
            if dy in [1, 3] and dx == 2:  # Eye sockets
                canvas[y][x] = BLACK
            else:  # Skull body
                canvas[y][x] = WHITE
    
    # Add dramatic effects around the text
    # Fire/explosion effects (indicating destruction)
    fire_positions = [
        (6, 50), (12, 54), (18, 52), (24, 56),
        (6, 6), (12, 4), (18, 6), (24, 4)
    ]
    
    for fy, fx in fire_positions:
        if fx < width and fy < height:
            canvas[fy][fx] = ORANGE
            if fy + 1 < height:
                canvas[fy + 1][fx] = YELLOW
    
    # Lightning/energy effects (showing impact)
    lightning_positions = [
        (4, 52), (10, 56), (16, 54), (22, 58),
        (4, 8), (10, 6), (16, 8), (22, 6)
    ]
    
    for ly, lx in lightning_positions:
        if lx < width and ly < height:
            canvas[ly][lx] = WHITE
    
    # Smoke effects (aftermath)
    smoke_positions = [
        (5, 48), (11, 50), (17, 49), (23, 51),
        (5, 10), (11, 8), (17, 10), (23, 8)
    ]
    
    for sy, sx in smoke_positions:
        if sx < width and sy < height:
            canvas[sy][sx] = GRAY
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Save image
    output_path = 'art/you_lost.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width * scale}x{height * scale} pixels")
    print(f"   Style: Minecraft-style pixel art game over message")
    print(f"   Features: YOU LOST! in dramatic red text, 3D shading")
    print(f"   Details: Broken sword, skull icons, fire/lightning effects")
    print(f"   Theme: Game over/defeat with ominous dark borders")

if __name__ == '__main__':
    create_you_lost_logo()