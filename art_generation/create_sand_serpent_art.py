#!/usr/bin/env python3
"""Sand Serpent Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_sand_serpent_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    TAN = [210, 180, 140, 255]
    SAND = [238, 214, 175, 255]
    DARK_TAN = [160, 130, 90, 255]
    BLACK = [0, 0, 0, 255]
    RED = [200, 0, 0, 255]
    YELLOW = [255, 255, 0, 255]
    
    # Serpent body - S-curve pattern
    body_coords = [
        (16, 28), (16, 27), (15, 26), (14, 25), (13, 24),
        (12, 23), (12, 22), (13, 21), (14, 20), (15, 19),
        (16, 18), (16, 17), (15, 16), (14, 15), (13, 14),
        (12, 13), (12, 12), (13, 11), (14, 10), (15, 9),
        (16, 8), (17, 7), (18, 6)
    ]
    
    for x, y in body_coords:
        canvas[y][x] = TAN
        canvas[y][x+1] = TAN
        canvas[y][x+2] = SAND
        # Scales pattern
        if y % 2 == 0:
            canvas[y][x+1] = DARK_TAN
    
    # Head (raised, menacing)
    for y in range(4, 8):
        for x in range(18, 24):
            canvas[y][x] = TAN
    
    # Eyes (slitted snake eyes)
    canvas[5][20] = YELLOW
    canvas[5][22] = YELLOW
    canvas[6][20] = BLACK
    canvas[6][22] = BLACK
    
    # Forked tongue
    canvas[6][24] = RED
    canvas[6][25] = RED
    canvas[7][24] = RED
    canvas[7][26] = RED
    
    # Tail tip
    canvas[29][16] = DARK_TAN
    canvas[30][16] = DARK_TAN
    
    return canvas


def create_sand_serpent_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    TAN = [210, 180, 140, 255]
    SAND = [238, 214, 175, 255]
    DARK_TAN = [160, 130, 90, 255]
    BLACK = [0, 0, 0, 255]
    RED = [200, 0, 0, 255]
    YELLOW = [255, 255, 0, 255]
    POISON = [150, 255, 50, 200]
    
    # Coiled, ready to strike
    body_coords = [
        (10, 26), (11, 25), (12, 24), (13, 23), (14, 22),
        (15, 21), (16, 20), (17, 19), (17, 18), (16, 17),
        (15, 16), (14, 15), (13, 14), (12, 13), (11, 12),
        (10, 11), (10, 10), (11, 9), (12, 8)
    ]
    
    for x, y in body_coords:
        canvas[y][x:x+3] = TAN
        if y % 2 == 0:
            canvas[y][x+1] = DARK_TAN
    
    # Head lunging forward
    for y in range(6, 10):
        for x in range(14, 22):
            canvas[y][x] = TAN
    
    # Fangs (dripping venom)
    canvas[9][18] = YELLOW
    canvas[10][18] = YELLOW
    canvas[11][18] = POISON
    canvas[9][20] = YELLOW
    canvas[10][20] = YELLOW
    canvas[11][20] = POISON
    
    # Eyes blazing
    canvas[7][16] = RED
    canvas[7][19] = RED
    
    # Extended tongue
    canvas[8][22] = RED
    canvas[8][23] = RED
    canvas[9][22] = RED
    canvas[9][24] = RED
    
    # Sand spray effect
    for x in range(20, 28):
        canvas[12][x] = SAND
        canvas[13][x] = [SAND[0], SAND[1], SAND[2], 150]
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_sand_serpent_art(), 'RGBA')
    img = img.resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/sand_serpent_monster.png")
    print(f"✅ Created: {art_dir}/sand_serpent_monster.png")
    
    attack = Image.fromarray(create_sand_serpent_attack_art(), 'RGBA')
    attack = attack.resize((256, 256), Image.NEAREST)
    attack.save(f"{art_dir}/sand_serpent_monster_attack.png")
    print(f"✅ Created: {art_dir}/sand_serpent_monster_attack.png")


if __name__ == "__main__":
    print("🐍 Generating Sand Serpent Art...")
    save_images()
    print("🐍 Complete!")
