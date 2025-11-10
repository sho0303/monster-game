#!/usr/bin/env python3
"""
Wild Boar Monster Art Generator
Creates pixel art for wild boar
"""

import numpy as np
from PIL import Image
import os

def create_boar_art():
    """Create wild boar pixel art"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BROWN = [101, 67, 33, 255]
    DARK_BROWN = [69, 41, 23, 255]
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    PINK = [255, 182, 193, 255]
    GRAY = [169, 169, 169, 255]
    
    # Body (large and stocky)
    for y in range(12, 24):
        for x in range(6, 26):
            canvas[y][x] = BROWN
    
    # Darker back
    for y in range(12, 18):
        for x in range(8, 24):
            canvas[y][x] = DARK_BROWN
    
    # Head (large snout)
    for y in range(10, 18):
        for x in range(20, 30):
            canvas[y][x] = BROWN
    
    # Snout
    for y in range(14, 17):
        for x in range(28, 31):
            canvas[y][x] = PINK
    
    # Nostrils
    canvas[15][29] = BLACK
    canvas[16][29] = BLACK
    
    # Eye (small, angry)
    canvas[12][24] = BLACK
    canvas[12][25] = BLACK
    canvas[13][24] = BLACK
    
    # Tusks
    canvas[16][28] = WHITE
    canvas[17][28] = WHITE
    canvas[17][29] = WHITE
    canvas[16][30] = WHITE
    canvas[17][30] = WHITE
    
    # Ears
    canvas[9][22] = BROWN
    canvas[8][22] = BROWN
    canvas[9][26] = BROWN
    canvas[8][26] = BROWN
    
    # Legs (short and sturdy)
    # Front legs
    for y in range(24, 30):
        canvas[y][20] = DARK_BROWN
        canvas[y][21] = DARK_BROWN
        canvas[y][24] = DARK_BROWN
        canvas[y][25] = DARK_BROWN
    
    # Back legs
    for y in range(24, 30):
        canvas[y][8] = DARK_BROWN
        canvas[y][9] = DARK_BROWN
        canvas[y][12] = DARK_BROWN
        canvas[y][13] = DARK_BROWN
    
    # Hooves
    canvas[30][20:22] = BLACK
    canvas[30][24:26] = BLACK
    canvas[30][8:10] = BLACK
    canvas[30][12:14] = BLACK
    
    # Tail
    canvas[14][4] = BROWN
    canvas[13][3] = BROWN
    canvas[12][2] = BROWN
    
    return canvas

def create_boar_attack_art():
    """Create wild boar charging attack"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    BROWN = [101, 67, 33, 255]
    DARK_BROWN = [69, 41, 23, 255]
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    PINK = [255, 182, 193, 255]
    DUST = [139, 119, 101, 150]  # Dust cloud
    
    # Body (leaning forward, charging)
    for y in range(14, 26):
        for x in range(4, 24):
            canvas[y][x] = BROWN
    
    # Darker back
    for y in range(14, 20):
        for x in range(6, 22):
            canvas[y][x] = DARK_BROWN
    
    # Head lowered (charging position)
    for y in range(16, 24):
        for x in range(18, 30):
            canvas[y][x] = BROWN
    
    # Snout forward
    for y in range(19, 22):
        for x in range(28, 31):
            canvas[y][x] = PINK
    
    # Angry eye
    canvas[17][22] = BLACK
    canvas[17][23] = BLACK
    canvas[18][22] = BLACK
    
    # Large tusks (prominent in attack)
    canvas[21][28] = WHITE
    canvas[22][28] = WHITE
    canvas[23][28] = WHITE
    canvas[21][30] = WHITE
    canvas[22][30] = WHITE
    canvas[23][30] = WHITE
    canvas[22][29] = WHITE
    
    # Legs in running position
    # Front legs extended
    for y in range(26, 31):
        canvas[y][22] = DARK_BROWN
        canvas[y][23] = DARK_BROWN
    
    # Back legs pushing
    for y in range(26, 30):
        canvas[y][6] = DARK_BROWN
        canvas[y][7] = DARK_BROWN
    
    # Motion dust clouds
    for y in range(28, 31):
        for x in range(1, 6):
            canvas[y][x] = DUST
        for x in range(8, 12):
            canvas[y][x] = DUST
    
    # Speed lines
    for y in range(15, 25, 2):
        for x in range(0, 4):
            canvas[y][x] = [100, 100, 100, 100]
    
    return canvas

def save_images():
    """Generate and save boar images"""
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    canvas = create_boar_art()
    img = Image.fromarray(canvas, 'RGBA')
    img_scaled = img.resize((256, 256), Image.NEAREST)
    img_scaled.save(f"{art_dir}/boar_monster.png")
    print(f"✅ Created: {art_dir}/boar_monster.png")
    
    attack_canvas = create_boar_attack_art()
    attack_img = Image.fromarray(attack_canvas, 'RGBA')
    attack_scaled = attack_img.resize((256, 256), Image.NEAREST)
    attack_scaled.save(f"{art_dir}/boar_monster_attack.png")
    print(f"✅ Created: {art_dir}/boar_monster_attack.png")

if __name__ == "__main__":
    print("🐗 Generating Wild Boar Art...")
    save_images()
    print("🐗 Complete!")
