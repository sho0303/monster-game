#!/usr/bin/env python3
"""
Whale Monster Art Generator - Creates pixel art for a massive whale monster
Inspired by ocean whales with distinctive features and water spout attack
Creates both regular and attack versions of the whale monster
"""

import numpy as np
from PIL import Image
import os

def create_whale_monster_art():
    """Create regular whale monster pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for whale monster
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    WHALE_BLUE = [70, 130, 180, 255]      # Steel blue whale body
    WHALE_DARK = [45, 85, 120, 255]       # Darker whale shading
    WHALE_LIGHT = [135, 170, 210, 255]    # Lighter whale highlights
    BELLY_WHITE = [240, 248, 255, 255]    # White belly
    BELLY_GRAY = [200, 210, 220, 255]     # Gray belly shading
    FIN_DARK = [30, 60, 90, 255]          # Dark fin color
    BLOWHOLE = [20, 20, 20, 255]          # Blowhole opening
    EYE_BLACK = [10, 10, 10, 255]         # Eye color
    WATER_BLUE = [100, 180, 255, 255]     # Water effects
    WATER_FOAM = [220, 248, 255, 255]     # Water foam
    BARNACLE = [160, 140, 120, 255]       # Barnacles on whale
    
    # Main whale body (massive and curved)
    # Upper body curve
    for y in range(6, 22):
        for x in range(4, 28):
            # Create whale body shape - elliptical with tapering
            center_y = 14
            center_x = 16
            
            # Elliptical body with tapering toward tail
            body_width = 12 - abs(x - center_x) * 0.3
            body_height = 8 - abs(y - center_y) * 0.2
            
            distance = ((x - center_x) ** 2) / (body_width ** 2) + ((y - center_y) ** 2) / (body_height ** 2)
            
            if distance <= 1:
                canvas[y, x] = WHALE_BLUE
                # Add shading on bottom and right
                if y >= center_y + 2 or x >= center_x + 4:
                    canvas[y, x] = WHALE_DARK
                # Add highlights on top
                elif y <= center_y - 2 and x <= center_x + 2:
                    canvas[y, x] = WHALE_LIGHT
    
    # Whale head (distinctive bulbous shape)
    for y in range(8, 18):
        for x in range(6, 16):
            head_distance = ((x - 10) ** 2 + (y - 13) ** 2)
            if head_distance <= 25:
                canvas[y, x] = WHALE_BLUE
                # Shading
                if x >= 12 or y >= 15:
                    canvas[y, x] = WHALE_DARK
                # Highlights
                elif x <= 9 and y <= 11:
                    canvas[y, x] = WHALE_LIGHT
    
    # Whale mouth (large and distinctive)
    for y in range(15, 18):
        for x in range(6, 14):
            if y == 16:
                canvas[y, x] = BLACK
            elif y == 15 or y == 17:
                if x >= 8 and x <= 12:
                    canvas[y, x] = WHALE_DARK
    
    # Eye (small but visible)
    canvas[11, 10] = EYE_BLACK
    canvas[10, 10] = WHITE  # Eye highlight
    
    # Blowhole (on top of head)
    canvas[8, 12] = BLOWHOLE
    canvas[8, 13] = BLOWHOLE
    
    # Belly (white/light colored)
    for y in range(16, 20):
        for x in range(8, 24):
            center_x = 16
            belly_width = 8 - abs(x - center_x) * 0.2
            if abs(x - center_x) <= belly_width:
                canvas[y, x] = BELLY_WHITE
                # Gray shading on edges
                if abs(x - center_x) >= belly_width - 1:
                    canvas[y, x] = BELLY_GRAY
    
    # Pectoral fins (side fins)
    # Left fin
    for y in range(13, 17):
        for x in range(2, 6):
            if (x - 3) ** 2 + (y - 15) ** 2 <= 4:
                canvas[y, x] = FIN_DARK
    
    # Right fin
    for y in range(13, 17):
        for x in range(26, 30):
            if (x - 28) ** 2 + (y - 15) ** 2 <= 4:
                canvas[y, x] = FIN_DARK
    
    # Tail section (tapering)
    for y in range(10, 20):
        for x in range(24, 32):
            tail_width = max(1, 6 - (x - 24) * 0.8)
            center_y = 15
            if abs(y - center_y) <= tail_width:
                canvas[y, x] = WHALE_BLUE
                # Shading
                if y >= center_y + 1:
                    canvas[y, x] = WHALE_DARK
    
    # Tail flukes (whale's distinctive tail)
    fluke_points = [
        (8, 30), (6, 31), (4, 30),   # Upper fluke
        (22, 30), (24, 31), (26, 30)  # Lower fluke
    ]
    for y, x in fluke_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = FIN_DARK
            # Add some thickness
            if y >= 6 and y <= 26:
                canvas[y, x-1] = FIN_DARK
    
    # Barnacles and texture details
    barnacle_spots = [(12, 18), (16, 20), (20, 16), (14, 10)]
    for y, x in barnacle_spots:
        canvas[y, x] = BARNACLE
    
    # Water effects around whale
    water_points = [
        (22, 2), (23, 4), (24, 6),    # Water splashes
        (22, 26), (23, 28), (24, 30)
    ]
    for y, x in water_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_FOAM
    
    # Small water droplets
    droplet_points = [(6, 2), (25, 1), (7, 29), (26, 31)]
    for y, x in droplet_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_BLUE
    
    return Image.fromarray(canvas)

def create_whale_monster_attack_art():
    """Create attack version of whale monster with water spout"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Same color palette plus attack effects
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    WHALE_BLUE = [70, 130, 180, 255]
    WHALE_DARK = [45, 85, 120, 255]
    WHALE_LIGHT = [135, 170, 210, 255]
    BELLY_WHITE = [240, 248, 255, 255]
    BELLY_GRAY = [200, 210, 220, 255]
    FIN_DARK = [30, 60, 90, 255]
    BLOWHOLE = [20, 20, 20, 255]
    EYE_BLACK = [10, 10, 10, 255]
    WATER_BLUE = [100, 180, 255, 255]
    WATER_FOAM = [220, 248, 255, 255]
    BARNACLE = [160, 140, 120, 255]
    SPOUT_WHITE = [255, 255, 255, 255]     # Water spout
    SPOUT_BLUE = [180, 220, 255, 255]      # Water spout blue
    PRESSURE_DARK = [50, 50, 50, 255]      # Pressure buildup
    
    # Main whale body (similar to regular but slightly more tense)
    for y in range(6, 22):
        for x in range(4, 28):
            center_y = 14
            center_x = 16
            
            body_width = 12 - abs(x - center_x) * 0.3
            body_height = 8 - abs(y - center_y) * 0.2
            
            distance = ((x - center_x) ** 2) / (body_width ** 2) + ((y - center_y) ** 2) / (body_height ** 2)
            
            if distance <= 1:
                canvas[y, x] = WHALE_BLUE
                if y >= center_y + 2 or x >= center_x + 4:
                    canvas[y, x] = WHALE_DARK
                elif y <= center_y - 2 and x <= center_x + 2:
                    canvas[y, x] = WHALE_LIGHT
    
    # Whale head (more aggressive posture)
    for y in range(8, 18):
        for x in range(6, 16):
            head_distance = ((x - 10) ** 2 + (y - 13) ** 2)
            if head_distance <= 25:
                canvas[y, x] = WHALE_BLUE
                if x >= 12 or y >= 15:
                    canvas[y, x] = WHALE_DARK
                elif x <= 9 and y <= 11:
                    canvas[y, x] = WHALE_LIGHT
    
    # Whale mouth (open wider, more threatening)
    for y in range(14, 19):
        for x in range(6, 16):
            if y == 16:
                canvas[y, x] = BLACK
            elif y == 15 or y == 17:
                if x >= 7 and x <= 13:
                    canvas[y, x] = BLACK
            elif y == 14 or y == 18:
                if x >= 9 and x <= 11:
                    canvas[y, x] = WHALE_DARK
    
    # Eye (more intense, focused)
    canvas[11, 10] = EYE_BLACK
    canvas[10, 9] = WHITE   # Angry highlight
    canvas[11, 9] = EYE_BLACK
    
    # Blowhole (pressurized, ready to spout)
    canvas[8, 12] = PRESSURE_DARK
    canvas[8, 13] = PRESSURE_DARK
    canvas[7, 12] = BLOWHOLE
    canvas[7, 13] = BLOWHOLE
    
    # MASSIVE WATER SPOUT (the main attack feature)
    # Spout base (from blowhole)
    for y in range(5, 8):
        for x in range(11, 15):
            canvas[y, x] = SPOUT_BLUE
            # White foam in center
            if x >= 12 and x <= 13:
                canvas[y, x] = SPOUT_WHITE
    
    # Spout column (shooting upward)
    for y in range(0, 6):
        width = 3 + (5 - y) // 2  # Gets wider as it goes up
        center_x = 12 + (y % 2)   # Slight wave motion
        
        for x_offset in range(-width//2, width//2 + 1):
            x = center_x + x_offset
            if 0 <= x < size:
                canvas[y, x] = SPOUT_BLUE
                # White foam in center
                if abs(x_offset) <= 1:
                    canvas[y, x] = SPOUT_WHITE
    
    # Water droplets flying from spout
    droplet_positions = [
        (1, 8), (0, 10), (2, 16), (1, 18),
        (3, 6), (2, 20), (0, 22), (4, 9)
    ]
    for y, x in droplet_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_BLUE
    
    # Belly (same as regular)
    for y in range(16, 20):
        for x in range(8, 24):
            center_x = 16
            belly_width = 8 - abs(x - center_x) * 0.2
            if abs(x - center_x) <= belly_width:
                canvas[y, x] = BELLY_WHITE
                if abs(x - center_x) >= belly_width - 1:
                    canvas[y, x] = BELLY_GRAY
    
    # Pectoral fins (extended for attack)
    # Left fin (extended)
    for y in range(12, 18):
        for x in range(1, 6):
            if (x - 3) ** 2 + (y - 15) ** 2 <= 6:
                canvas[y, x] = FIN_DARK
    
    # Right fin (extended)
    for y in range(12, 18):
        for x in range(26, 31):
            if (x - 28) ** 2 + (y - 15) ** 2 <= 6:
                canvas[y, x] = FIN_DARK
    
    # Tail section (powerful thrust)
    for y in range(10, 20):
        for x in range(24, 32):
            tail_width = max(1, 6 - (x - 24) * 0.8)
            center_y = 15
            if abs(y - center_y) <= tail_width:
                canvas[y, x] = WHALE_BLUE
                if y >= center_y + 1:
                    canvas[y, x] = WHALE_DARK
    
    # Tail flukes (spread wide for power)
    fluke_points = [
        (6, 30), (4, 31), (2, 30),    # Upper fluke (wider)
        (24, 30), (26, 31), (28, 30)   # Lower fluke (wider)
    ]
    for y, x in fluke_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = FIN_DARK
            if y >= 4 and y <= 28:
                if x > 0:
                    canvas[y, x-1] = FIN_DARK
    
    # Barnacles (same as regular)
    barnacle_spots = [(12, 18), (16, 20), (20, 16), (14, 10)]
    for y, x in barnacle_spots:
        canvas[y, x] = BARNACLE
    
    # Intense water effects (showing power)
    # Turbulent water around whale
    turbulent_water = [
        (22, 2), (23, 3), (24, 5), (25, 7),
        (22, 27), (23, 29), (24, 30), (25, 31),
        (6, 1), (7, 0), (8, 2), (9, 1)
    ]
    for y, x in turbulent_water:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_FOAM
    
    # Water pressure waves
    pressure_waves = [
        (20, 8), (21, 10), (22, 12),
        (20, 20), (21, 22), (22, 24)
    ]
    for y, x in pressure_waves:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = WATER_BLUE
    
    return Image.fromarray(canvas)

def save_whale_monster_art():
    """Generate and save both versions of whale monster art"""
    # Create art directory if it doesn't exist
    art_dir = "art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate both versions
    whale_img = create_whale_monster_art()
    whale_attack_img = create_whale_monster_attack_art()
    
    # Scale up for consistency (8x scale: 32x32 -> 256x256)
    scale_factor = 8
    final_size = (32 * scale_factor, 32 * scale_factor)
    
    # Resize using nearest neighbor to maintain pixel art look
    whale_img = whale_img.resize(final_size, Image.Resampling.NEAREST)
    whale_attack_img = whale_attack_img.resize(final_size, Image.Resampling.NEAREST)
    
    # Save the images
    whale_path = os.path.join(art_dir, "whale_monster.png")
    whale_attack_path = os.path.join(art_dir, "whale_monster_attack.png")
    
    whale_img.save(whale_path)
    whale_attack_img.save(whale_attack_path)
    
    print(f"Regular whale monster art saved to: {whale_path}")
    print(f"Attack whale monster art saved to: {whale_attack_path}")
    
    return whale_img, whale_attack_img

if __name__ == "__main__":
    save_whale_monster_art()