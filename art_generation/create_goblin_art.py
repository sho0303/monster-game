#!/usr/bin/env python3
"""
Goblin Thief Monster Art Generator
Creates pixel art for sneaky goblin
"""

import numpy as np
from PIL import Image
import os

def create_goblin_art():
    """Create goblin pixel art"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    GREEN = [34, 139, 34, 255]
    DARK_GREEN = [0, 100, 0, 255]
    YELLOW = [255, 215, 0, 255]  # Gold coins
    BROWN = [139, 69, 19, 255]
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    RED = [255, 0, 0, 255]
    GRAY = [128, 128, 128, 255]
    
    # Large goblin head (characteristic big head)
    for y in range(8, 18):
        for x in range(10, 22):
            if (x-16)**2 + (y-13)**2 <= 36:
                canvas[y][x] = GREEN
    
    # Pointed ears
    canvas[10][8] = GREEN
    canvas[11][8] = DARK_GREEN
    canvas[10][24] = GREEN
    canvas[11][24] = DARK_GREEN
    
    # Evil eyes
    canvas[12][13] = BLACK
    canvas[12][19] = BLACK
    canvas[13][13] = RED
    canvas[13][19] = RED
    
    # Crooked grin
    for x in range(13, 19):
        canvas[15][x] = BLACK
    canvas[16][14] = WHITE  # Tooth
    canvas[16][17] = WHITE  # Tooth
    
    # Small body
    for y in range(18, 26):
        for x in range(12, 20):
            canvas[y][x] = DARK_GREEN
    
    # Ragged vest
    for y in range(19, 24):
        for x in range(13, 19):
            canvas[y][x] = BROWN
    
    # Arms (one holding sack)
    # Left arm
    for y in range(20, 24):
        canvas[y][10] = GREEN
        canvas[y][11] = GREEN
    
    # Right arm extended
    for y in range(20, 24):
        canvas[y][20] = GREEN
        canvas[y][21] = GREEN
    
    # Money sack
    for y in range(22, 28):
        for x in range(21, 25):
            canvas[y][x] = BROWN
    # Gold coins spilling out
    canvas[24][22] = YELLOW
    canvas[25][23] = YELLOW
    canvas[26][24] = YELLOW
    
    # Legs
    for y in range(26, 30):
        canvas[y][14] = GREEN
        canvas[y][15] = GREEN
        canvas[y][17] = GREEN
        canvas[y][18] = GREEN
    
    # Simple feet
    canvas[30][13:16] = BROWN
    canvas[30][17:20] = BROWN
    
    return canvas

def create_goblin_attack_art():
    """Create goblin attack animation"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    GREEN = [34, 139, 34, 255]
    DARK_GREEN = [0, 100, 0, 255]
    BROWN = [139, 69, 19, 255]
    BLACK = [0, 0, 0, 255]
    RED = [255, 0, 0, 255]
    GRAY = [192, 192, 192, 255]
    
    # Head (lunging forward)
    for y in range(6, 16):
        for x in range(8, 20):
            if (x-14)**2 + (y-11)**2 <= 36:
                canvas[y][x] = GREEN
    
    # Ears
    canvas[8][6] = GREEN
    canvas[8][22] = GREEN
    
    # Angry eyes
    canvas[10][11] = RED
    canvas[10][17] = RED
    canvas[11][11] = BLACK
    canvas[11][17] = BLACK
    
    # Snarl
    for x in range(11, 17):
        canvas[13][x] = BLACK
    
    # Body (crouched)
    for y in range(16, 24):
        for x in range(10, 18):
            canvas[y][x] = DARK_GREEN
    
    # Arms extended (attacking with dagger)
    # Left arm
    for y in range(18, 22):
        for x in range(6, 10):
            canvas[y][x] = GREEN
    
    # Right arm with dagger
    for y in range(18, 22):
        for x in range(18, 22):
            canvas[y][x] = GREEN
    
    # Dagger blade
    for y in range(16, 20):
        canvas[y][23] = GRAY
        canvas[y][24] = GRAY
    canvas[15][23] = GRAY  # Point
    
    # Dagger handle
    canvas[20][22] = BROWN
    canvas[21][22] = BROWN
    
    # Motion lines
    for i in range(3):
        canvas[17+i][25+i] = [128, 128, 128, 100]
        canvas[18+i][26+i] = [128, 128, 128, 80]
    
    return canvas

def save_images():
    """Generate and save goblin images"""
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    canvas = create_goblin_art()
    img = Image.fromarray(canvas, 'RGBA')
    img_scaled = img.resize((256, 256), Image.NEAREST)
    img_scaled.save(f"{art_dir}/goblin_monster.png")
    print(f"✅ Created: {art_dir}/goblin_monster.png")
    
    attack_canvas = create_goblin_attack_art()
    attack_img = Image.fromarray(attack_canvas, 'RGBA')
    attack_scaled = attack_img.resize((256, 256), Image.NEAREST)
    attack_scaled.save(f"{art_dir}/goblin_monster_attack.png")
    print(f"✅ Created: {art_dir}/goblin_monster_attack.png")

if __name__ == "__main__":
    print("👺 Generating Goblin Art...")
    save_images()
    print("👺 Complete!")
