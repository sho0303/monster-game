"""
Spider Queen Monster Creator
Creates pixel art for a Spider Queen (Drider-like): Female upper body, spider lower body.
Inspired by the concept of a pale-skinned queen with a red/brown armored spider body.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art
"""

from PIL import Image
import numpy as np
import random

def create_spiderqueen_default():
    """Create the default Spider Queen pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # --- Palette ---
    # Spider Body (Red/Brown/Dark)
    SPIDER_BASE = [80, 20, 20, 255]
    SPIDER_MID = [120, 40, 40, 255]
    SPIDER_HIGHLIGHT = [160, 60, 60, 255]
    SPIDER_SHADOW = [40, 10, 10, 255]
    SPIDER_GLOW = [255, 100, 50, 255] # Glowing sacs
    
    # Legs
    LEG_DARK = [50, 20, 20, 255]
    LEG_MID = [100, 40, 40, 255]
    LEG_TIP = [30, 10, 10, 255]
    
    # Human Upper Body (Pale Blueish)
    SKIN_BASE = [180, 200, 210, 255]
    SKIN_SHADOW = [140, 160, 170, 255]
    SKIN_HIGHLIGHT = [220, 230, 240, 255]
    
    # Armor/Clothing (Red/Gold)
    ARMOR_RED = [140, 30, 30, 255]
    ARMOR_DARK = [80, 10, 10, 255]
    ARMOR_TRIM = [180, 140, 60, 255] # Goldish
    
    # Hair/Horns
    HAIR_DARK = [20, 20, 30, 255]
    HORN_BONE = [200, 190, 180, 255]
    
    # Eyes
    EYE_GLOW = [220, 255, 50, 255] # Yellow/Green
    
    center_x = 32
    
    # === 1. Spider Lower Body ===
    # Bulbous abdomen at the back
    abdomen_center_x = 32
    abdomen_center_y = 45
    
    for y in range(35, 60):
        for x in range(15, 50):
            dx = x - abdomen_center_x
            dy = y - abdomen_center_y
            
            # Abdomen shape (oval)
            if (dx*dx)/(16*16) + (dy*dy)/(12*12) <= 1.0:
                # Base color
                color = SPIDER_BASE
                
                # Shading (bottom darker)
                if dy > 3: color = SPIDER_SHADOW
                # Highlight (top)
                elif dy < -3: color = SPIDER_MID
                
                # Glowing sacs/spots on the abdomen
                if (x % 6 == 0 and y % 5 == 0) and dy > 0:
                    color = SPIDER_GLOW
                
                canvas[y, x] = color

    # === 2. Spider Legs ===
    # 8 legs coming out from the "waist" area (around y=40)
    # We'll draw 4 on each side.
    
    leg_origins = [
        (24, 42), (22, 44), (20, 46), (18, 48), # Left side origins
        (40, 42), (42, 44), (44, 46), (46, 48)  # Right side origins
    ]
    
    # Leg paths (simplified jointed legs)
    # Left legs
    leg_paths_left = [
        [(-5, -5), (-5, 10)], # Front-ish
        [(-8, -2), (-4, 12)],
        [(-8, 2), (-2, 10)],
        [(-6, 5), (-1, 8)]    # Back-ish
    ]
    
    # Draw Left Legs
    for i, (ox, oy) in enumerate(leg_origins[:4]):
        path = leg_paths_left[i]
        # Segment 1: Body to Joint
        jx, jy = ox + path[0][0], oy + path[0][1]
        _draw_line(canvas, ox, oy, jx, jy, LEG_MID)
        # Segment 2: Joint to Tip
        tx, ty = jx + path[1][0], jy + path[1][1]
        _draw_line(canvas, jx, jy, tx, ty, LEG_DARK)
        # Tip
        if 0 <= tx < width and 0 <= ty < height:
            canvas[ty, tx] = LEG_TIP

    # Draw Right Legs (Mirrored logic)
    for i, (ox, oy) in enumerate(leg_origins[4:]):
        path = leg_paths_left[i] # Reuse relative offsets but mirror X
        # Segment 1
        jx, jy = ox - path[0][0], oy + path[0][1]
        _draw_line(canvas, ox, oy, jx, jy, LEG_MID)
        # Segment 2
        tx, ty = jx - path[1][0], jy + path[1][1]
        _draw_line(canvas, jx, jy, tx, ty, LEG_DARK)
        # Tip
        if 0 <= tx < width and 0 <= ty < height:
            canvas[ty, tx] = LEG_TIP

    # === 3. Human Upper Body ===
    # Rising from y=40
    waist_y = 40
    head_y = 18
    
    # Torso
    for y in range(head_y + 8, waist_y + 2):
        width_at_y = 4
        if y < head_y + 12: width_at_y = 5 # Chest
        elif y > waist_y - 4: width_at_y = 5 # Hips/Waist connection
        
        for x in range(center_x - width_at_y // 2, center_x + width_at_y // 2 + 1):
            if 0 <= x < width:
                canvas[y, x] = SKIN_BASE
                # Armor/Clothing (Corset style)
                if y > head_y + 12:
                    if x == center_x - width_at_y // 2 or x == center_x + width_at_y // 2:
                        canvas[y, x] = ARMOR_RED
                    if y % 3 == 0 and abs(x - center_x) < 2:
                        canvas[y, x] = ARMOR_TRIM # Laces/Gold

    # Head
    for y in range(head_y, head_y + 9):
        for x in range(center_x - 3, center_x + 4):
            # Oval head
            if (x-center_x)**2 + (y-(head_y+4))**2 <= 16:
                canvas[y, x] = SKIN_BASE
    
    # Face
    canvas[head_y + 4, center_x - 1] = EYE_GLOW # Left Eye
    canvas[head_y + 4, center_x + 1] = EYE_GLOW # Right Eye
    canvas[head_y + 7, center_x] = [100, 50, 50, 255] # Mouth

    # Hair
    for y in range(head_y - 2, head_y + 10):
        for x in range(center_x - 5, center_x + 6):
            if canvas[y, x][3] == 0: # If empty
                # Hair volume
                if (x-center_x)**2 + (y-(head_y+2))**2 <= 25:
                     canvas[y, x] = HAIR_DARK
    
    # Crown/Horns
    # Left Horn
    _draw_line(canvas, center_x - 2, head_y, center_x - 5, head_y - 6, HORN_BONE)
    # Right Horn
    _draw_line(canvas, center_x + 2, head_y, center_x + 5, head_y - 6, HORN_BONE)
    # Center Crown
    canvas[head_y-1, center_x] = ARMOR_RED
    canvas[head_y-2, center_x] = ARMOR_RED

    # Arms
    # Left Arm (raised slightly)
    _draw_line(canvas, center_x - 4, head_y + 10, center_x - 8, head_y + 14, SKIN_BASE) # Upper
    _draw_line(canvas, center_x - 8, head_y + 14, center_x - 10, head_y + 8, SKIN_BASE) # Lower (raised hand)
    # Hand glow
    canvas[head_y + 7, center_x - 10] = [255, 50, 50, 200] # Magic glow

    # Right Arm (down/holding something?)
    _draw_line(canvas, center_x + 4, head_y + 10, center_x + 8, head_y + 14, SKIN_BASE)
    _draw_line(canvas, center_x + 8, head_y + 14, center_x + 10, head_y + 18, SKIN_BASE)
    # Gauntlets
    canvas[head_y + 16, center_x + 9] = ARMOR_RED
    canvas[head_y + 17, center_x + 10] = ARMOR_RED

    return canvas

def create_spiderqueen_attack():
    """Create the attacking Spider Queen pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Reuse Palette
    SPIDER_BASE = [80, 20, 20, 255]
    SPIDER_MID = [120, 40, 40, 255]
    SPIDER_HIGHLIGHT = [160, 60, 60, 255]
    SPIDER_SHADOW = [40, 10, 10, 255]
    SPIDER_GLOW = [255, 100, 50, 255]
    
    LEG_DARK = [50, 20, 20, 255]
    LEG_MID = [100, 40, 40, 255]
    LEG_TIP = [30, 10, 10, 255]
    
    SKIN_BASE = [180, 200, 210, 255]
    ARMOR_RED = [140, 30, 30, 255]
    ARMOR_TRIM = [180, 140, 60, 255]
    HAIR_DARK = [20, 20, 30, 255]
    HORN_BONE = [200, 190, 180, 255]
    EYE_GLOW = [255, 50, 50, 255] # Red eyes for attack!
    
    center_x = 32
    
    # === 1. Spider Lower Body (Lunging forward) ===
    abdomen_center_x = 32
    abdomen_center_y = 42 # Slightly higher
    
    for y in range(32, 58):
        for x in range(15, 50):
            dx = x - abdomen_center_x
            dy = y - abdomen_center_y
            if (dx*dx)/(15*15) + (dy*dy)/(11*11) <= 1.0:
                color = SPIDER_BASE
                if dy > 3: color = SPIDER_SHADOW
                elif dy < -3: color = SPIDER_MID
                if (x % 6 == 0 and y % 5 == 0) and dy > 0:
                    color = SPIDER_GLOW
                canvas[y, x] = color

    # === 2. Spider Legs (Aggressive/Raised) ===
    leg_origins = [
        (24, 40), (22, 42), (20, 44), (18, 46),
        (40, 40), (42, 42), (44, 44), (46, 46)
    ]
    
    # Front legs raised high
    # Left
    _draw_line(canvas, leg_origins[0][0], leg_origins[0][1], leg_origins[0][0]-8, leg_origins[0][1]-10, LEG_MID) # Up
    _draw_line(canvas, leg_origins[0][0]-8, leg_origins[0][1]-10, leg_origins[0][0]-4, leg_origins[0][1]-15, LEG_TIP) # Tip
    
    # Right
    _draw_line(canvas, leg_origins[4][0], leg_origins[4][1], leg_origins[4][0]+8, leg_origins[4][1]-10, LEG_MID)
    _draw_line(canvas, leg_origins[4][0]+8, leg_origins[4][1]-10, leg_origins[4][0]+4, leg_origins[4][1]-15, LEG_TIP)

    # Other legs planted
    for i in range(1, 4):
        # Left
        ox, oy = leg_origins[i]
        _draw_line(canvas, ox, oy, ox-6, oy+5, LEG_MID)
        _draw_line(canvas, ox-6, oy+5, ox-10, oy+10, LEG_DARK)
        # Right
        ox, oy = leg_origins[i+4]
        _draw_line(canvas, ox, oy, ox+6, oy+5, LEG_MID)
        _draw_line(canvas, ox+6, oy+5, ox+10, oy+10, LEG_DARK)

    # === 3. Human Upper Body (Casting/Attacking) ===
    waist_y = 38
    head_y = 16
    
    # Torso
    for y in range(head_y + 8, waist_y + 2):
        width_at_y = 4
        if y < head_y + 12: width_at_y = 5
        for x in range(center_x - width_at_y // 2, center_x + width_at_y // 2 + 1):
            if 0 <= x < width:
                canvas[y, x] = SKIN_BASE
                if y > head_y + 12:
                    if x == center_x - width_at_y // 2 or x == center_x + width_at_y // 2:
                        canvas[y, x] = ARMOR_RED

    # Head
    for y in range(head_y, head_y + 9):
        for x in range(center_x - 3, center_x + 4):
            if (x-center_x)**2 + (y-(head_y+4))**2 <= 16:
                canvas[y, x] = SKIN_BASE
    
    # Angry Face
    canvas[head_y + 4, center_x - 1] = EYE_GLOW
    canvas[head_y + 4, center_x + 1] = EYE_GLOW
    canvas[head_y + 7, center_x] = [50, 0, 0, 255] # Open mouth

    # Hair (Wilder)
    for y in range(head_y - 4, head_y + 10):
        for x in range(center_x - 6, center_x + 7):
            if canvas[y, x][3] == 0:
                if (x-center_x)**2 + (y-(head_y+2))**2 <= 30:
                     if random.random() > 0.3: canvas[y, x] = HAIR_DARK

    # Horns
    _draw_line(canvas, center_x - 2, head_y, center_x - 6, head_y - 8, HORN_BONE)
    _draw_line(canvas, center_x + 2, head_y, center_x + 6, head_y - 8, HORN_BONE)

    # Arms (Both raised casting magic)
    # Left
    _draw_line(canvas, center_x - 4, head_y + 10, center_x - 10, head_y + 8, SKIN_BASE)
    _draw_line(canvas, center_x - 10, head_y + 8, center_x - 14, head_y + 2, SKIN_BASE)
    
    # Right
    _draw_line(canvas, center_x + 4, head_y + 10, center_x + 10, head_y + 8, SKIN_BASE)
    _draw_line(canvas, center_x + 10, head_y + 8, center_x + 14, head_y + 2, SKIN_BASE)

    # Magic Effects
    # Red magic orb above hands
    for r in range(6):
        for angle in range(0, 360, 30):
            rad = angle * 3.14159 / 180
            mx = int(center_x + r * np.cos(rad))
            my = int(head_y - 5 + r * np.sin(rad))
            if 0 <= mx < width and 0 <= my < height:
                if random.random() > 0.5:
                    canvas[my, mx] = [255, 50, 50, 200]

    return canvas

def _draw_line(canvas, x0, y0, x1, y1, color):
    """Bresenham's Line Algorithm"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < canvas.shape[1] and 0 <= y0 < canvas.shape[0]:
            canvas[y0, x0] = color
        
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def main():
    print("Creating Spider Queen monster images...")
    
    spider_default = create_spiderqueen_default()
    spider_attack = create_spiderqueen_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(spider_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/spider_queen.png')
    print(f"✓ Saved: art/spider_queen.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(spider_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/spider_queen_attack.png')
    print(f"✓ Saved: art/spider_queen_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Spider Queen creation complete!")

if __name__ == '__main__':
    main()
