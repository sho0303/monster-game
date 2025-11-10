#!/usr/bin/env python3
"""Bandit Leader Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_bandit_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    SKIN = [210, 180, 140, 255]
    BLACK = [0, 0, 0, 255]
    BROWN = [101, 67, 33, 255]
    DARK_BROWN = [69, 41, 23, 255]
    RED = [139, 0, 0, 255]  # Bandana
    GRAY = [192, 192, 192, 255]  # Sword
    GOLD = [255, 215, 0, 255]
    LEATHER = [139, 90, 43, 255]
    
    # Bandana (signature bandit look)
    for x in range(11, 21):
        canvas[6][x] = RED
        canvas[7][x] = RED
    # Bandana knot
    canvas[6][21] = RED
    canvas[7][21] = RED
    canvas[7][22] = RED
    
    # Scruffy face
    for y in range(8, 14):
        for x in range(13, 19):
            if (x-16)**2 + (y-11)**2 <= 9:
                canvas[y][x] = SKIN
    
    # Evil eyes
    canvas[10][14] = BLACK
    canvas[10][17] = BLACK
    canvas[11][14] = BLACK
    canvas[11][17] = BLACK
    
    # Scar across face
    for x in range(14, 18):
        canvas[10][x] = DARK_BROWN
    
    # Rough beard
    for y in range(12, 14):
        for x in range(14, 18):
            canvas[y][x] = DARK_BROWN
    
    # Leather vest
    for y in range(14, 24):
        for x in range(12, 20):
            canvas[y][x] = LEATHER
    
    # Belt with buckle
    for x in range(12, 20):
        canvas[20][x] = DARK_BROWN
    canvas[20][15] = GOLD
    canvas[20][16] = GOLD
    
    # Left arm (holding sword)
    for y in range(16, 22):
        canvas[y][10] = SKIN
        canvas[y][11] = SKIN
    
    # Sword blade
    for y in range(8, 18):
        canvas[y][8] = GRAY
        canvas[y][9] = GRAY
    canvas[7][8] = [255, 255, 255, 255]  # Tip
    
    # Sword handle
    canvas[18][8] = BROWN
    canvas[19][8] = BROWN
    canvas[18][9] = BROWN
    canvas[19][9] = BROWN
    
    # Right arm (fist/coin pouch)
    for y in range(16, 22):
        canvas[y][20] = SKIN
        canvas[y][21] = SKIN
    
    # Coin pouch
    for y in range(20, 24):
        for x in range(21, 25):
            canvas[y][x] = DARK_BROWN
    # Gold coins spilling
    canvas[22][24] = GOLD
    canvas[23][25] = GOLD
    canvas[24][26] = GOLD
    
    # Pants
    for y in range(24, 30):
        for x in range(13, 19):
            canvas[y][x] = BLACK
    
    # Boots
    for y in range(30, 32):
        for x in range(12, 16):
            canvas[y][x] = DARK_BROWN
        for x in range(16, 20):
            canvas[y][x] = DARK_BROWN
    
    return canvas


def create_bandit_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    SKIN = [210, 180, 140, 255]
    BLACK = [0, 0, 0, 255]
    BROWN = [101, 67, 33, 255]
    DARK_BROWN = [69, 41, 23, 255]
    RED = [139, 0, 0, 255]
    GRAY = [192, 192, 192, 255]
    WHITE = [255, 255, 255, 255]
    LEATHER = [139, 90, 43, 255]
    SLASH = [200, 200, 200, 180]
    
    # Bandana
    for x in range(9, 19):
        canvas[8][x] = RED
        canvas[9][x] = RED
    canvas[8][19] = RED
    
    # Face (snarling)
    for y in range(10, 16):
        for x in range(11, 17):
            canvas[y][x] = SKIN
    
    # Angry eyes
    canvas[12][12] = BLACK
    canvas[12][15] = BLACK
    canvas[13][12] = RED
    canvas[13][15] = RED
    
    # Scar
    for x in range(12, 16):
        canvas[12][x] = DARK_BROWN
    
    # Grimace
    for x in range(12, 16):
        canvas[14][x] = BLACK
    
    # Vest (action pose)
    for y in range(16, 24):
        for x in range(10, 18):
            canvas[y][x] = LEATHER
    
    # Sword arm extended (slashing)
    for y in range(14, 20):
        for x in range(18, 24):
            canvas[y][x] = SKIN
    
    # SWORD SLASH
    # Blade in motion
    for i in range(12):
        x = 20 + i
        y = 8 + i
        if x < 31 and y < 32:
            canvas[y][x] = GRAY
            if x + 1 < 32:
                canvas[y][x+1] = GRAY
    
    # Blade tip
    canvas[6][20] = WHITE
    canvas[7][21] = WHITE
    
    # Sword handle
    canvas[18][22] = BROWN
    canvas[19][22] = BROWN
    canvas[19][23] = BROWN
    
    # SLASH EFFECT
    for i in range(14):
        x = 22 + i
        y = 10 + i
        if x < 32 and y < 32:
            canvas[y][x] = SLASH
    
    # Motion lines
    for i in range(5):
        canvas[10+i][26+i] = [150, 150, 150, 100]
    
    # Other arm bracing
    for y in range(18, 22):
        canvas[y][6] = SKIN
        canvas[y][7] = SKIN
    
    # Legs in fighting stance
    for y in range(24, 30):
        canvas[y][12] = BLACK
        canvas[y][13] = BLACK
        canvas[y][15] = BLACK
        canvas[y][16] = BLACK
    
    # Dust from movement
    for x in range(8, 18, 2):
        canvas[28][x] = [150, 150, 150, 100]
        canvas[29][x] = [150, 150, 150, 80]
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_bandit_art(), 'RGBA')
    img = img.resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/bandit_monster.png")
    print(f"✅ Created: {art_dir}/bandit_monster.png")
    
    attack = Image.fromarray(create_bandit_attack_art(), 'RGBA')
    attack = attack.resize((256, 256), Image.NEAREST)
    attack.save(f"{art_dir}/bandit_monster_attack.png")
    print(f"✅ Created: {art_dir}/bandit_monster_attack.png")


if __name__ == "__main__":
    print("🗡️ Generating Bandit Leader Art...")
    save_images()
    print("🗡️ Complete!")
