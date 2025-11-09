#!/usr/bin/env python3
"""
Merman King Monster Art Generator - Creates pixel art for the merman king monster
Inspired by Neptune with trident, crown, and regal appearance
Creates both regular and attack versions of the merman king
"""

import numpy as np
from PIL import Image
import os

def create_merman_king_art():
    """Create regular merman king pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for merman king (Neptune-inspired)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    SKIN_TAN = [210, 180, 140, 255]       # Tanned weathered skin
    SKIN_DARK = [180, 150, 110, 255]     # Darker skin shading
    BEARD_WHITE = [245, 245, 245, 255]    # White flowing beard
    BEARD_GRAY = [200, 200, 200, 255]    # Gray beard shading
    HAIR_GRAY = [160, 160, 160, 255]     # Gray hair
    CROWN_GOLD = [255, 215, 0, 255]      # Golden crown
    CROWN_DARK = [200, 170, 0, 255]      # Crown shading
    JEWEL_BLUE = [0, 100, 200, 255]      # Crown jewel
    TRIDENT_GOLD = [255, 215, 0, 255]    # Golden trident
    TRIDENT_DARK = [200, 170, 0, 255]    # Trident shading
    TRIDENT_HANDLE = [139, 69, 19, 255]  # Brown trident handle
    TAIL_BLUE = [0, 120, 180, 255]       # Royal blue tail
    TAIL_DARK = [0, 80, 120, 255]        # Darker tail shading
    SCALES_SILVER = [192, 192, 192, 255] # Silver scale highlights
    CAPE_PURPLE = [128, 0, 128, 255]     # Royal purple cape
    CAPE_DARK = [100, 0, 100, 255]       # Cape shading
    WATER_FOAM = [220, 248, 255, 255]    # Water foam effects
    
    # Head (larger and more imposing)
    for y in range(8, 16):
        for x in range(12, 20):
            if ((x - 16) ** 2 + (y - 12) ** 2) <= 12:
                canvas[y, x] = SKIN_TAN
                # Add shading
                if x >= 17 or y >= 14:
                    canvas[y, x] = SKIN_DARK
    
    # Crown (elaborate)
    # Crown base
    for x in range(11, 21):
        canvas[7, x] = CROWN_GOLD
        canvas[6, x] = CROWN_DARK
    
    # Crown spikes
    for x in [12, 14, 16, 18, 20]:
        canvas[5, x] = CROWN_GOLD
        canvas[4, x] = CROWN_GOLD
        if x == 16:  # Center spike taller
            canvas[3, x] = CROWN_GOLD
    
    # Crown jewel (center)
    canvas[6, 16] = JEWEL_BLUE
    
    # Eyes (piercing and regal)
    canvas[10, 14] = BLACK
    canvas[10, 18] = BLACK
    canvas[9, 14] = WHITE  # Eye highlight
    canvas[9, 18] = WHITE
    
    # Nose
    canvas[12, 16] = SKIN_DARK
    
    # Mouth (stern expression)
    for x in range(15, 18):
        canvas[13, x] = BLACK
    
    # Flowing beard
    # Beard main shape
    for y in range(14, 22):
        for x in range(13, 19):
            if y >= 16:
                width = max(2, 6 - (y - 16))
                start_x = 16 - width // 2
                end_x = 16 + width // 2
                if start_x <= x <= end_x:
                    canvas[y, x] = BEARD_WHITE
                    # Add gray shading
                    if x >= 17 or (y - 14) % 2 == 1:
                        canvas[y, x] = BEARD_GRAY
            else:
                canvas[y, x] = BEARD_WHITE
                if x >= 17:
                    canvas[y, x] = BEARD_GRAY
    
    # Hair (flowing from crown)
    for x in range(10, 12):
        for y in range(8, 14):
            canvas[y, x] = HAIR_GRAY
    for x in range(20, 22):
        for y in range(8, 14):
            canvas[y, x] = HAIR_GRAY
    
    # Muscular torso
    for y in range(16, 24):
        width = 8 - abs(y - 20)
        start_x = 16 - width // 2
        end_x = 16 + width // 2
        for x in range(start_x, end_x + 1):
            canvas[y, x] = SKIN_TAN
            # Muscle definition
            if x >= start_x + width // 2 or y >= 22:
                canvas[y, x] = SKIN_DARK
    
    # Royal cape (flowing behind)
    for y in range(14, 26):
        for x in range(8, 12):
            if y >= 16:
                canvas[y, x] = CAPE_PURPLE
                if x >= 10 or y >= 24:
                    canvas[y, x] = CAPE_DARK
    
    # Arms (powerful)
    # Left arm (holding trident)
    for y in range(18, 24):
        for x in range(6, 10):
            if abs(x - 7) <= 1:
                canvas[y, x] = SKIN_TAN
                if x >= 8:
                    canvas[y, x] = SKIN_DARK
    
    # Right arm
    for y in range(18, 22):
        for x in range(22, 26):
            if abs(x - 24) <= 1:
                canvas[y, x] = SKIN_TAN
                if x >= 24:
                    canvas[y, x] = SKIN_DARK
    
    # Trident (Neptune's signature weapon)
    # Trident handle
    for y in range(8, 26):
        canvas[y, 4] = TRIDENT_HANDLE
        canvas[y, 5] = TRIDENT_HANDLE
    
    # Trident head
    # Center prong
    for y in range(2, 8):
        canvas[y, 4] = TRIDENT_GOLD
        canvas[y, 5] = TRIDENT_GOLD
    
    # Side prongs
    for y in range(4, 8):
        canvas[y, 2] = TRIDENT_GOLD  # Left prong
        canvas[y, 7] = TRIDENT_GOLD  # Right prong
    
    # Prong tips
    canvas[2, 2] = TRIDENT_GOLD
    canvas[2, 7] = TRIDENT_GOLD
    canvas[1, 4] = TRIDENT_GOLD
    canvas[1, 5] = TRIDENT_GOLD
    
    # Trident decorative elements
    canvas[6, 3] = TRIDENT_DARK
    canvas[6, 6] = TRIDENT_DARK
    
    # Merman tail (powerful and regal)
    for y in range(24, 32):
        width = 6 + (y - 24) // 2
        start_x = 16 - width // 2
        end_x = 16 + width // 2
        for x in range(start_x, end_x + 1):
            canvas[y, x] = TAIL_BLUE
            # Scale pattern
            if (x + y) % 3 == 0:
                canvas[y, x] = SCALES_SILVER
            # Shading
            if x >= start_x + width // 2:
                canvas[y, x] = TAIL_DARK
    
    # Tail fin (majestic)
    fin_points = [(28, 10), (30, 8), (31, 12), (31, 20), (30, 24), (28, 22)]
    for y, x_center in fin_points:
        for x_offset in range(-2, 3):
            x = x_center + x_offset
            if 0 <= x < size:
                canvas[y, x] = TAIL_BLUE
                if abs(x_offset) >= 1:
                    canvas[y, x] = TAIL_DARK
    
    # Water effects (showing his power over the seas)
    # Water swirls around base
    water_points = [
        (26, 8), (26, 24), (27, 6), (27, 26),
        (28, 4), (28, 28), (29, 2), (29, 30)
    ]
    for y, x in water_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_FOAM
    
    return Image.fromarray(canvas)

def create_merman_king_attack_art():
    """Create attack version of merman king pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Same color palette
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    SKIN_TAN = [210, 180, 140, 255]
    SKIN_DARK = [180, 150, 110, 255]
    BEARD_WHITE = [245, 245, 245, 255]
    BEARD_GRAY = [200, 200, 200, 255]
    HAIR_GRAY = [160, 160, 160, 255]
    CROWN_GOLD = [255, 215, 0, 255]
    CROWN_DARK = [200, 170, 0, 255]
    JEWEL_BLUE = [0, 100, 200, 255]
    TRIDENT_GOLD = [255, 215, 0, 255]
    TRIDENT_DARK = [200, 170, 0, 255]
    TRIDENT_HANDLE = [139, 69, 19, 255]
    TAIL_BLUE = [0, 120, 180, 255]
    TAIL_DARK = [0, 80, 120, 255]
    SCALES_SILVER = [192, 192, 192, 255]
    CAPE_PURPLE = [128, 0, 128, 255]
    CAPE_DARK = [100, 0, 100, 255]
    LIGHTNING = [255, 255, 0, 255]      # Lightning effects
    STORM_CLOUD = [100, 100, 100, 255] # Storm clouds
    WAVE_WHITE = [255, 255, 255, 255]   # Crashing waves
    
    # Head (similar but more aggressive expression)
    for y in range(8, 16):
        for x in range(12, 20):
            if ((x - 16) ** 2 + (y - 12) ** 2) <= 12:
                canvas[y, x] = SKIN_TAN
                if x >= 17 or y >= 14:
                    canvas[y, x] = SKIN_DARK
    
    # Crown (glowing with power)
    for x in range(11, 21):
        canvas[7, x] = CROWN_GOLD
        canvas[6, x] = CROWN_DARK
    
    # Crown spikes with lightning
    for x in [12, 14, 16, 18, 20]:
        canvas[5, x] = CROWN_GOLD
        canvas[4, x] = LIGHTNING  # Lightning on crown spikes
        if x == 16:
            canvas[3, x] = LIGHTNING
    
    # Crown jewel (glowing)
    canvas[6, 16] = LIGHTNING
    canvas[7, 16] = JEWEL_BLUE
    
    # Eyes (glowing with rage)
    canvas[10, 14] = LIGHTNING
    canvas[10, 18] = LIGHTNING
    canvas[9, 14] = WHITE
    canvas[9, 18] = WHITE
    
    # Nose
    canvas[12, 16] = SKIN_DARK
    
    # Mouth (roaring)
    for x in range(14, 19):
        canvas[13, x] = BLACK
    for x in range(15, 18):
        canvas[14, x] = BLACK
    
    # Beard (flowing with power)
    for y in range(14, 22):
        for x in range(13, 19):
            if y >= 16:
                width = max(2, 6 - (y - 16))
                start_x = 16 - width // 2
                end_x = 16 + width // 2
                if start_x <= x <= end_x:
                    canvas[y, x] = BEARD_WHITE
                    if x >= 17 or (y - 14) % 2 == 1:
                        canvas[y, x] = BEARD_GRAY
            else:
                canvas[y, x] = BEARD_WHITE
                if x >= 17:
                    canvas[y, x] = BEARD_GRAY
    
    # Hair (flowing with energy)
    for x in range(10, 12):
        for y in range(8, 14):
            canvas[y, x] = HAIR_GRAY
    for x in range(20, 22):
        for y in range(8, 14):
            canvas[y, x] = HAIR_GRAY
    
    # Torso (tensed for attack)
    for y in range(16, 24):
        width = 8 - abs(y - 20)
        start_x = 16 - width // 2
        end_x = 16 + width // 2
        for x in range(start_x, end_x + 1):
            canvas[y, x] = SKIN_TAN
            if x >= start_x + width // 2 or y >= 22:
                canvas[y, x] = SKIN_DARK
    
    # Cape (billowing with storm winds)
    for y in range(14, 26):
        for x in range(8, 13):  # Wider, more dramatic
            if y >= 16:
                canvas[y, x] = CAPE_PURPLE
                if x >= 11 or y >= 24:
                    canvas[y, x] = CAPE_DARK
    
    # Arms (raised for attack)
    # Left arm (thrusting trident)
    for y in range(16, 22):
        for x in range(6, 10):
            if abs(x - 7) <= 1:
                canvas[y, x] = SKIN_TAN
                if x >= 8:
                    canvas[y, x] = SKIN_DARK
    
    # Right arm (commanding the storm)
    for y in range(16, 20):
        for x in range(22, 26):
            if abs(x - 24) <= 1:
                canvas[y, x] = SKIN_TAN
                if x >= 24:
                    canvas[y, x] = SKIN_DARK
    
    # Trident (crackling with lightning)
    # Handle
    for y in range(6, 24):
        canvas[y, 4] = TRIDENT_HANDLE
        canvas[y, 5] = TRIDENT_HANDLE
    
    # Head (electrified)
    for y in range(1, 6):
        canvas[y, 4] = LIGHTNING
        canvas[y, 5] = LIGHTNING
    
    # Prongs (lightning-charged)
    for y in range(2, 6):
        canvas[y, 2] = LIGHTNING
        canvas[y, 7] = LIGHTNING
    
    # Lightning bolts from trident
    lightning_points = [
        (1, 1), (0, 3), (2, 0), (1, 8), (0, 9), (2, 10)
    ]
    for y, x in lightning_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = LIGHTNING
    
    # Tail (thrashing powerfully)
    for y in range(24, 32):
        width = 7 + (y - 24) // 2  # Slightly wider, more powerful
        start_x = 16 - width // 2
        end_x = 16 + width // 2
        for x in range(start_x, end_x + 1):
            canvas[y, x] = TAIL_BLUE
            if (x + y) % 3 == 0:
                canvas[y, x] = SCALES_SILVER
            if x >= start_x + width // 2:
                canvas[y, x] = TAIL_DARK
    
    # Tail fin (spread wide in attack)
    fin_points = [(29, 8), (30, 6), (31, 10), (31, 22), (30, 26), (29, 24)]
    for y, x_center in fin_points:
        for x_offset in range(-3, 4):  # Wider fin
            x = x_center + x_offset
            if 0 <= x < size:
                canvas[y, x] = TAIL_BLUE
                if abs(x_offset) >= 2:
                    canvas[y, x] = TAIL_DARK
    
    # Storm effects (showing his wrath)
    # Storm clouds
    for y in range(0, 4):
        for x in range(20, 32):
            if (x + y) % 3 == 0:
                canvas[y, x] = STORM_CLOUD
    
    # Crashing waves
    wave_points = [
        (28, 2), (29, 4), (30, 1), (31, 3),
        (26, 28), (27, 30), (28, 29), (29, 31)
    ]
    for y, x in wave_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WAVE_WHITE
    
    # Lightning strikes from right hand
    for y in range(12, 16):
        for x in range(26, 32):
            if (x + y) % 4 == 0:
                canvas[y, x] = LIGHTNING
    
    return Image.fromarray(canvas)

def save_merman_king_art():
    """Generate and save both versions of merman king art"""
    # Create art directory if it doesn't exist
    art_dir = "art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate both versions
    merman_king_img = create_merman_king_art()
    merman_king_attack_img = create_merman_king_attack_art()
    
    # Scale up for consistency with demon (8x scale: 32x32 -> 256x256)
    scale_factor = 8
    final_size = (32 * scale_factor, 32 * scale_factor)
    
    # Resize using nearest neighbor to maintain pixel art look
    merman_king_img = merman_king_img.resize(final_size, Image.Resampling.NEAREST)
    merman_king_attack_img = merman_king_attack_img.resize(final_size, Image.Resampling.NEAREST)
    
    # Save the images
    merman_king_path = os.path.join(art_dir, "merman_king_monster.png")
    merman_king_attack_path = os.path.join(art_dir, "merman_king_monster_attack.png")
    
    merman_king_img.save(merman_king_path)
    merman_king_attack_img.save(merman_king_attack_path)
    
    print(f"Regular merman king art saved to: {merman_king_path}")
    print(f"Attack merman king art saved to: {merman_king_attack_path}")
    
    return merman_king_img, merman_king_attack_img

if __name__ == "__main__":
    save_merman_king_art()