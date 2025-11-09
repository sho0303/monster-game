#!/usr/bin/env python3
"""
Kraken Monster Art Generator - Creates pixel art for the legendary kraken sea monster
Inspired by massive octopus-like creatures with tentacles and ancient power
Creates both regular and attack versions of the kraken
"""

import numpy as np
from PIL import Image
import os

def create_kraken_art():
    """Create regular kraken pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for kraken (deep sea monster)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    BODY_DARK = [40, 20, 60, 255]         # Dark purple main body
    BODY_SHADOW = [20, 10, 30, 255]      # Darker body shading
    TENTACLE_PURPLE = [60, 30, 80, 255]   # Purple tentacles
    TENTACLE_DARK = [35, 15, 45, 255]    # Dark tentacle shading
    SUCKER_PINK = [200, 120, 140, 255]   # Pink sucker cups
    SUCKER_DARK = [150, 80, 100, 255]    # Dark sucker shading
    EYE_RED = [200, 50, 50, 255]         # Menacing red eyes
    EYE_GLOW = [255, 100, 100, 255]      # Eye glow
    BEAK_YELLOW = [220, 200, 120, 255]   # Yellowish beak
    BEAK_DARK = [180, 160, 80, 255]      # Beak shading
    WATER_BLUE = [0, 80, 120, 255]       # Deep water
    WATER_FOAM = [180, 220, 240, 255]    # Water foam
    BARNACLE = [160, 140, 120, 255]      # Ancient barnacles
    
    # Main body (bulbous head/mantle)
    for y in range(6, 20):
        for x in range(10, 22):
            # Create oval shape for the mantle
            center_x, center_y = 16, 13
            if ((x - center_x) ** 2 / 36 + (y - center_y) ** 2 / 49) <= 1:
                canvas[y, x] = BODY_DARK
                # Add shading for 3D effect
                if x >= center_x + 2 or y >= center_y + 3:
                    canvas[y, x] = BODY_SHADOW
    
    # Eyes (large and menacing)
    # Left eye
    for y in range(9, 13):
        for x in range(12, 15):
            if ((x - 13) ** 2 + (y - 11) ** 2) <= 4:
                canvas[y, x] = EYE_RED
                # Eye highlight
                if x == 13 and y == 10:
                    canvas[y, x] = EYE_GLOW
                # Pupil
                if x == 13 and y == 11:
                    canvas[y, x] = BLACK
    
    # Right eye
    for y in range(9, 13):
        for x in range(17, 20):
            if ((x - 18) ** 2 + (y - 11) ** 2) <= 4:
                canvas[y, x] = EYE_RED
                # Eye highlight
                if x == 18 and y == 10:
                    canvas[y, x] = EYE_GLOW
                # Pupil
                if x == 18 and y == 11:
                    canvas[y, x] = BLACK
    
    # Beak/mouth (sharp and dangerous)
    beak_points = [(15, 15), (15, 16), (16, 15), (16, 16), (17, 15), (17, 16)]
    for y, x in beak_points:
        canvas[y, x] = BEAK_YELLOW
        # Add shading
        if x >= 16:
            canvas[y, x] = BEAK_DARK
    
    # Tentacles (8 tentacles spreading outward)
    # Tentacle 1 (top-left)
    tentacle_1_points = [(18, 8), (19, 7), (20, 6), (21, 5), (22, 4), (23, 3)]
    for y, x in tentacle_1_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            canvas[y, x + 1] = TENTACLE_DARK if x + 1 < size else TENTACLE_PURPLE
            # Add suckers
            if (y + x) % 3 == 0:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 2 (top-right)
    tentacle_2_points = [(18, 24), (19, 25), (20, 26), (21, 27), (22, 28), (23, 29)]
    for y, x in tentacle_2_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            if x - 1 >= 0:
                canvas[y, x - 1] = TENTACLE_DARK
            # Add suckers
            if (y + x) % 3 == 0:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 3 (left side)
    tentacle_3_points = [(16, 6), (17, 5), (18, 4), (19, 3), (20, 2), (21, 1)]
    for y, x in tentacle_3_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            canvas[y + 1, x] = TENTACLE_DARK if y + 1 < size else TENTACLE_PURPLE
            # Add suckers
            if (y + x) % 3 == 1:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 4 (right side)
    tentacle_4_points = [(16, 26), (17, 27), (18, 28), (19, 29), (20, 30), (21, 31)]
    for y, x in tentacle_4_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            if y + 1 < size:
                canvas[y + 1, x] = TENTACLE_DARK
            # Add suckers
            if (y + x) % 3 == 1:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 5 (bottom-left)
    tentacle_5_points = [(20, 10), (21, 9), (22, 8), (23, 7), (24, 6), (25, 5), (26, 4)]
    for y, x in tentacle_5_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            canvas[y, x + 1] = TENTACLE_DARK if x + 1 < size else TENTACLE_PURPLE
            # Add suckers
            if (y + x) % 3 == 2:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 6 (bottom-right)
    tentacle_6_points = [(20, 22), (21, 23), (22, 24), (23, 25), (24, 26), (25, 27), (26, 28)]
    for y, x in tentacle_6_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            if x - 1 >= 0:
                canvas[y, x - 1] = TENTACLE_DARK
            # Add suckers
            if (y + x) % 3 == 2:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 7 (bottom center-left)
    tentacle_7_points = [(20, 14), (22, 13), (24, 12), (26, 11), (28, 10), (30, 9), (31, 8)]
    for y, x in tentacle_7_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            canvas[y, x + 1] = TENTACLE_DARK if x + 1 < size else TENTACLE_PURPLE
            # Add suckers
            if y % 2 == 0:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 8 (bottom center-right)
    tentacle_8_points = [(20, 18), (22, 19), (24, 20), (26, 21), (28, 22), (30, 23), (31, 24)]
    for y, x in tentacle_8_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            if x - 1 >= 0:
                canvas[y, x - 1] = TENTACLE_DARK
            # Add suckers
            if y % 2 == 0:
                canvas[y, x] = SUCKER_PINK
    
    # Ancient barnacles on the body (showing age and power)
    barnacle_points = [(10, 14), (12, 18), (14, 12), (16, 19), (18, 13)]
    for y, x in barnacle_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = BARNACLE
    
    # Water effects around the creature
    water_points = [
        (5, 8), (5, 24), (4, 12), (4, 20),
        (27, 6), (27, 26), (28, 4), (28, 28),
        (29, 2), (29, 30), (30, 0), (30, 31)
    ]
    for y, x in water_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_FOAM
    
    return Image.fromarray(canvas)

def create_kraken_attack_art():
    """Create attack version of kraken pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Enhanced color palette for attack mode
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    BODY_DARK = [40, 20, 60, 255]
    BODY_SHADOW = [20, 10, 30, 255]
    TENTACLE_PURPLE = [80, 40, 100, 255]    # Darker, more aggressive
    TENTACLE_DARK = [45, 20, 55, 255]
    SUCKER_PINK = [220, 140, 160, 255]     # Brighter, more visible
    SUCKER_DARK = [170, 100, 120, 255]
    EYE_RED = [255, 0, 0, 255]             # Brighter, more menacing
    EYE_GLOW = [255, 150, 150, 255]        # Glowing with rage
    BEAK_YELLOW = [240, 220, 140, 255]
    BEAK_DARK = [200, 180, 100, 255]
    WHIRLPOOL = [0, 60, 100, 255]          # Dark swirling water
    FOAM_VIOLENT = [255, 255, 255, 255]    # Violent white foam
    LIGHTNING = [255, 255, 200, 255]       # Electric effects
    VENOM = [100, 255, 100, 255]           # Toxic green
    
    # Main body (more aggressive posture)
    for y in range(5, 19):
        for x in range(9, 23):
            center_x, center_y = 16, 12
            if ((x - center_x) ** 2 / 49 + (y - center_y) ** 2 / 64) <= 1:
                canvas[y, x] = BODY_DARK
                if x >= center_x + 3 or y >= center_y + 4:
                    canvas[y, x] = BODY_SHADOW
    
    # Eyes (glowing with fury)
    # Left eye (larger, more menacing)
    for y in range(8, 14):
        for x in range(11, 16):
            if ((x - 13) ** 2 + (y - 11) ** 2) <= 6:
                canvas[y, x] = EYE_RED
                # Glowing effect
                if ((x - 13) ** 2 + (y - 11) ** 2) <= 2:
                    canvas[y, x] = EYE_GLOW
                # Pupil
                if x == 13 and y == 11:
                    canvas[y, x] = BLACK
    
    # Right eye
    for y in range(8, 14):
        for x in range(16, 21):
            if ((x - 18) ** 2 + (y - 11) ** 2) <= 6:
                canvas[y, x] = EYE_RED
                if ((x - 18) ** 2 + (y - 11) ** 2) <= 2:
                    canvas[y, x] = EYE_GLOW
                if x == 18 and y == 11:
                    canvas[y, x] = BLACK
    
    # Beak (opened wide for attack)
    beak_points = [(14, 14), (14, 17), (15, 13), (15, 18), (16, 14), (16, 17), (17, 15), (17, 16)]
    for y, x in beak_points:
        canvas[y, x] = BEAK_YELLOW
        if x >= 16 or y >= 16:
            canvas[y, x] = BEAK_DARK
    
    # Venom dripping from beak
    venom_points = [(18, 15), (19, 16), (20, 15)]
    for y, x in venom_points:
        canvas[y, x] = VENOM
    
    # Aggressive tentacles (raised for attack)
    # Tentacle 1 (striking upward left)
    strike_tentacle_1 = [(18, 6), (17, 5), (16, 4), (15, 3), (14, 2), (13, 1), (12, 0)]
    for y, x in strike_tentacle_1:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            canvas[y + 1, x + 1] = TENTACLE_DARK if y + 1 < size and x + 1 < size else TENTACLE_PURPLE
            # Glowing suckers in attack mode
            if (y + x) % 2 == 0:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 2 (striking upward right)
    strike_tentacle_2 = [(18, 26), (17, 27), (16, 28), (15, 29), (14, 30), (13, 31)]
    for y, x in strike_tentacle_2:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            if y + 1 < size and x - 1 >= 0:
                canvas[y + 1, x - 1] = TENTACLE_DARK
            if (y + x) % 2 == 0:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 3 (grasping left)
    grasp_tentacle_1 = [(15, 7), (16, 6), (17, 5), (18, 4), (19, 3), (20, 2), (21, 1), (22, 0)]
    for y, x in grasp_tentacle_1:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            canvas[y, x + 1] = TENTACLE_DARK if x + 1 < size else TENTACLE_PURPLE
            if y % 2 == 1:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacle 4 (grasping right)
    grasp_tentacle_2 = [(15, 25), (16, 26), (17, 27), (18, 28), (19, 29), (20, 30), (21, 31)]
    for y, x in grasp_tentacle_2:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = TENTACLE_PURPLE
            if x - 1 >= 0:
                canvas[y, x - 1] = TENTACLE_DARK
            if y % 2 == 1:
                canvas[y, x] = SUCKER_PINK
    
    # Tentacles creating whirlpool (bottom tentacles)
    whirlpool_tentacles = [
        [(19, 12), (21, 11), (23, 10), (25, 9), (27, 8), (29, 7), (31, 6)],
        [(19, 20), (21, 21), (23, 22), (25, 23), (27, 24), (29, 25), (31, 26)],
        [(20, 16), (22, 16), (24, 16), (26, 16), (28, 16), (30, 16), (31, 16)],
        [(20, 14), (22, 15), (24, 14), (26, 13), (28, 12), (30, 11), (31, 10)]
    ]
    
    for tentacle in whirlpool_tentacles:
        for y, x in tentacle:
            if 0 <= x < size and 0 <= y < size:
                canvas[y, x] = TENTACLE_PURPLE
                # Add violent suckers
                if (x + y) % 3 == 0:
                    canvas[y, x] = SUCKER_PINK
                # Shading
                if x >= 28:
                    canvas[y, x] = TENTACLE_DARK
    
    # Whirlpool effect (showing the kraken's power)
    whirlpool_center = (26, 16)
    for radius in range(1, 6):
        for angle in range(0, 360, 30):
            x = int(whirlpool_center[1] + radius * np.cos(np.radians(angle)))
            y = int(whirlpool_center[0] + radius * np.sin(np.radians(angle)))
            if 0 <= x < size and 0 <= y < size:
                if radius % 2 == 0:
                    canvas[y, x] = WHIRLPOOL
                else:
                    canvas[y, x] = FOAM_VIOLENT
    
    # Lightning crackling around the creature (ancient power)
    lightning_points = [
        (2, 8), (3, 10), (1, 12), (4, 14),
        (2, 20), (3, 22), (1, 24), (4, 26),
        (0, 16), (1, 18), (2, 15), (3, 17)
    ]
    for y, x in lightning_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = LIGHTNING
    
    # Violent water eruption
    eruption_points = [
        (0, 4), (0, 28), (1, 2), (1, 30),
        (2, 0), (2, 31), (3, 1), (3, 29),
        (31, 2), (31, 30), (30, 0), (30, 31),
        (29, 1), (29, 29), (28, 3), (28, 27)
    ]
    for y, x in eruption_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = FOAM_VIOLENT
    
    return Image.fromarray(canvas)

def save_kraken_art():
    """Generate and save both versions of kraken art"""
    # Create art directory if it doesn't exist
    art_dir = "art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate both versions
    kraken_img = create_kraken_art()
    kraken_attack_img = create_kraken_attack_art()
    
    # Scale up for consistency with other monsters (8x scale: 32x32 -> 256x256)
    scale_factor = 8
    final_size = (32 * scale_factor, 32 * scale_factor)
    
    # Resize using nearest neighbor to maintain pixel art look
    kraken_img = kraken_img.resize(final_size, Image.Resampling.NEAREST)
    kraken_attack_img = kraken_attack_img.resize(final_size, Image.Resampling.NEAREST)
    
    # Save the images
    kraken_path = os.path.join(art_dir, "kraken_monster.png")
    kraken_attack_path = os.path.join(art_dir, "kraken_monster_attack.png")
    
    kraken_img.save(kraken_path)
    kraken_attack_img.save(kraken_attack_path)
    
    print(f"Regular kraken art saved to: {kraken_path}")
    print(f"Attack kraken art saved to: {kraken_attack_path}")
    
    return kraken_img, kraken_attack_img

if __name__ == "__main__":
    save_kraken_art()