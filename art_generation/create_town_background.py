"""
Create a pixel art town background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random
import math

def create_town_background():
    """Create a pixel art fantasy town square based on reference"""
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # === COLORS ===
    # Sky
    SKY_BLUE = [100, 180, 240, 255]
    CLOUD_WHITE = [255, 255, 255, 255]
    
    # Landscape
    GRASS_LIGHT = [100, 180, 60, 255]
    GRASS_DARK = [60, 140, 40, 255]
    
    # Buildings (Stone)
    STONE_LIGHT = [180, 180, 190, 255]
    STONE_MID = [140, 140, 150, 255]
    STONE_DARK = [100, 100, 110, 255]
    MOSS_GREEN = [80, 140, 60, 255]
    
    # Buildings (Wood/Plaster)
    WALL_CREAM = [240, 230, 200, 255]
    WOOD_BROWN = [100, 70, 40, 255]
    ROOF_RED = [180, 80, 70, 255]
    ROOF_DARK = [140, 50, 40, 255]
    
    # Ground
    COBBLE_LIGHT = [170, 170, 160, 255]
    COBBLE_DARK = [140, 140, 130, 255]
    
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

    # === 1. SKY ===
    for y in range(height):
        for x in range(width):
            if y < 40:
                draw_pixel(x, y, SKY_BLUE)
                
    # Clouds
    for i in range(8):
        cx = random.randint(0, width)
        cy = random.randint(0, 25)
        r = random.randint(5, 15)
        for y in range(cy - r, cy + r):
            for x in range(cx - r*2, cx + r*2):
                if ((x-cx)/(r*2))**2 + ((y-cy)/r)**2 < 1.0:
                    draw_pixel(x, y, CLOUD_WHITE)

    # === 2. BACKGROUND HILLS ===
    for x in range(width):
        # Rolling hills
        hy = 35 + int(math.sin(x * 0.05) * 5)
        for y in range(hy, 45):
            draw_pixel(x, y, GRASS_LIGHT)
            
    # Distant houses on hills
    for i in range(3):
        hx = 40 + i * 30
        hy = 32 + (i % 2) * 3
        # Tiny house
        for y in range(hy, hy + 6):
            for x in range(hx, hx + 6):
                draw_pixel(x, y, WALL_CREAM)
        # Roof
        for y in range(hy - 3, hy):
            for x in range(hx - 1, hx + 7):
                if y > hy - 3 + abs(x - (hx + 3)) * 0.5:
                    draw_pixel(x, y, ROOF_RED)

    # === 3. MIDGROUND BUILDINGS ===
    
    # Large Stone Church (Right side)
    cx = 85
    cy = 45
    cw = 30
    ch = 35
    
    # Main body
    for y in range(cy - ch, cy):
        for x in range(cx, cx + cw):
            col = STONE_MID
            if x % 10 == 0 or y % 8 == 0: col = STONE_DARK # Bricks
            if random.random() > 0.9: col = MOSS_GREEN # Moss
            draw_pixel(x, y, col)
            
    # Tower
    tx = cx + 5
    for y in range(cy - ch - 15, cy - ch):
        for x in range(tx, tx + 12):
            draw_pixel(x, y, STONE_MID)
            
    # Tower Roof
    for y in range(cy - ch - 25, cy - ch - 15):
        for x in range(tx - 2, tx + 14):
            # Pointed roof
            width_at_y = (y - (cy - ch - 25)) * 1.5
            if abs(x - (tx + 6)) < width_at_y:
                draw_pixel(x, y, ROOF_RED)
                
    # Church Door (Arched)
    dx = cx + 10
    dy = cy
    for y in range(dy - 12, dy):
        for x in range(dx, dx + 10):
            if y > dy - 8 or ((x - (dx+5))**2 + (y - (dy-8))**2 < 20):
                draw_pixel(x, y, WOOD_BROWN)
                
    # Timber Houses (Left side)
    for i in range(2):
        hx = 5 + i * 35
        hy = 48
        hw = 25
        hh = 20
        
        # Walls
        for y in range(hy - hh, hy):
            for x in range(hx, hx + hw):
                col = WALL_CREAM
                # Timber framing
                if x == hx or x == hx + hw - 1 or y == hy - hh or y == hy - 1:
                    col = WOOD_BROWN
                if (x - hx) % 12 == 0: col = WOOD_BROWN
                # Removed diagonal cross beam
                draw_pixel(x, y, col)
                
        # Doors
        dx = hx + hw // 2 - 4
        dy = hy
        for y in range(dy - 10, dy):
            for x in range(dx, dx + 8):
                # Arched top
                if y > dy - 8 or ((x - (dx+3.5))**2 + (y - (dy-8))**2 < 16):
                    draw_pixel(x, y, WOOD_BROWN)
                    # Iron banding
                    if y == dy - 5 or y == dy - 9:
                        draw_pixel(x, y, [60, 60, 70, 255])
                    # Handle
                    if x == dx + 6 and y == dy - 5:
                        draw_pixel(x, y, [200, 200, 50, 255])

        # Roof
        for y in range(hy - hh - 10, hy - hh):
            for x in range(hx - 2, hx + hw + 2):
                center = hx + hw // 2
                if abs(x - center) < (y - (hy - hh - 10)) * 1.5:
                    draw_pixel(x, y, ROOF_RED)

    # === 4. FOREGROUND ===
    
    # Cobblestone Ground
    for y in range(45, height):
        for x in range(width):
            col = COBBLE_LIGHT
            # Perspective stones
            scale = (y - 45) / 20.0 + 0.5
            if (x + (y%2)*5) % int(8 * scale) == 0 or y % int(4 * scale) == 0:
                col = COBBLE_DARK
            draw_pixel(x, y, col)
            
    # Fountain (Center Foreground)
    fx = width // 2
    fy = 58
    
    # Water pool base
    for y in range(fy - 3, fy + 5):
        for x in range(fx - 20, fx + 20):
            # Ellipse pool
            if ((x-fx)/20)**2 + ((y-fy)/4)**2 < 1.0:
                draw_pixel(x, y, STONE_MID) # Rim
                # Water inside
                if ((x-fx)/16)**2 + ((y-fy)/3)**2 < 1.0:
                     draw_pixel(x, y, [60, 160, 220, 255])
                     # Ripples
                     if random.random() > 0.9:
                         draw_pixel(x, y, [200, 240, 255, 200])

    # Center pillar
    for y in range(fy - 12, fy):
        for x in range(fx - 3, fx + 4):
             draw_pixel(x, y, STONE_MID)
             if x == fx - 3 or x == fx + 3: draw_pixel(x, y, STONE_DARK)

    # Top bowl
    by = fy - 12
    for y in range(by - 2, by + 2):
        for x in range(fx - 8, fx + 8):
            if ((x-fx)/8)**2 + ((y-by)/2)**2 < 1.0:
                draw_pixel(x, y, STONE_MID)
                
    # Water spray
    for i in range(20):
        sx = fx + random.randint(-2, 2)
        sy = by - random.randint(0, 8)
        draw_pixel(sx, sy, [200, 240, 255, 200])
        # Falling water
        if random.random() > 0.5:
            ox = random.randint(-6, 6)
            oy = by + random.randint(2, 10)
            draw_pixel(fx + ox, oy, [150, 200, 255, 180])

    # Stairs (Right Foreground)
    sx = 100
    sy = 50
    for i in range(5):
        step_y = sy + i * 3
        step_x = sx + i * 4
        for y in range(step_y, height):
            for x in range(step_x, width):
                draw_pixel(x, y, STONE_LIGHT)
                if y == step_y: draw_pixel(x, y, STONE_MID) # Step edge

    # Save image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 4x
    scale_factor = 4
    final_width = width * scale_factor
    final_height = height * scale_factor
    img = img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    img.save('art/town_background.png')
    print(f"✓ Saved: art/town_background.png ({final_width}x{final_height})")

if __name__ == "__main__":
    create_town_background()
