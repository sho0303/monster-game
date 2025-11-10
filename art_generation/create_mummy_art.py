#!/usr/bin/env python3
"""Mummy Guardian Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_mummy_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    BANDAGE = [240, 234, 214, 255]
    DARK_BANDAGE = [200, 190, 170, 255]
    SHADOW = [60, 50, 40, 255]
    EYE_GLOW = [0, 255, 255, 255]
    GOLD = [255, 215, 0, 255]
    
    # Body (humanoid shape wrapped in bandages)
    for y in range(10, 28):
        for x in range(12, 20):
            canvas[y][x] = BANDAGE
    
    # Head
    for y in range(6, 12):
        for x in range(13, 19):
            if (x-16)**2 + (y-9)**2 <= 9:
                canvas[y][x] = BANDAGE
    
    # Bandage wrapping texture (horizontal lines)
    for y in range(6, 28, 2):
        for x in range(12, 20):
            if canvas[y][x][3] > 0:
                canvas[y][x] = DARK_BANDAGE
    
    # Glowing eyes (menacing)
    canvas[8][14] = EYE_GLOW
    canvas[8][17] = EYE_GLOW
    canvas[9][14] = EYE_GLOW
    canvas[9][17] = EYE_GLOW
    
    # Dark shadows (depth)
    canvas[10][13] = SHADOW
    canvas[10][18] = SHADOW
    
    # Arms (reaching forward)
    # Left arm
    for y in range(14, 20):
        canvas[y][10] = BANDAGE
        canvas[y][11] = BANDAGE
        if y % 2 == 0:
            canvas[y][10] = DARK_BANDAGE
    
    # Right arm
    for y in range(14, 20):
        canvas[y][20] = BANDAGE
        canvas[y][21] = BANDAGE
        if y % 2 == 0:
            canvas[y][20] = DARK_BANDAGE
    
    # Hands
    for x in range(8, 12):
        canvas[20][x] = BANDAGE
    for x in range(20, 24):
        canvas[20][x] = BANDAGE
    
    # Golden amulet (ancient artifact)
    canvas[12][15] = GOLD
    canvas[12][16] = GOLD
    canvas[13][15] = GOLD
    canvas[13][16] = GOLD
    
    # Legs
    for y in range(28, 31):
        canvas[y][14] = BANDAGE
        canvas[y][15] = BANDAGE
        canvas[y][17] = BANDAGE
        canvas[y][18] = BANDAGE
    
    return canvas


def create_mummy_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    BANDAGE = [240, 234, 214, 255]
    DARK_BANDAGE = [200, 190, 170, 255]
    SHADOW = [60, 50, 40, 255]
    EYE_GLOW = [0, 255, 255, 255]
    GOLD = [255, 215, 0, 255]
    CURSE = [128, 0, 128, 180]
    
    # Body (lunging forward)
    for y in range(12, 26):
        for x in range(10, 18):
            canvas[y][x] = BANDAGE
    
    # Head (forward)
    for y in range(8, 14):
        for x in range(11, 17):
            if (x-14)**2 + (y-11)**2 <= 9:
                canvas[y][x] = BANDAGE
    
    # Bandage texture
    for y in range(8, 26, 2):
        for x in range(10, 18):
            if canvas[y][x][3] > 0:
                canvas[y][x] = DARK_BANDAGE
    
    # Eyes blazing with ancient power
    canvas[10][12] = EYE_GLOW
    canvas[10][15] = EYE_GLOW
    canvas[11][12] = EYE_GLOW
    canvas[11][15] = EYE_GLOW
    # Eye glow effect
    canvas[10][11] = [EYE_GLOW[0], EYE_GLOW[1], EYE_GLOW[2], 150]
    canvas[10][16] = [EYE_GLOW[0], EYE_GLOW[1], EYE_GLOW[2], 150]
    
    # Arms extended (grabbing)
    # Left arm
    for y in range(16, 22):
        for x in range(4, 10):
            canvas[y][x] = BANDAGE
            if y % 2 == 0:
                canvas[y][x] = DARK_BANDAGE
    
    # Right arm
    for y in range(16, 22):
        for x in range(18, 24):
            canvas[y][x] = BANDAGE
            if y % 2 == 0:
                canvas[y][x] = DARK_BANDAGE
    
    # Grasping hands
    canvas[20][2] = BANDAGE
    canvas[21][2] = BANDAGE
    canvas[21][3] = BANDAGE
    canvas[20][25] = BANDAGE
    canvas[21][25] = BANDAGE
    canvas[21][26] = BANDAGE
    
    # Golden amulet glowing
    canvas[14][13] = GOLD
    canvas[14][14] = GOLD
    canvas[15][13] = GOLD
    canvas[15][14] = GOLD
    
    # Ancient curse energy (purple mist)
    for x in range(6, 22, 2):
        canvas[18][x] = CURSE
        canvas[19][x] = CURSE
    
    # Loose bandages flying
    canvas[12][8] = DARK_BANDAGE
    canvas[13][7] = DARK_BANDAGE
    canvas[12][20] = DARK_BANDAGE
    canvas[13][21] = DARK_BANDAGE
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_mummy_art(), 'RGBA')
    img = img.resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/mummy_monster.png")
    print(f"✅ Created: {art_dir}/mummy_monster.png")
    
    attack = Image.fromarray(create_mummy_attack_art(), 'RGBA')
    attack = attack.resize((256, 256), Image.NEAREST)
    attack.save(f"{art_dir}/mummy_monster_attack.png")
    print(f"✅ Created: {art_dir}/mummy_monster_attack.png")


if __name__ == "__main__":
    print("🧟 Generating Mummy Guardian Art...")
    save_images()
    print("🧟 Complete!")
