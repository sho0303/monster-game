#!/usr/bin/env python3
"""Shadow Wraith Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_wraith_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Semi-transparent ghostly colors
    SHADOW = [40, 40, 60, 180]
    DARK_SHADOW = [20, 20, 40, 200]
    GLOW = [100, 100, 200, 150]
    EYE = [255, 0, 0, 255]
    WISP = [150, 150, 255, 100]
    
    # Hooded figure (ethereal)
    for y in range(6, 14):
        for x in range(11, 21):
            if (x-16)**2//2 + (y-10)**2 <= 16:
                canvas[y][x] = SHADOW
    
    # Hood shadow (darker)
    for y in range(7, 11):
        for x in range(13, 19):
            canvas[y][x] = DARK_SHADOW
    
    # Glowing red eyes (menacing)
    canvas[9][14] = EYE
    canvas[9][17] = EYE
    canvas[10][14] = EYE
    canvas[10][17] = EYE
    
    # Flowing robe/body (fading to transparent)
    for y in range(14, 26):
        width = max(2, 10 - (y - 14) // 2)
        start_x = 16 - width // 2
        for x in range(start_x, start_x + width):
            alpha = max(50, 180 - (y - 14) * 10)
            canvas[y][x] = [SHADOW[0], SHADOW[1], SHADOW[2], alpha]
    
    # Wispy tendrils
    canvas[16][10] = WISP
    canvas[17][9] = WISP
    canvas[18][8] = WISP
    canvas[16][22] = WISP
    canvas[17][23] = WISP
    canvas[18][24] = WISP
    
    # Ethereal glow
    for y in range(12, 20):
        canvas[y][15] = GLOW
        canvas[y][16] = GLOW
    
    return canvas


def create_wraith_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    SHADOW = [40, 40, 60, 200]
    DARK_SHADOW = [20, 20, 40, 220]
    EYE = [255, 0, 0, 255]
    ENERGY = [200, 0, 200, 180]
    WISP = [150, 150, 255, 120]
    
    # Lunging forward, menacing
    for y in range(8, 16):
        for x in range(9, 23):
            if (x-16)**2//3 + (y-12)**2 <= 16:
                canvas[y][x] = SHADOW
    
    # Hood
    for y in range(9, 13):
        for x in range(12, 20):
            canvas[y][x] = DARK_SHADOW
    
    # Blazing eyes
    canvas[11][13] = EYE
    canvas[11][18] = EYE
    canvas[12][13] = EYE
    canvas[12][18] = EYE
    # Eye trails
    canvas[11][12] = [EYE[0], 0, 0, 150]
    canvas[11][19] = [EYE[0], 0, 0, 150]
    
    # Spectral arms reaching
    for y in range(14, 20):
        # Left arm
        canvas[y][4+y-14] = SHADOW
        canvas[y][5+y-14] = DARK_SHADOW
        # Right arm
        canvas[y][27-y+14] = SHADOW
        canvas[y][26-y+14] = DARK_SHADOW
    
    # Clawed hands
    for i in range(3):
        canvas[19+i][9] = [0, 0, 0, 200]
        canvas[19+i][23] = [0, 0, 0, 200]
    
    # Dark energy blast
    for y in range(16, 22):
        for x in range(12, 20):
            canvas[y][x] = ENERGY
    
    # Energy wisps flying
    for i in range(10):
        x = 10 + i
        y = 22 + i // 3
        canvas[y][x] = WISP
    
    # Fade effect at bottom
    for y in range(22, 28):
        alpha = max(30, 150 - (y - 22) * 20)
        for x in range(14, 18):
            canvas[y][x] = [SHADOW[0], SHADOW[1], SHADOW[2], alpha]
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_wraith_art(), 'RGBA')
    img = img.resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/wraith_monster.png")
    print(f"✅ Created: {art_dir}/wraith_monster.png")
    
    attack = Image.fromarray(create_wraith_attack_art(), 'RGBA')
    attack = attack.resize((256, 256), Image.NEAREST)
    attack.save(f"{art_dir}/wraith_monster_attack.png")
    print(f"✅ Created: {art_dir}/wraith_monster_attack.png")


if __name__ == "__main__":
    print("👻 Generating Shadow Wraith Art...")
    save_images()
    print("👻 Complete!")
