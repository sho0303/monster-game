#!/usr/bin/env python3
"""Dark Sorcerer Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_sorcerer_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    PURPLE = [75, 0, 130, 255]
    DARK_PURPLE = [50, 0, 80, 255]
    SKIN = [210, 180, 140, 255]
    BLACK = [0, 0, 0, 255]
    MAGIC_PURPLE = [138, 43, 226, 255]
    MAGIC_GLOW = [186, 85, 211, 200]
    WHITE = [255, 255, 255, 255]
    
    # Tall pointed hat
    for y in range(2, 8):
        width = (8 - y) // 2 + 1
        for x in range(16 - width, 16 + width):
            canvas[y][x] = DARK_PURPLE
    
    # Hat brim
    for x in range(11, 21):
        canvas[8][x] = PURPLE
        canvas[9][x] = PURPLE
    
    # Face (sinister)
    for y in range(10, 14):
        for x in range(13, 19):
            canvas[y][x] = SKIN
    
    # Evil eyes (glowing)
    canvas[11][14] = MAGIC_PURPLE
    canvas[11][17] = MAGIC_PURPLE
    
    # Goatee (classic evil sorcerer)
    canvas[13][15] = BLACK
    canvas[13][16] = BLACK
    canvas[14][15] = BLACK
    canvas[14][16] = BLACK
    
    # Robe (flowing, mystical)
    for y in range(14, 28):
        width = min(10, 6 + (y - 14) // 3)
        start_x = 16 - width // 2
        for x in range(start_x, start_x + width):
            canvas[y][x] = PURPLE
            if x == start_x or x == start_x + width - 1:
                canvas[y][x] = DARK_PURPLE
    
    # Robe trim (mystical symbols area)
    for y in range(16, 26):
        canvas[y][15] = MAGIC_PURPLE
        canvas[y][16] = MAGIC_PURPLE
    
    # Left arm (holding staff)
    for y in range(16, 22):
        canvas[y][10] = PURPLE
        canvas[y][11] = PURPLE
    
    # Staff
    for y in range(10, 22):
        canvas[y][8] = [101, 67, 33, 255]  # Brown wood
    
    # Crystal on staff (glowing)
    canvas[8][8] = MAGIC_PURPLE
    canvas[9][8] = MAGIC_PURPLE
    canvas[9][7] = MAGIC_GLOW
    canvas[9][9] = MAGIC_GLOW
    
    # Right arm (casting pose)
    for y in range(16, 20):
        canvas[y][20] = PURPLE
        canvas[y][21] = PURPLE
    
    # Magical hand gesture
    canvas[18][22] = SKIN
    canvas[18][23] = SKIN
    canvas[19][22] = SKIN
    
    # Magical sparks around hand
    canvas[17][24] = MAGIC_GLOW
    canvas[19][24] = MAGIC_GLOW
    canvas[18][25] = MAGIC_PURPLE
    
    return canvas


def create_sorcerer_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    PURPLE = [75, 0, 130, 255]
    DARK_PURPLE = [50, 0, 80, 255]
    SKIN = [210, 180, 140, 255]
    MAGIC_PURPLE = [138, 43, 226, 255]
    MAGIC_GLOW = [186, 85, 211, 200]
    ENERGY = [148, 0, 211, 220]
    LIGHTNING = [218, 112, 214, 255]
    
    # Hat (dynamic angle)
    for y in range(4, 10):
        width = (10 - y) // 2 + 1
        for x in range(14 - width, 14 + width):
            canvas[y][x] = DARK_PURPLE
    
    # Hat brim
    for x in range(9, 19):
        canvas[10][x] = PURPLE
    
    # Face (intense concentration)
    for y in range(11, 15):
        for x in range(11, 17):
            canvas[y][x] = SKIN
    
    # Eyes blazing with power
    canvas[12][12] = MAGIC_PURPLE
    canvas[12][15] = MAGIC_PURPLE
    canvas[13][12] = LIGHTNING
    canvas[13][15] = LIGHTNING
    
    # Robe (billowing with power)
    for y in range(15, 26):
        width = min(12, 7 + (y - 15) // 2)
        start_x = 14 - width // 2
        for x in range(start_x, start_x + width):
            canvas[y][x] = PURPLE
    
    # Both arms raised (channeling spell)
    # Left arm
    for y in range(14, 18):
        canvas[y][6+y-14] = PURPLE
        canvas[y][7+y-14] = PURPLE
    
    # Right arm
    for y in range(14, 18):
        canvas[y][25-y+14] = PURPLE
        canvas[y][24-y+14] = PURPLE
    
    # Hands channeling energy
    canvas[16][4] = SKIN
    canvas[16][5] = SKIN
    canvas[16][26] = SKIN
    canvas[16][27] = SKIN
    
    # MASSIVE SPELL EFFECT
    # Energy orb forming
    for y in range(6, 14):
        for x in range(16, 28):
            if (x-22)**2 + (y-10)**2 <= 25:
                canvas[y][x] = ENERGY
    
    # Bright core
    canvas[10][22] = LIGHTNING
    canvas[10][23] = LIGHTNING
    canvas[11][22] = LIGHTNING
    canvas[11][23] = LIGHTNING
    
    # Energy bolts
    for i in range(5):
        canvas[8+i][24+i] = LIGHTNING
        canvas[8+i][26+i] = MAGIC_GLOW
    
    # Magical runes floating
    canvas[12][12] = MAGIC_GLOW
    canvas[14][10] = MAGIC_GLOW
    canvas[16][8] = MAGIC_GLOW
    
    # Dark energy wisps
    for y in range(18, 24, 2):
        canvas[y][10] = ENERGY
        canvas[y][18] = ENERGY
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_sorcerer_art(), 'RGBA')
    img = img.resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/sorcerer_monster.png")
    print(f"✅ Created: {art_dir}/sorcerer_monster.png")
    
    attack = Image.fromarray(create_sorcerer_attack_art(), 'RGBA')
    attack = attack.resize((256, 256), Image.NEAREST)
    attack.save(f"{art_dir}/sorcerer_monster_attack.png")
    print(f"✅ Created: {art_dir}/sorcerer_monster_attack.png")


if __name__ == "__main__":
    print("🧙 Generating Dark Sorcerer Art...")
    save_images()
    print("🧙 Complete!")
