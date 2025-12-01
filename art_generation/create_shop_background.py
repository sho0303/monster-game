"""
Create a pixel art shop background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random
import math

def create_shop_background():
    """Create a pixel art fantasy shop interior"""
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # === COLORS ===
    # Wood (Floor, Counter, Shelves)
    WOOD_DARK = [70, 40, 20, 255]
    WOOD_MID = [100, 60, 30, 255]
    WOOD_LIGHT = [130, 80, 40, 255]
    WOOD_HIGHLIGHT = [160, 100, 50, 255]
    
    # Stone (Walls)
    STONE_DARK = [60, 60, 70, 255]
    STONE_MID = [90, 90, 100, 255]
    STONE_LIGHT = [120, 120, 130, 255]
    
    # Background/Shadows
    SHADOW = [30, 20, 10, 100] # Semi-transparent shadow
    BLACK = [0, 0, 0, 255]
    
    # Items on shelves
    POTION_RED = [200, 50, 50, 255]
    POTION_BLUE = [50, 50, 200, 255]
    POTION_GREEN = [50, 200, 50, 255]
    GOLD = [255, 215, 0, 255]
    STEEL = [150, 150, 170, 255]
    
    # Helper to draw pixel
    def draw_pixel(x, y, color):
        if 0 <= x < width and 0 <= y < height:
            # Simple alpha blending
            if len(color) == 4 and color[3] < 255:
                current = canvas[y][x]
                alpha = color[3] / 255.0
                for c in range(3):
                    canvas[y][x][c] = int(current[c] * (1 - alpha) + color[c] * alpha)
                canvas[y][x][3] = 255 # Assume opaque result for simplicity
            else:
                canvas[y][x] = color

    # === 1. WALLS & FLOOR ===
    floor_y = 40 # Where the wall meets the floor
    
    # Draw Wall (Stone bricks)
    for y in range(floor_y):
        for x in range(width):
            # Base wall color
            col = STONE_MID
            
            # Brick pattern
            brick_h = 8
            brick_w = 16
            row = y // brick_h
            offset = (row % 2) * (brick_w // 2)
            
            # Mortar lines
            if y % brick_h == 0 or (x + offset) % brick_w == 0:
                col = STONE_DARK
            # Highlights
            elif y % brick_h == 1 or (x + offset) % brick_w == 1:
                col = STONE_LIGHT
            # Texture
            elif (x * y * 13) % 100 < 5:
                col = STONE_DARK
                
            draw_pixel(x, y, col)
            
    # Draw Floor (Wood planks)
    for y in range(floor_y, height):
        for x in range(width):
            # Perspective effect for planks?
            # Simple horizontal planks for now
            col = WOOD_MID
            
            plank_h = 6
            if (y - floor_y) % plank_h == 0:
                col = WOOD_DARK
            elif (x * y * 7) % 100 < 5: # Wood grain
                col = WOOD_LIGHT
                
            draw_pixel(x, y, col)

    # === 2. SHELVES (Background) ===
    shelf_y_positions = [15, 28]
    shelf_depth = 4
    
    for sy in shelf_y_positions:
        # Draw shelf board
        for x in range(10, width - 10):
            # Shelf shadow underneath
            for y in range(sy + 1, sy + 4):
                draw_pixel(x, y, SHADOW)
                
            # Shelf top
            draw_pixel(x, sy, WOOD_LIGHT)
            # Shelf front face
            draw_pixel(x, sy + 1, WOOD_DARK)
            
        # Draw items on shelf
        for x in range(15, width - 15, 8):
            if random.random() > 0.3: # 70% chance of item
                item_type = random.choice(['potion', 'book', 'ingot'])
                
                if item_type == 'potion':
                    color = random.choice([POTION_RED, POTION_BLUE, POTION_GREEN])
                    # Bottle shape
                    draw_pixel(x, sy - 1, color)
                    draw_pixel(x, sy - 2, color)
                    draw_pixel(x, sy - 3, [200, 200, 200, 150]) # Glass neck
                    
                elif item_type == 'book':
                    color = random.choice([[100, 50, 50, 255], [50, 50, 100, 255]])
                    # Book spine
                    for by in range(1, 5):
                        draw_pixel(x, sy - by, color)
                        draw_pixel(x+1, sy - by, color)
                        
                elif item_type == 'ingot':
                    # Stack of gold/steel
                    color = random.choice([GOLD, STEEL])
                    draw_pixel(x, sy - 1, color)
                    draw_pixel(x+1, sy - 1, color)
                    draw_pixel(x+2, sy - 1, color)
                    draw_pixel(x+1, sy - 2, color)

    # === 3. COUNTER (Foreground) ===
    counter_top_y = 45
    counter_height = height - counter_top_y
    
    for y in range(counter_top_y, height):
        for x in range(width):
            # Counter takes up full width? Or maybe centered?
            # Let's make it full width for the "shop view" feel
            
            # Counter Top Surface (perspective)
            if y < counter_top_y + 5:
                col = WOOD_LIGHT
                if y == counter_top_y:
                    col = WOOD_HIGHLIGHT # Edge highlight
                elif (x * 3) % 20 == 0: # Wood grain
                    col = WOOD_MID
            # Counter Front Face
            else:
                col = WOOD_MID
                # Vertical panels
                if x % 32 == 0 or x % 32 == 31:
                    col = WOOD_DARK
                # Wood grain texture
                elif (x * y * 17) % 100 < 5:
                    col = WOOD_DARK
                # Shadow under the lip
                if y == counter_top_y + 5:
                    col = SHADOW
                    
            draw_pixel(x, y, col)

    # === 4. LIGHTING/ATMOSPHERE ===
    # Vignette
    for y in range(height):
        for x in range(width):
            dist_from_center = ((x - width/2)**2 + (y - height/2)**2)**0.5
            max_dist = (width/2)**2 + (height/2)**2
            
            if dist_from_center > 40:
                opacity = int((dist_from_center - 40) * 2)
                if opacity > 150: opacity = 150
                draw_pixel(x, y, [0, 0, 0, opacity])

    # Save image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 4x (matching ocean background)
    scale_factor = 4
    final_width = width * scale_factor
    final_height = height * scale_factor
    img = img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    img.save('art/shop_background.png')
    print(f"✓ Saved: art/shop_background.png ({final_width}x{final_height})")

if __name__ == "__main__":
    print("Creating shop background...")
    create_shop_background()
    print("✅ Shop background creation complete!")
