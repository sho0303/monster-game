#!/usr/bin/env python3
"""Scorpion King Monster Art Generator"""
import numpy as np
from PIL import Image
import os


def create_scorpion_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    BLACK = [0, 0, 0, 255]
    RED = [139, 0, 0, 255]
    DARK_RED = [100, 0, 0, 255]
    ORANGE = [255, 140, 0, 255]
    
    # Body segments
    for y in range(14, 20):
        for x in range(10, 22):
            canvas[y][x] = RED
    
    # Head/pincers
    for y in range(16, 19):
        for x in range(22, 28):
            canvas[y][x] = DARK_RED
    
    # Large pincers
    for y in range(14, 17):
        for x in range(26, 30):
            canvas[y][x] = BLACK
    for y in range(19, 22):
        for x in range(26, 30):
            canvas[y][x] = BLACK
    
    # Legs (8 legs)
    for i in range(4):
        # Left legs
        canvas[16+i][6+i] = BLACK
        canvas[17+i][5+i] = BLACK
        # Right legs
        canvas[16+i][25-i] = BLACK
        canvas[17+i][26-i] = BLACK
    
    # Tail (curved up)
    tail_coords = [(8, 20), (6, 18), (4, 16), (3, 14), (2, 12)]
    for x, y in tail_coords:
        canvas[y][x] = RED
        canvas[y][x+1] = RED
    
    # Stinger (poisonous)
    canvas[10][2] = ORANGE
    canvas[10][3] = ORANGE
    canvas[9][2] = ORANGE
    
    return canvas


def create_scorpion_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    BLACK = [0, 0, 0, 255]
    RED = [139, 0, 0, 255]
    ORANGE = [255, 140, 0, 255]
    POISON = [0, 255, 0, 200]
    
    # Body (attacking stance)
    for y in range(18, 24):
        for x in range(8, 20):
            canvas[y][x] = RED
    
    # Head forward
    for y in range(20, 23):
        for x in range(20, 26):
            canvas[y][x] = RED
    
    # Pincers open wide
    for y in range(16, 20):
        for x in range(24, 30):
            canvas[y][x] = BLACK
    for y in range(23, 27):
        for x in range(24, 30):
            canvas[y][x] = BLACK
    
    # Tail striking down
    tail_coords = [(16, 16), (14, 14), (12, 12), (14, 10), (16, 8), (18, 6)]
    for x, y in tail_coords:
        canvas[y][x] = RED
    
    # Stinger with poison drip
    canvas[4][18] = ORANGE
    canvas[5][18] = POISON
    canvas[6][18] = POISON
    
    return canvas


def save_images():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    img = Image.fromarray(create_scorpion_art(), 'RGBA').resize((256, 256), Image.NEAREST)
    img.save(f"{art_dir}/scorpion_monster.png")
    print(f"✅ Created: {art_dir}/scorpion_monster.png")
    
    attack_img = Image.fromarray(create_scorpion_attack_art(), 'RGBA').resize((256, 256), Image.NEAREST)
    attack_img.save(f"{art_dir}/scorpion_monster_attack.png")
    print(f"✅ Created: {art_dir}/scorpion_monster_attack.png")


if __name__ == "__main__":
    print("🦂 Generating Scorpion King Art...")
    save_images()
    print("🦂 Complete!")
