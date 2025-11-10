#!/usr/bin/env python3
"""Stone Golem Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_golem_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    STONE = [128, 128, 128, 255]
    DARK_STONE = [80, 80, 80, 255]
    LIGHT_STONE = [160, 160, 160, 255]
    MOSS = [34, 139, 34, 255]
    GLOW = [255, 140, 0, 255]
    
    # Massive body (rectangular, blocky)
    for y in range(12, 28):
        for x in range(10, 22):
            canvas[y][x] = STONE
    
    # Stone blocks texture
    for y in range(12, 28, 4):
        for x in range(10, 22):
            canvas[y][x] = DARK_STONE
    for x in range(10, 22, 4):
        for y in range(12, 28):
            canvas[y][x] = DARK_STONE
    
    # Head (large, square)
    for y in range(4, 12):
        for x in range(12, 20):
            canvas[y][x] = STONE
    
    # Block pattern on head
    for y in range(4, 12, 3):
        for x in range(12, 20):
            canvas[y][x] = DARK_STONE
    
    # Glowing eyes (magical runes)
    canvas[7][14] = GLOW
    canvas[7][17] = GLOW
    canvas[8][14] = GLOW
    canvas[8][17] = GLOW
    
    # Moss patches (ancient)
    canvas[6][13] = MOSS
    canvas[10][12] = MOSS
    canvas[15][11] = MOSS
    canvas[20][21] = MOSS
    
    # Massive arms
    # Left arm
    for y in range(14, 24):
        for x in range(6, 10):
            canvas[y][x] = STONE
            if (y - 14) % 3 == 0:
                canvas[y][x] = DARK_STONE
    
    # Right arm
    for y in range(14, 24):
        for x in range(22, 26):
            canvas[y][x] = STONE
            if (y - 14) % 3 == 0:
                canvas[y][x] = DARK_STONE
    
    # Fists
    for y in range(24, 28):
        for x in range(5, 10):
            canvas[y][x] = STONE
        for x in range(22, 27):
            canvas[y][x] = STONE
    
    # Legs (short, sturdy)
    for y in range(28, 31):
        for x in range(12, 16):
            canvas[y][x] = DARK_STONE
        for x in range(16, 20):
            canvas[y][x] = DARK_STONE
    
    # Highlights (dimensional look)
    for y in range(6, 26, 3):
        canvas[y][13] = LIGHT_STONE
        canvas[y][19] = LIGHT_STONE
    
    return canvas


def create_golem_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    STONE = [128, 128, 128, 255]
    DARK_STONE = [80, 80, 80, 255]
    LIGHT_STONE = [160, 160, 160, 255]
    GLOW = [255, 140, 0, 255]
    DUST = [139, 119, 101, 150]
    CRACK = [60, 60, 60, 255]
    
    # Body (leaning forward for smash)
    for y in range(14, 26):
        for x in range(8, 20):
            canvas[y][x] = STONE
    
    # Stone texture
    for y in range(14, 26, 4):
        for x in range(8, 20):
            canvas[y][x] = DARK_STONE
    
    # Head lowered
    for y in range(10, 16):
        for x in range(10, 18):
            canvas[y][x] = STONE
    
    # Eyes blazing with power
    canvas[12][12] = GLOW
    canvas[12][15] = GLOW
    canvas[13][12] = GLOW
    canvas[13][15] = GLOW
    # Glow effect
    canvas[12][11] = [GLOW[0], GLOW[1], 0, 150]
    canvas[12][16] = [GLOW[0], GLOW[1], 0, 150]
    
    # Massive right fist raised
    for y in range(6, 12):
        for x in range(18, 26):
            canvas[y][x] = STONE
            if y % 2 == 0:
                canvas[y][x] = DARK_STONE
    
    # Fist details
    for x in range(20, 24):
        canvas[8][x] = LIGHT_STONE
    
    # Left arm bracing
    for y in range(16, 22):
        for x in range(4, 8):
            canvas[y][x] = STONE
    
    # Ground impact cracks
    for x in range(8, 24):
        canvas[26][x] = CRACK
        if x % 3 == 0:
            canvas[27][x] = CRACK
            canvas[28][x] = CRACK
    
    # Dust clouds from impact
    for y in range(24, 28):
        for x in range(10, 22, 2):
            canvas[y][x] = DUST
    
    # Motion lines from fist
    for i in range(4):
        canvas[8+i][27+i] = [100, 100, 100, 100]
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_golem_art(), 'RGBA')
    img = img.resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/golem_monster.png")
    print(f"✅ Created: {art_dir}/golem_monster.png")
    
    attack = Image.fromarray(create_golem_attack_art(), 'RGBA')
    attack = attack.resize((256, 256), Image.NEAREST)
    attack.save(f"{art_dir}/golem_monster_attack.png")
    print(f"✅ Created: {art_dir}/golem_monster_attack.png")


if __name__ == "__main__":
    print("🗿 Generating Stone Golem Art...")
    save_images()
    print("🗿 Complete!")
