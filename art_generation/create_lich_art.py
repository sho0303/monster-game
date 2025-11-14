#!/usr/bin/env python3
"""
Lich Monster Art Generator - Creates pixel art for the undead lich sorcerer
Inspired by skeletal undead spellcasters with flowing robes and dark magic
Creates both regular and attack versions of the lich
Base resolution: 64x64, scaled to 256x256 (4x)
"""

import numpy as np
from PIL import Image
import os

def create_lich_art():
    """Create regular lich pixel art at 64x64 resolution"""
    # Create a 64x64 canvas
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for lich (undead necromancer)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    
    # Skull colors
    SKULL_WHITE = [240, 240, 230, 255]
    SKULL_LIGHT = [255, 255, 245, 255]
    SKULL_SHADOW = [180, 180, 170, 255]
    SKULL_DARK = [120, 120, 110, 255]
    
    # Eye colors (glowing green/red)
    EYE_GREEN = [0, 255, 100, 255]
    EYE_GLOW = [150, 255, 150, 255]
    EYE_DARK = [0, 150, 50, 255]
    
    # Robe colors (dark tattered robes)
    ROBE_DARK = [40, 50, 45, 255]
    ROBE_MID = [60, 70, 65, 255]
    ROBE_LIGHT = [80, 90, 85, 255]
    ROBE_SHADOW = [20, 25, 23, 255]
    
    # Magic/energy colors
    MAGIC_GREEN = [50, 255, 100, 255]
    MAGIC_LIGHT = [100, 255, 150, 255]
    MAGIC_DARK = [20, 180, 60, 255]
    
    # Bone/skeletal colors
    BONE_WHITE = [230, 230, 220, 255]
    BONE_SHADOW = [160, 160, 150, 255]
    
    # Mist/ethereal colors
    MIST_GRAY = [100, 120, 110, 150]
    MIST_LIGHT = [150, 170, 160, 100]
    
    # Draw flowing robes (main body) - ghostly and tattered
    # Upper robe body
    for y in range(20, 55):
        for x in range(18, 46):
            # Bell-shaped robe
            width_at_y = int(10 + (y - 20) * 0.4)
            center_x = 32
            if abs(x - center_x) <= width_at_y:
                # Base robe color
                canvas[y, x] = ROBE_DARK
                # Add shading
                if x >= center_x + width_at_y - 3:
                    canvas[y, x] = ROBE_SHADOW
                elif x >= center_x + 2:
                    canvas[y, x] = ROBE_MID
                elif x <= center_x - width_at_y + 3:
                    canvas[y, x] = ROBE_SHADOW
                # Add highlights
                if x >= center_x - 2 and x <= center_x + 2 and y < 40:
                    canvas[y, x] = ROBE_LIGHT
    
    # Add tattered edges to robes
    tatter_points = [
        (54, 20), (54, 21), (54, 44), (54, 43),
        (52, 18), (52, 46), (50, 17), (50, 47),
        (48, 19), (48, 45), (46, 21), (46, 43)
    ]
    for y, x in tatter_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = ROBE_SHADOW
    
    # Draw skeletal hands/arms emerging from robes
    # Left hand (raised, casting)
    left_hand_points = [
        # Wrist/forearm
        (25, 20), (25, 21), (26, 20), (26, 21),
        (27, 19), (27, 20), (28, 19), (28, 20),
        # Palm
        (23, 21), (23, 22), (23, 23),
        (24, 21), (24, 22), (24, 23), (24, 24),
        (25, 22), (25, 23), (25, 24),
    ]
    for y, x in left_hand_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
            # Add shadows
            if x >= 23 or y >= 26:
                canvas[y, x] = BONE_SHADOW
    
    # Left hand fingers
    left_fingers = [
        (21, 22), (20, 22), (19, 23),  # Index finger
        (22, 24), (21, 24), (20, 25),  # Middle finger
        (22, 25), (21, 26), (20, 27),  # Ring finger
    ]
    for y, x in left_fingers:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
    
    # Right hand (holding staff/lower)
    right_hand_points = [
        # Wrist/forearm
        (32, 42), (32, 43), (33, 42), (33, 43),
        (34, 41), (34, 42), (35, 41), (35, 42),
        # Palm
        (30, 43), (30, 44), (30, 45),
        (31, 43), (31, 44), (31, 45), (31, 46),
        (32, 44), (32, 45), (32, 46),
    ]
    for y, x in right_hand_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
            if x >= 42 or y >= 34:
                canvas[y, x] = BONE_SHADOW
    
    # Draw skull head (large and detailed)
    skull_center_x, skull_center_y = 32, 12
    
    # Main skull shape (oval)
    for y in range(6, 20):
        for x in range(24, 40):
            distance = ((x - skull_center_x) ** 2 / 64 + (y - skull_center_y) ** 2 / 49)
            if distance <= 1:
                canvas[y, x] = SKULL_WHITE
                # Add shading to skull
                if x >= skull_center_x + 4 or y >= skull_center_y + 4:
                    canvas[y, x] = SKULL_SHADOW
                elif x >= skull_center_x + 2 or y >= skull_center_y + 2:
                    canvas[y, x] = SKULL_WHITE
                # Highlights
                if x <= skull_center_x - 2 and y <= skull_center_y - 1:
                    canvas[y, x] = SKULL_LIGHT
    
    # Eye sockets (large, glowing green)
    # Left eye socket
    for y in range(10, 15):
        for x in range(27, 31):
            eye_dist = ((x - 28.5) ** 2 + (y - 12) ** 2)
            if eye_dist <= 6:
                canvas[y, x] = BLACK
                # Glowing green eyes
                if eye_dist <= 3:
                    canvas[y, x] = EYE_GREEN
                if eye_dist <= 1.5:
                    canvas[y, x] = EYE_GLOW
    
    # Right eye socket
    for y in range(10, 15):
        for x in range(33, 37):
            eye_dist = ((x - 34.5) ** 2 + (y - 12) ** 2)
            if eye_dist <= 6:
                canvas[y, x] = BLACK
                if eye_dist <= 3:
                    canvas[y, x] = EYE_GREEN
                if eye_dist <= 1.5:
                    canvas[y, x] = EYE_GLOW
    
    # Nasal cavity (triangular)
    nose_points = [
        (15, 31), (15, 32),
        (16, 31), (16, 32), (16, 33),
        (17, 31), (17, 32), (17, 33),
    ]
    for y, x in nose_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BLACK
    
    # Jaw and teeth (menacing grin)
    # Upper jaw line
    for x in range(27, 37):
        canvas[17, x] = SKULL_SHADOW
    
    # Teeth (detailed)
    teeth_top = [
        (18, 28), (18, 29),  # Tooth 1
        (18, 30), (18, 31),  # Tooth 2
        (18, 32), (18, 33),  # Tooth 3
        (18, 34), (18, 35),  # Tooth 4
    ]
    for y, x in teeth_top:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SKULL_LIGHT
            canvas[y+1, x] = SKULL_WHITE
    
    # Tooth gaps (black)
    tooth_gaps = [(19, 29), (19, 31), (19, 33), (19, 35)]
    for y, x in tooth_gaps:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BLACK
    
    # Add cracks to skull for age/decay
    crack_points = [
        (8, 35), (9, 35), (10, 36), (11, 36),  # Right forehead crack
        (7, 28), (8, 28), (9, 27),              # Left forehead crack
        (14, 26), (15, 26), (16, 25),           # Left cheek crack
    ]
    for y, x in crack_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SKULL_DARK
    
    # Draw magical aura/energy around left hand
    aura_points = [
        (22, 20), (23, 19), (24, 18), (21, 21),
        (20, 21), (21, 19), (22, 18), (23, 17),
        (24, 19), (25, 18), (26, 17), (25, 20),
        (19, 22), (20, 24), (21, 25), (22, 26),
    ]
    for y, x in aura_points:
        if 0 <= x < size and 0 <= y < size:
            if canvas[y, x][3] == 0:  # Only on empty space
                canvas[y, x] = MAGIC_DARK
    
    # Floating magical orbs around lich
    orb_centers = [(10, 16), (14, 48), (8, 50)]
    for orb_y, orb_x in orb_centers:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dy*dy + dx*dx <= 4:
                    ny, nx = orb_y + dy, orb_x + dx
                    if 0 <= nx < size and 0 <= ny < size:
                        if dy*dy + dx*dx <= 1:
                            canvas[ny, nx] = MAGIC_LIGHT
                        else:
                            canvas[ny, nx] = MAGIC_GREEN
    
    # Ethereal mist at bottom of robes
    for y in range(52, 60):
        for x in range(15, 49):
            if (x + y) % 3 == 0 and canvas[y, x][3] == 0:
                canvas[y, x] = MIST_GRAY
            elif (x + y) % 5 == 0 and canvas[y, x][3] == 0:
                canvas[y, x] = MIST_LIGHT
    
    return canvas

def create_lich_attack_art():
    """Create attack version of lich pixel art at 64x64 resolution"""
    # Create a 64x64 canvas
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Enhanced color palette for attack mode
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    
    # Skull colors (more intense)
    SKULL_WHITE = [240, 240, 230, 255]
    SKULL_LIGHT = [255, 255, 245, 255]
    SKULL_SHADOW = [180, 180, 170, 255]
    SKULL_DARK = [120, 120, 110, 255]
    
    # Eye colors (brighter, more menacing)
    EYE_RED = [255, 0, 0, 255]
    EYE_GLOW = [255, 100, 100, 255]
    EYE_DARK = [180, 0, 0, 255]
    
    # Robe colors
    ROBE_DARK = [40, 50, 45, 255]
    ROBE_MID = [60, 70, 65, 255]
    ROBE_LIGHT = [80, 90, 85, 255]
    ROBE_SHADOW = [20, 25, 23, 255]
    
    # Attack magic colors (intense green energy)
    MAGIC_BRIGHT = [100, 255, 150, 255]
    MAGIC_CORE = [200, 255, 200, 255]
    MAGIC_INTENSE = [50, 255, 100, 255]
    MAGIC_DARK = [20, 200, 60, 255]
    
    # Lightning/energy
    LIGHTNING = [255, 255, 255, 255]
    LIGHTNING_GREEN = [150, 255, 180, 255]
    
    # Bone colors
    BONE_WHITE = [230, 230, 220, 255]
    BONE_SHADOW = [160, 160, 150, 255]
    
    # Vortex/dark magic
    VORTEX_PURPLE = [80, 0, 100, 255]
    VORTEX_DARK = [40, 0, 50, 255]
    
    # Draw robes (more billowing, showing power)
    for y in range(18, 58):
        for x in range(16, 48):
            width_at_y = int(12 + (y - 18) * 0.45)
            center_x = 32
            if abs(x - center_x) <= width_at_y:
                canvas[y, x] = ROBE_DARK
                if x >= center_x + width_at_y - 4:
                    canvas[y, x] = ROBE_SHADOW
                elif x >= center_x + 3:
                    canvas[y, x] = ROBE_MID
                elif x <= center_x - width_at_y + 4:
                    canvas[y, x] = ROBE_SHADOW
                if x >= center_x - 3 and x <= center_x + 3 and y < 35:
                    canvas[y, x] = ROBE_LIGHT
    
    # Enhanced tattered edges
    tatter_points = [
        (57, 18), (57, 19), (57, 45), (57, 46),
        (55, 16), (55, 48), (53, 15), (53, 49),
        (51, 17), (51, 47), (49, 19), (49, 45),
        (56, 20), (56, 44), (54, 18), (54, 46)
    ]
    for y, x in tatter_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = ROBE_SHADOW
    
    # Both hands raised for casting
    # Left hand (raised high, channeling)
    left_hand = [
        (20, 18), (20, 19), (21, 18), (21, 19),
        (22, 17), (22, 18), (23, 17), (23, 18),
        (18, 19), (18, 20), (18, 21),
        (19, 19), (19, 20), (19, 21), (19, 22),
        (20, 20), (20, 21), (20, 22),
    ]
    for y, x in left_hand:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
            if x >= 19 or y >= 22:
                canvas[y, x] = BONE_SHADOW
    
    # Left fingers (spread wide)
    left_fingers = [
        (16, 19), (15, 19), (14, 20),  # Finger 1
        (17, 21), (16, 22), (15, 23),  # Finger 2
        (17, 23), (16, 24), (15, 25),  # Finger 3
        (18, 24), (17, 25), (16, 26),  # Finger 4
    ]
    for y, x in left_fingers:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
    
    # Right hand (raised, casting)
    right_hand = [
        (20, 44), (20, 45), (21, 44), (21, 45),
        (22, 45), (22, 46), (23, 45), (23, 46),
        (18, 45), (18, 46), (18, 47),
        (19, 44), (19, 45), (19, 46), (19, 47),
        (20, 45), (20, 46), (20, 47),
    ]
    for y, x in right_hand:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
            if x <= 44 or y >= 22:
                canvas[y, x] = BONE_SHADOW
    
    # Right fingers
    right_fingers = [
        (16, 47), (15, 47), (14, 46),  # Finger 1
        (17, 46), (16, 45), (15, 44),  # Finger 2
        (17, 48), (16, 49), (15, 50),  # Finger 3
        (18, 48), (17, 49), (16, 50),  # Finger 4
    ]
    for y, x in right_fingers:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BONE_WHITE
    
    # Skull head (tilted back slightly in casting pose)
    skull_center_x, skull_center_y = 32, 10
    
    for y in range(4, 18):
        for x in range(24, 40):
            distance = ((x - skull_center_x) ** 2 / 64 + (y - skull_center_y) ** 2 / 49)
            if distance <= 1:
                canvas[y, x] = SKULL_WHITE
                if x >= skull_center_x + 4 or y >= skull_center_y + 5:
                    canvas[y, x] = SKULL_SHADOW
                elif x >= skull_center_x + 2 or y >= skull_center_y + 3:
                    canvas[y, x] = SKULL_WHITE
                if x <= skull_center_x - 2 and y <= skull_center_y - 1:
                    canvas[y, x] = SKULL_LIGHT
    
    # Eyes (glowing red with rage)
    # Left eye
    for y in range(8, 13):
        for x in range(27, 31):
            eye_dist = ((x - 28.5) ** 2 + (y - 10) ** 2)
            if eye_dist <= 6:
                canvas[y, x] = BLACK
                if eye_dist <= 3.5:
                    canvas[y, x] = EYE_RED
                if eye_dist <= 1.5:
                    canvas[y, x] = EYE_GLOW
    
    # Right eye
    for y in range(8, 13):
        for x in range(33, 37):
            eye_dist = ((x - 34.5) ** 2 + (y - 10) ** 2)
            if eye_dist <= 6:
                canvas[y, x] = BLACK
                if eye_dist <= 3.5:
                    canvas[y, x] = EYE_RED
                if eye_dist <= 1.5:
                    canvas[y, x] = EYE_GLOW
    
    # Nasal cavity
    nose_points = [
        (13, 31), (13, 32),
        (14, 31), (14, 32), (14, 33),
        (15, 31), (15, 32), (15, 33),
    ]
    for y, x in nose_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BLACK
    
    # Jaw and teeth (opened wide in spell casting)
    for x in range(27, 37):
        canvas[15, x] = SKULL_SHADOW
    
    teeth_top = [
        (16, 28), (16, 29),
        (16, 30), (16, 31),
        (16, 32), (16, 33),
        (16, 34), (16, 35),
    ]
    for y, x in teeth_top:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SKULL_LIGHT
            canvas[y+1, x] = SKULL_WHITE
    
    # Mouth opened wider for spell
    for x in range(28, 36):
        for y in range(17, 20):
            if y == 17 or y == 19:
                canvas[y, x] = SKULL_WHITE
            else:
                canvas[y, x] = BLACK
    
    # Skull cracks
    crack_points = [
        (6, 35), (7, 35), (8, 36), (9, 36),
        (5, 28), (6, 28), (7, 27),
        (12, 26), (13, 26), (14, 25),
    ]
    for y, x in crack_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SKULL_DARK
    
    # Massive magical energy sphere between hands
    spell_center_y, spell_center_x = 18, 32
    for y in range(10, 27):
        for x in range(24, 40):
            dist = ((x - spell_center_x) ** 2 + (y - spell_center_y) ** 2)
            if dist <= 49:  # Large energy sphere
                if dist <= 16:
                    canvas[y, x] = MAGIC_CORE
                elif dist <= 25:
                    canvas[y, x] = MAGIC_BRIGHT
                elif dist <= 36:
                    canvas[y, x] = MAGIC_INTENSE
                else:
                    canvas[y, x] = MAGIC_DARK
    
    # Lightning bolts emanating from spell
    lightning_strikes = [
        # Left side
        [(18, 24), (17, 22), (16, 20), (15, 18), (14, 16)],
        [(20, 24), (19, 22), (18, 20), (17, 18), (16, 16)],
        # Right side
        [(18, 40), (17, 42), (16, 44), (15, 46), (14, 48)],
        [(20, 40), (19, 42), (18, 44), (17, 46), (16, 48)],
        # Top
        [(10, 32), (8, 32), (6, 31), (4, 30), (2, 29)],
        [(12, 30), (10, 28), (8, 26), (6, 24), (4, 22)],
        [(12, 34), (10, 36), (8, 38), (6, 40), (4, 42)],
    ]
    
    for strike in lightning_strikes:
        for i, (y, x) in enumerate(strike):
            if 0 <= x < size and 0 <= y < size:
                if i % 2 == 0:
                    canvas[y, x] = LIGHTNING
                else:
                    canvas[y, x] = LIGHTNING_GREEN
                # Add branch
                if i > 0 and i < len(strike) - 1:
                    if x + 1 < size:
                        canvas[y, x+1] = LIGHTNING_GREEN
    
    # Dark vortex at bottom (power emanating)
    for y in range(50, 62):
        for x in range(20, 44):
            if (x + y) % 3 == 0:
                canvas[y, x] = VORTEX_DARK
            elif (x + y) % 4 == 0:
                canvas[y, x] = VORTEX_PURPLE
    
    # Floating runes/symbols around lich (mystical)
    rune_positions = [(8, 12), (10, 52), (25, 50), (25, 14)]
    for ry, rx in rune_positions:
        # Simple cross-like rune
        if 0 <= rx < size and 0 <= ry < size:
            canvas[ry, rx] = MAGIC_BRIGHT
            if rx + 1 < size:
                canvas[ry, rx+1] = MAGIC_INTENSE
            if rx - 1 >= 0:
                canvas[ry, rx-1] = MAGIC_INTENSE
            if ry + 1 < size:
                canvas[ry+1, rx] = MAGIC_INTENSE
            if ry - 1 >= 0:
                canvas[ry-1, rx] = MAGIC_INTENSE
    
    return canvas

def save_lich_art():
    """Generate and save both versions of lich art"""
    # Create art directory if it doesn't exist
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate both versions
    lich_canvas = create_lich_art()
    lich_attack_canvas = create_lich_attack_art()
    
    lich_img = Image.fromarray(lich_canvas, 'RGBA')
    lich_attack_img = Image.fromarray(lich_attack_canvas, 'RGBA')
    
    # Scale up to 256x256 (4x scale: 64x64 -> 256x256)
    scale_factor = 4
    final_size = (64 * scale_factor, 64 * scale_factor)
    
    # Resize using nearest neighbor to maintain pixel art look
    lich_img = lich_img.resize(final_size, Image.Resampling.NEAREST)
    lich_attack_img = lich_attack_img.resize(final_size, Image.Resampling.NEAREST)
    
    # Save the images
    lich_path = os.path.join(art_dir, "lich_monster.png")
    lich_attack_path = os.path.join(art_dir, "lich_monster_attack.png")
    
    lich_img.save(lich_path)
    lich_attack_img.save(lich_attack_path)
    
    print(f"✅ Regular lich art saved to: {lich_path}")
    print(f"✅ Attack lich art saved to: {lich_attack_path}")
    print(f"📐 Base resolution: 64x64, Final size: 256x256 (4x scale)")
    print(f"🎨 Style: Pixel art undead necromancer with skull face, flowing robes, and dark magic")
    
    return lich_img, lich_attack_img

if __name__ == "__main__":
    save_lich_art()
