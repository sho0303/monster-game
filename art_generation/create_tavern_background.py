"""
Create a pixel art tavern background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random
import math

def create_tavern_background():
    """Create a pixel art fantasy tavern interior"""
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # === COLORS ===
    # Wood (Floor, Bar, Tables)
    WOOD_DARK = [60, 40, 20, 255]
    WOOD_MID = [90, 60, 30, 255]
    WOOD_LIGHT = [120, 80, 40, 255]
    WOOD_HIGHLIGHT = [150, 100, 50, 255]
    
    # Walls (Plaster/Stone)
    WALL_BASE = [180, 170, 150, 255]
    WALL_SHADOW = [140, 130, 110, 255]
    BEAM_COLOR = [50, 30, 15, 255]
    
    # Fireplace
    STONE_DARK = [50, 50, 60, 255]
    STONE_LIGHT = [100, 100, 110, 255]
    FIRE_ORANGE = [255, 100, 0, 255]
    FIRE_YELLOW = [255, 200, 0, 255]
    
    # Bottles/Decor
    BOTTLE_GREEN = [50, 150, 50, 255]
    BOTTLE_RED = [150, 50, 50, 255]
    BOTTLE_BLUE = [50, 50, 150, 255]
    GOLD = [255, 215, 0, 255]
    
    # Helper to draw pixel
    def draw_pixel(x, y, color):
        if 0 <= x < width and 0 <= y < height:
            if len(color) == 4 and color[3] < 255:
                current = canvas[y][x]
                alpha = color[3] / 255.0
                for c in range(3):
                    canvas[y][x][c] = int(current[c] * (1 - alpha) + color[c] * alpha)
                canvas[y][x][3] = 255
            else:
                canvas[y][x] = color

    # === 1. BACKGROUND (Walls & Floor) ===
    
    # Floor (Bottom 1/3)
    floor_y = 40
    for y in range(height):
        for x in range(width):
            if y >= floor_y:
                # Wooden floor planks
                col = WOOD_MID
                # Plank lines
                if (y - floor_y) % 6 == 0: col = WOOD_DARK
                # Random grain
                if random.random() > 0.9: col = WOOD_LIGHT
                draw_pixel(x, y, col)
            else:
                # Wall
                col = WALL_BASE
                # Shadow near ceiling
                if y < 10: col = WALL_SHADOW
                # Shadow in corners
                if x < 10 or x > width - 10: col = WALL_SHADOW
                draw_pixel(x, y, col)

    # Ceiling Beams
    for x in range(0, width, 30):
        for y in range(0, floor_y):
            # Vertical beams
            if x < width:
                draw_pixel(x, y, BEAM_COLOR)
                draw_pixel(x+1, y, BEAM_COLOR)
                
    # Horizontal beam at top
    for x in range(width):
        for y in range(4):
            draw_pixel(x, y, BEAM_COLOR)

    # === 2. FIREPLACE (Right Side) ===
    fx = width - 30
    fy = floor_y - 15
    fw = 20
    fh = 15
    
    # Chimney
    for y in range(0, fy):
        for x in range(fx + 4, fx + fw - 4):
            draw_pixel(x, y, STONE_LIGHT)
            if x == fx + 4 or x == fx + fw - 5: draw_pixel(x, y, STONE_DARK)
            
    # Hearth
    for y in range(fy, floor_y):
        for x in range(fx, fx + fw):
            draw_pixel(x, y, STONE_DARK)
            # Bricks
            if (x + y) % 4 == 0: draw_pixel(x, y, STONE_LIGHT)
            
    # Fire pit (black hole)
    for y in range(fy + 5, floor_y):
        for x in range(fx + 4, fx + fw - 4):
            draw_pixel(x, y, [20, 10, 10, 255])
            
    # Fire
    for i in range(20):
        fire_x = random.randint(fx + 5, fx + fw - 5)
        fire_y = random.randint(fy + 8, floor_y - 1)
        draw_pixel(fire_x, fire_y, FIRE_ORANGE)
        if random.random() > 0.5:
            draw_pixel(fire_x, fire_y - 1, FIRE_YELLOW)

    # === 3. BAR COUNTER (Left/Back) ===
    bx = 10
    by = floor_y - 10
    bw = 60
    bh = 12
    
    # Back shelves
    for y in range(by - 15, by):
        for x in range(bx, bx + bw):
            if (y - (by-15)) % 8 == 0: # Shelf lines
                draw_pixel(x, y, WOOD_DARK)
            elif x % 10 == 0: # Vertical supports
                draw_pixel(x, y, WOOD_DARK)
                
    # Bottles on shelves
    for i in range(15):
        bottle_x = random.randint(bx + 2, bx + bw - 2)
        bottle_y = random.choice([by - 16, by - 8])
        color = random.choice([BOTTLE_GREEN, BOTTLE_RED, BOTTLE_BLUE])
        draw_pixel(bottle_x, bottle_y, color)
        draw_pixel(bottle_x, bottle_y - 1, color)
        draw_pixel(bottle_x, bottle_y - 2, [200, 200, 200, 150]) # Neck

    # Counter Top
    for y in range(by, by + bh):
        for x in range(bx, bx + bw):
            col = WOOD_MID
            if y == by: col = WOOD_HIGHLIGHT # Top edge
            if y > by + 2: col = WOOD_DARK # Front face shadow
            draw_pixel(x, y, col)

    # === 4. TABLES AND CHAIRS (Foreground) ===
    
    tables = [(40, 50), (90, 55)]
    
    for tx, ty in tables:
        # Table Top (Round-ish)
        for y in range(ty - 2, ty + 3):
            for x in range(tx - 8, tx + 8):
                if ((x-tx)/8)**2 + ((y-ty)/3)**2 < 1.0:
                    draw_pixel(x, y, WOOD_LIGHT)
                    if y == ty - 2: draw_pixel(x, y, WOOD_HIGHLIGHT)
                    
        # Table Legs
        for y in range(ty + 3, ty + 8):
            draw_pixel(tx - 4, y, WOOD_DARK)
            draw_pixel(tx + 4, y, WOOD_DARK)
            
        # Stools
        for sx in [tx - 12, tx + 12]:
            sy = ty + 2
            # Seat
            for x in range(sx - 2, sx + 3):
                draw_pixel(x, sy, WOOD_MID)
            # Legs
            for y in range(sy + 1, sy + 5):
                draw_pixel(sx - 2, y, WOOD_DARK)
                draw_pixel(sx + 2, y, WOOD_DARK)

    # === 5. LIGHTING EFFECTS ===
    # Warm glow from fireplace
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - (fx + fw//2))**2 + (y - (floor_y - 5))**2)
            if dist < 40:
                # Add warm tint
                intensity = (40 - dist) / 40.0 * 0.3
                current = canvas[y][x]
                r = min(255, int(current[0] + 100 * intensity))
                g = min(255, int(current[1] + 50 * intensity))
                canvas[y][x][0] = r
                canvas[y][x][1] = g

    # Save image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 4x
    scale_factor = 4
    final_width = width * scale_factor
    final_height = height * scale_factor
    img = img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    img.save('art/tavern_background.png')
    print(f"✓ Saved: art/tavern_background.png ({final_width}x{final_height})")

if __name__ == "__main__":
    create_tavern_background()
