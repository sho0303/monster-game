"""
Create a pixel art blacksmith background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random
import math

def create_blacksmith_background():
    """Create a pixel art fantasy blacksmith shop based on stone forge inspiration"""
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # === COLORS ===
    # Stone (Walls, Forge, Floor)
    STONE_DARK = [40, 40, 45, 255]
    STONE_MID = [70, 70, 75, 255]
    STONE_LIGHT = [100, 100, 105, 255]
    STONE_HIGHLIGHT = [130, 130, 135, 255]
    
    # Wood (Beams, Tools, Barrel)
    WOOD_DARK = [50, 30, 15, 255]
    WOOD_MID = [90, 50, 25, 255]
    WOOD_LIGHT = [120, 70, 35, 255]
    
    # Fire
    FIRE_CORE = [255, 255, 200, 255]
    FIRE_YELLOW = [255, 220, 50, 255]
    FIRE_ORANGE = [255, 100, 20, 255]
    FIRE_RED = [180, 50, 10, 255]
    
    # Metal (Anvil, Tools)
    METAL_DARK = [30, 35, 40, 255]
    METAL_MID = [60, 70, 80, 255]
    METAL_LIGHT = [100, 110, 120, 255]
    
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

    # === 1. STRUCTURE (Walls & Floor) ===
    floor_y = 45
    
    # Back Wall (Stone Bricks)
    for y in range(floor_y):
        for x in range(width):
            col = STONE_MID
            # Brick pattern
            if (y % 8 == 0) or ((y // 8) % 2 == 0 and x % 16 == 0) or ((y // 8) % 2 == 1 and (x + 8) % 16 == 0):
                col = STONE_DARK
            elif (x * y * 13) % 100 < 10:
                col = STONE_LIGHT
            draw_pixel(x, y, col)
            
    # Floor (Stone Tiles)
    for y in range(floor_y, height):
        for x in range(width):
            col = STONE_MID
            # Perspective lines
            if (x - width/2) * (y - floor_y + 10) % 400 < 10 or y % 10 == 0:
                col = STONE_DARK
            draw_pixel(x, y, col)

    # Roof Beams
    # Main horizontal beam
    beam_y = 15
    for y in range(beam_y, beam_y + 6):
        for x in range(width):
            col = WOOD_MID
            if y == beam_y + 5: col = WOOD_DARK # Shadow
            if (x * 7) % 20 == 0: col = WOOD_DARK # Grain
            draw_pixel(x, y, col)

    # === 2. THE FORGE (Central Arch) ===
    arch_cx = width // 2
    arch_cy = 45
    arch_w = 25
    arch_h = 25
    
    # Draw Arch Stones
    for y in range(arch_cy - arch_h - 5, arch_cy + 1):
        for x in range(arch_cx - arch_w - 5, arch_cx + arch_w + 5):
            # Ellipse equation for arch
            dx = (x - arch_cx)
            dy = (y - arch_cy)
            
            # Outer curve
            if (dx/(arch_w+4))**2 + (dy/(arch_h+4))**2 <= 1.0:
                # Inner curve (hole)
                if (dx/arch_w)**2 + (dy/arch_h)**2 > 1.0 or y > arch_cy:
                    # This is the stone frame
                    col = STONE_LIGHT
                    # Radial lines for arch stones
                    angle = math.atan2(dy, dx)
                    if int(angle * 10) % 4 == 0:
                        col = STONE_DARK
                    draw_pixel(x, y, col)
                else:
                    # Inside the forge (Fire background)
                    # Brick interior
                    col = [50, 30, 20, 255]
                    if (x + y) % 5 == 0: col = [40, 20, 10, 255]
                    draw_pixel(x, y, col)

    # Fire (Realistic Flames: Blue -> White -> Yellow -> Red)
    fire_base_y = arch_cy
    FIRE_BLUE = [50, 100, 255, 255]
    FIRE_WHITE = [255, 255, 255, 255]
    
    for x in range(arch_cx - 12, arch_cx + 13):
        # Calculate flame height based on position (higher in middle) and randomness
        dist = abs(x - arch_cx)
        max_h = 18 - dist
        if max_h < 2: max_h = 2
        
        h = random.randint(int(max_h * 0.7), max_h)
        
        for y in range(fire_base_y - h, fire_base_y + 1):
            # Gradient
            rel_h = (fire_base_y - y) / h # 0 at bottom, 1 at top
            
            if rel_h < 0.15: col = FIRE_BLUE
            elif rel_h < 0.4: col = FIRE_WHITE
            elif rel_h < 0.7: col = FIRE_YELLOW
            else: col = FIRE_RED
            
            draw_pixel(x, y, col)
            
    # Glow on floor from fire
    for i in range(20):
        fx = random.randint(arch_cx - 15, arch_cx + 15)
        fy = random.randint(arch_cy, arch_cy + 5)
        if random.random() > 0.5:
            draw_pixel(fx, fy, FIRE_ORANGE)

    # === 3. ANVIL (Center Foreground) ===
    anvil_x = width // 2
    anvil_y = 52  # Moved down slightly
    
    # Stone Base
    for y in range(anvil_y + 4, anvil_y + 8):
        for x in range(anvil_x - 10, anvil_x + 10):
            # Circular base
            if ((x - anvil_x)/10)**2 + ((y - (anvil_y+6))/3)**2 <= 1.0:
                draw_pixel(x, y, STONE_LIGHT)
                if x > anvil_x + 5: draw_pixel(x, y, STONE_DARK) # Shadow
                
    # Anvil Body
    for y in range(anvil_y - 2, anvil_y + 5):
        for x in range(anvil_x - 12, anvil_x + 12):
            # Silhouette logic
            draw = False
            # Top
            if y < anvil_y and abs(x - anvil_x) < 12: draw = True
            # Neck
            if y >= anvil_y and y < anvil_y + 3 and abs(x - anvil_x) < 5: draw = True
            # Base
            if y >= anvil_y + 3 and abs(x - anvil_x) < 8: draw = True
            
            if draw:
                col = METAL_MID
                if y == anvil_y - 2: col = METAL_LIGHT # Top surface
                if x > anvil_x + 2: col = METAL_DARK # Shadow side
                draw_pixel(x, y, col)

    # === 4. CLUTTER & TOOLS ===
    
    # Barrel (Right)
    barrel_x = width - 20
    barrel_y = 45
    for y in range(barrel_y, barrel_y + 15):
        for x in range(barrel_x - 6, barrel_x + 6):
            # Barrel curve
            width_mod = 6
            if y < barrel_y + 2 or y > barrel_y + 12: width_mod = 5
            
            if abs(x - barrel_x) < width_mod:
                col = WOOD_MID
                if x > barrel_x + 2: col = WOOD_DARK
                # Metal bands
                if y == barrel_y + 3 or y == barrel_y + 11:
                    col = METAL_DARK
                draw_pixel(x, y, col)
                
    # Stool (Left)
    stool_x = 20
    stool_y = 48
    # Seat
    for x in range(stool_x - 5, stool_x + 5):
        draw_pixel(x, stool_y, WOOD_LIGHT)
        draw_pixel(x, stool_y + 1, WOOD_DARK)
    # Legs
    for y in range(stool_y + 2, stool_y + 8):
        draw_pixel(stool_x - 4, y, WOOD_MID)
        draw_pixel(stool_x + 3, y, WOOD_MID)
    
    # Swords on Wall (Display)
    for sx in [15, width - 15]:
        sy = 25
        # Pommel
        draw_pixel(sx, sy, METAL_DARK)
        # Grip
        draw_pixel(sx, sy + 1, WOOD_DARK)
        draw_pixel(sx, sy + 2, WOOD_DARK)
        # Crossguard
        draw_pixel(sx - 2, sy + 3, METAL_DARK)
        draw_pixel(sx - 1, sy + 3, METAL_DARK)
        draw_pixel(sx, sy + 3, METAL_MID)
        draw_pixel(sx + 1, sy + 3, METAL_DARK)
        draw_pixel(sx + 2, sy + 3, METAL_DARK)
        # Blade
        for i in range(12):
            draw_pixel(sx, sy + 4 + i, METAL_LIGHT)
            draw_pixel(sx - 1, sy + 4 + i, METAL_MID) # Shadow/Edge
            
    # Tongs hanging on wall (Left of arch)
    tx = arch_cx - 20
    ty = 30
    for i in range(8):
        draw_pixel(tx, ty + i, METAL_DARK)
        draw_pixel(tx + 2, ty + i, METAL_DARK)
    draw_pixel(tx + 1, ty + 2, METAL_DARK) # Hinge

    # === 5. LIGHTING ===
    # Warm glow from the fire
    for y in range(height):
        for x in range(width):
            # Distance from fire center
            dist = ((x - arch_cx)**2 + (y - (arch_cy - 5))**2)**0.5
            
            if dist < 40:
                intensity = int((40 - dist) * 4)
                if intensity > 0:
                    current = canvas[y][x]
                    # Add orange/yellow tint
                    # Cast to int to avoid overflow
                    r = min(255, int(current[0]) + intensity)
                    g = min(255, int(current[1]) + int(intensity * 0.6))
                    b = min(255, int(current[2]) + int(intensity * 0.1))
                    canvas[y][x] = [r, g, b, 255]

    # Vignette
    for y in range(height):
        for x in range(width):
            dist_center = ((x - width/2)**2 + (y - height/2)**2)**0.5
            if dist_center > 45:
                opacity = int((dist_center - 45) * 4)
                if opacity > 180: opacity = 180
                
                current = canvas[y][x]
                factor = (255 - opacity) / 255.0
                canvas[y][x] = [
                    int(current[0] * factor),
                    int(current[1] * factor),
                    int(current[2] * factor),
                    255
                ]

    # Save image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 4x
    scale_factor = 4
    final_width = width * scale_factor
    final_height = height * scale_factor
    img = img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    img.save('art/blacksmith_background.png')
    print(f"✓ Saved: art/blacksmith_background.png ({final_width}x{final_height})")

if __name__ == "__main__":
    print("Creating blacksmith background...")
    create_blacksmith_background()
    print("✅ Blacksmith background creation complete!")
