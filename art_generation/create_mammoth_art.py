#!/usr/bin/env python3
"""
Mammoth Monster Art Generator - Creates pixel art for the mammoth monster
Inspired by woolly mammoth with long tusks and shaggy fur
Creates both regular and attack versions of the mammoth
"""

import numpy as np
from PIL import Image
import os

def create_mammoth_art():
    """Create regular mammoth pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for mammoth (woolly mammoth colors)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    FUR_BROWN = [120, 80, 50, 255]        # Brown shaggy fur
    FUR_DARK = [80, 50, 30, 255]          # Dark brown shading
    FUR_LIGHT = [160, 110, 70, 255]       # Light brown highlights
    TUSK_WHITE = [255, 250, 240, 255]     # Ivory tusks
    TUSK_SHADOW = [230, 220, 200, 255]    # Tusk shading
    SKIN_GRAY = [100, 100, 100, 255]      # Visible skin (trunk, ears)
    SKIN_DARK = [60, 60, 60, 255]         # Dark skin shading
    
    # Body (large round body) - positioned center-left
    body_center_x, body_center_y = 14, 18
    
    # Draw large round body
    for y in range(11, 26):
        for x in range(6, 22):
            # Elliptical body shape
            if ((x - body_center_x) ** 2) / 36 + ((y - body_center_y) ** 2) / 36 <= 1:
                canvas[y, x] = FUR_BROWN
    
    # Head (smaller, positioned on upper left of body)
    head_x, head_y = 10, 13
    for y in range(8, 17):
        for x in range(5, 15):
            # Rounded head
            if ((x - head_x) ** 2) / 16 + ((y - head_y) ** 2) / 16 <= 1:
                canvas[y, x] = FUR_BROWN
    
    # Trunk (long curved trunk extending down from head)
    trunk_segments = [
        (9, 16), (9, 17), (8, 18), (8, 19), (7, 20), (7, 21), (8, 22), (9, 23)
    ]
    for tx, ty in trunk_segments:
        # Make trunk thicker (3 pixels wide)
        for dx in range(-1, 2):
            if 0 <= tx + dx < size and 0 <= ty < size:
                canvas[ty, tx + dx] = SKIN_GRAY
    
    # Trunk tip (slightly wider at end)
    canvas[23, 8] = SKIN_GRAY
    canvas[23, 9] = SKIN_GRAY
    canvas[23, 10] = SKIN_GRAY
    canvas[24, 9] = SKIN_DARK
    
    # Large ears (flapping out from sides of head)
    # Left ear
    for y in range(10, 16):
        for x in range(2, 6):
            if ((x - 3) ** 2 + (y - 13) ** 2) <= 8:
                canvas[y, x] = FUR_DARK
    
    # Right ear  
    for y in range(10, 16):
        for x in range(13, 17):
            if ((x - 15) ** 2 + (y - 13) ** 2) <= 8:
                canvas[y, x] = FUR_DARK
    
    # Tusks (long curved ivory tusks)
    # Left tusk (curves outward and down)
    left_tusk_points = [
        (7, 15), (6, 16), (5, 17), (4, 18), (3, 19), (3, 20), (2, 21), (2, 22)
    ]
    for tx, ty in left_tusk_points:
        canvas[ty, tx] = TUSK_WHITE
        canvas[ty, tx + 1] = TUSK_WHITE
        # Add shading
        if ty > 17:
            canvas[ty, tx] = TUSK_SHADOW
    
    # Right tusk (curves outward and down)
    right_tusk_points = [
        (13, 15), (14, 16), (15, 17), (16, 18), (17, 19), (17, 20), (18, 21), (18, 22)
    ]
    for tx, ty in right_tusk_points:
        canvas[ty, tx] = TUSK_WHITE
        canvas[ty, tx - 1] = TUSK_WHITE
        # Add shading
        if ty > 17:
            canvas[ty, tx] = TUSK_SHADOW
    
    # Eyes (small black eyes on head)
    canvas[11, 7] = BLACK
    canvas[11, 13] = BLACK
    # Eye highlights
    canvas[10, 7] = WHITE
    canvas[10, 13] = WHITE
    
    # Legs (4 thick pillar-like legs)
    # Front left leg
    for y in range(24, 30):
        for x in range(8, 11):
            canvas[y, x] = FUR_DARK
    
    # Front right leg
    for y in range(24, 30):
        for x in range(14, 17):
            canvas[y, x] = FUR_DARK
    
    # Back left leg
    for y in range(23, 29):
        for x in range(11, 14):
            canvas[y, x] = FUR_DARK
    
    # Back right leg
    for y in range(23, 29):
        for x in range(17, 20):
            canvas[y, x] = FUR_DARK
    
    # Feet (darker at bottom)
    for x in range(8, 11):
        canvas[29, x] = BLACK
    for x in range(14, 17):
        canvas[29, x] = BLACK
    for x in range(11, 14):
        canvas[28, x] = BLACK
    for x in range(17, 20):
        canvas[28, x] = BLACK
    
    # Add shaggy fur texture (darker patches for fur effect)
    import random
    random.seed(42)
    for y in range(8, 26):
        for x in range(5, 22):
            if canvas[y, x][0] == FUR_BROWN[0] and canvas[y, x][3] > 0:
                if random.random() > 0.7:
                    canvas[y, x] = FUR_DARK
                elif random.random() > 0.85:
                    canvas[y, x] = FUR_LIGHT
    
    # Add fur strands hanging down (shaggy appearance)
    fur_strands = [
        (7, 19), (9, 20), (11, 21), (13, 22), (15, 21), (17, 20), (19, 19)
    ]
    for fx, fy in fur_strands:
        canvas[fy, fx] = FUR_DARK
        if fy + 1 < size:
            canvas[fy + 1, fx] = FUR_DARK
    
    # Tail (small stubby tail at back)
    canvas[20, 21] = FUR_DARK
    canvas[21, 21] = FUR_DARK
    canvas[21, 22] = FUR_DARK
    
    return canvas

def create_mammoth_attack():
    """Create mammoth attack animation - charging with raised trunk"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette (same as regular)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    FUR_BROWN = [120, 80, 50, 255]
    FUR_DARK = [80, 50, 30, 255]
    FUR_LIGHT = [160, 110, 70, 255]
    TUSK_WHITE = [255, 250, 240, 255]
    TUSK_SHADOW = [230, 220, 200, 255]
    SKIN_GRAY = [100, 100, 100, 255]
    SKIN_DARK = [60, 60, 60, 255]
    DUST_BROWN = [160, 130, 100, 255]     # Dust cloud effect
    
    # Body - leaning forward in charging stance
    body_center_x, body_center_y = 15, 19
    
    # Draw body (slightly tilted forward)
    for y in range(12, 27):
        for x in range(7, 23):
            if ((x - body_center_x) ** 2) / 36 + ((y - body_center_y) ** 2) / 36 <= 1:
                canvas[y, x] = FUR_BROWN
    
    # Head - lowered for charging
    head_x, head_y = 11, 14
    for y in range(9, 18):
        for x in range(6, 16):
            if ((x - head_x) ** 2) / 16 + ((y - head_y) ** 2) / 16 <= 1:
                canvas[y, x] = FUR_BROWN
    
    # Trunk - raised aggressively
    trunk_segments = [
        (10, 9), (9, 8), (9, 7), (8, 6), (8, 5), (9, 4), (10, 3)
    ]
    for tx, ty in trunk_segments:
        for dx in range(-1, 2):
            if 0 <= tx + dx < size and 0 <= ty < size:
                canvas[ty, tx + dx] = SKIN_GRAY
    
    # Trunk tip - curled
    canvas[3, 9] = SKIN_GRAY
    canvas[3, 10] = SKIN_GRAY
    canvas[3, 11] = SKIN_GRAY
    canvas[2, 10] = SKIN_DARK
    
    # Ears - flared out
    # Left ear (more visible)
    for y in range(11, 17):
        for x in range(2, 7):
            if ((x - 4) ** 2 + (y - 14) ** 2) <= 9:
                canvas[y, x] = FUR_DARK
    
    # Right ear
    for y in range(11, 17):
        for x in range(14, 18):
            if ((x - 16) ** 2 + (y - 14) ** 2) <= 7:
                canvas[y, x] = FUR_DARK
    
    # Tusks - pointing forward menacingly
    # Left tusk (more forward)
    left_tusk_points = [
        (7, 16), (6, 17), (5, 18), (4, 19), (3, 20), (3, 21), (2, 22), (1, 23)
    ]
    for tx, ty in left_tusk_points:
        canvas[ty, tx] = TUSK_WHITE
        canvas[ty, tx + 1] = TUSK_WHITE
        if ty > 18:
            canvas[ty, tx] = TUSK_SHADOW
    
    # Right tusk
    right_tusk_points = [
        (14, 16), (15, 17), (16, 18), (17, 19), (18, 20), (18, 21), (19, 22), (20, 23)
    ]
    for tx, ty in right_tusk_points:
        canvas[ty, tx] = TUSK_WHITE
        canvas[ty, tx - 1] = TUSK_WHITE
        if ty > 18:
            canvas[ty, tx] = TUSK_SHADOW
    
    # Eyes - wider/more aggressive
    canvas[12, 8] = BLACK
    canvas[12, 14] = BLACK
    canvas[11, 8] = WHITE
    canvas[11, 14] = WHITE
    
    # Legs - in running position (front legs forward, back legs back)
    # Front left leg (extended forward)
    for y in range(23, 30):
        for x in range(6, 9):
            canvas[y, x] = FUR_DARK
    
    # Front right leg
    for y in range(24, 30):
        for x in range(15, 18):
            canvas[y, x] = FUR_DARK
    
    # Back left leg (extended back)
    for y in range(22, 28):
        for x in range(12, 15):
            canvas[y, x] = FUR_DARK
    
    # Back right leg
    for y in range(22, 28):
        for x in range(19, 22):
            canvas[y, x] = FUR_DARK
    
    # Feet
    for x in range(6, 9):
        canvas[29, x] = BLACK
    for x in range(15, 18):
        canvas[29, x] = BLACK
    for x in range(12, 15):
        canvas[27, x] = BLACK
    for x in range(19, 22):
        canvas[27, x] = BLACK
    
    # Add shaggy fur texture
    import random
    random.seed(42)
    for y in range(9, 27):
        for x in range(6, 23):
            if canvas[y, x][0] == FUR_BROWN[0] and canvas[y, x][3] > 0:
                if random.random() > 0.7:
                    canvas[y, x] = FUR_DARK
                elif random.random() > 0.85:
                    canvas[y, x] = FUR_LIGHT
    
    # Add dust clouds at feet (charging effect)
    dust_positions = [
        (5, 29), (4, 28), (8, 29), (9, 28),
        (23, 29), (24, 28), (25, 29)
    ]
    for dx, dy in dust_positions:
        if 0 <= dx < size and 0 <= dy < size:
            canvas[dy, dx] = DUST_BROWN
            canvas[dy, dx][3] = 180  # Semi-transparent
    
    # Tail raised
    canvas[21, 22] = FUR_DARK
    canvas[20, 23] = FUR_DARK
    canvas[19, 24] = FUR_DARK
    
    return canvas

def main():
    """Generate mammoth monster art files"""
    print("Creating Mammoth Monster Art...")
    
    # Create output directory if it doesn't exist
    output_dir = "art"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate regular mammoth
    print("  - Creating regular mammoth...")
    mammoth_canvas = create_mammoth_art()
    mammoth_img = Image.fromarray(mammoth_canvas, 'RGBA')
    
    # Scale up 8x for better visibility (32 -> 256)
    mammoth_scaled = mammoth_img.resize((256, 256), Image.NEAREST)
    mammoth_scaled.save(os.path.join(output_dir, "mammoth_monster.png"))
    print(f"    ✓ Saved {output_dir}/mammoth_monster.png")
    
    # Generate attack mammoth
    print("  - Creating mammoth attack animation...")
    attack_canvas = create_mammoth_attack()
    attack_img = Image.fromarray(attack_canvas, 'RGBA')
    
    # Scale up 8x
    attack_scaled = attack_img.resize((256, 256), Image.NEAREST)
    attack_scaled.save(os.path.join(output_dir, "mammoth_monster_attack.png"))
    print(f"    ✓ Saved {output_dir}/mammoth_monster_attack.png")
    
    print("\n✅ Mammoth Monster Art Generation Complete!")
    print(f"   Regular: {output_dir}/mammoth_monster.png (256x256)")
    print(f"   Attack:  {output_dir}/mammoth_monster_attack.png (256x256)")

if __name__ == "__main__":
    main()
